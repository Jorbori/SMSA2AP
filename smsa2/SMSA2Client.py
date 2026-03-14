from __future__ import annotations

import asyncio
import collections
import time
import traceback
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass

import ModuleUpdate
from .options import Smsa2Options
from .bit_helper import change_endian, bit_flagger, extract_bits
import dolphin_memory_engine as dme
from . import addresses

try:
    from worlds.tracker.TrackerClient import TrackerGameContext
except:
    pass

ModuleUpdate.update()

import Utils

''' "Comment-Dictionary"
    #Gravi01    Preventing Crash when game is closed/disconnected before Client + Allowing client to reconnect

'''


from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    server_loop
tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for Super Mario Sunshine Arcade 2. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Super Mario Sunshine Arcade 2 is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

ticket_listing = []
world_flags = {}
debug = False
debug_b = False

game_ver = 0x3a


@dataclass
class NozzleItem:
    nozzle_name: str
    ap_item_id: int


NOZZLES: list[NozzleItem] = [
    NozzleItem("Spray Nozzle", 523000),
    NozzleItem("Hover Nozzle", 523001),
    NozzleItem("Rocket Nozzle", 523002),
    NozzleItem("Turbo Nozzle", 523003),
    NozzleItem("Bubble Nozzle", 523004),
]


class Smsa2CommandProcessor(ClientCommandProcessor):
    def _cmd_connect(self, address: str = "") -> bool:
        if isinstance(self.ctx, Smsa2Context):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")

    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True
        refresh_collection_counts(self.ctx)


class Smsa2Context(SuperContext):
    command_processor: Smsa2CommandProcessor
    game = "Super Mario Sunshine Arcade 2"
    items_handling = 0b111  # full remote

    options: Smsa2Options

    hook_check = False
    hook_nagged = False

    believe_hooked = False

    lives_given = 0
    lives_switch = False

    plaza_episode = 0

    goal = 50
    corona_message_given = False
    blue_status = 1
    fludd_start = 0
    victory = False

    ap_nozzles_received = []

    tags = {"AP"}

    def __init__(self, server_address, password):
        super(Smsa2Context, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Smsa2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []
    
    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Super Mario Sunshine Arcade 2 Client"
        return ui

    '''
    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class Smsa2Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Super Mario Sunshine Arcade 2 Client"

        self.ui = Smsa2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
    '''

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            slot_data = args.get("slot_data")
            self.goal = slot_data.get("goal_level_shines")

    def get_corona_goal(self):
        if self.goal:
            return self.goal
        else:
            return 50


storedShines = []
curShines = []
delaySeconds = .5
location_offset = 523000

def read_string(console_address: int, strlen: int) -> str:
    return dme.read_bytes(console_address, strlen).split(b"\0", 1)[0].decode()


def game_start():
    for x in range(0, addresses.SMS_SHINE_BYTE_COUNT):
        storedShines.append(0x00)
        curShines.append(0x00)
    # dme.hook()
    # return dme.is_hooked()


async def game_watcher(ctx: Smsa2Context):
    while not ctx.exit_event.is_set():

        sync_msg = [{'cmd': 'Sync'}]
        if ctx.locations_checked:
            sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
        await ctx.send_msgs(sync_msg)

        #Gravi01 Begin      
        '''
        dme.is_hooked() returns true if just the emulation stops, as dolphin itself is still running
        this causes the dme to write into a non existing memory, resulting in the crashes.
        changed if to check based on connection status, and unhooking DME properly if connection is lost (Exception)
        ''' 
        if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
            try:
                if addresses.SMS_CURRENT_STAGE != 13:
                    refresh_collection_counts(ctx)
            except Exception:
                logger.info("Connection to Dolphin lost, reconnecting...")
                ctx.dolphin_status = CONNECTION_LOST_STATUS
                dme.un_hook()
        ctx.lives_switch = True
        #Gravi01 End

        if ctx.victory and not ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        await asyncio.sleep(0.2)
        ctx.lives_switch = False


async def location_watcher(ctx):
    def _sub():
        if not dme.is_hooked():
            return

        for x in range(0, addresses.SMS_SHINE_BYTE_COUNT):
            targ_location = addresses.SMS_SHINE_LOCATION_OFFSET + x
            cache_byte = dme.read_byte(targ_location)
            curShines[x] = cache_byte

        if storedShines != curShines:
            memory_changed(ctx)

        return

    while not ctx.exit_event.is_set():
        #Gravi01 Begin      #Changing dme.is_Hooked => Connection Status 
        #if not dme.is_hooked():
            #dme.hook()
        #else:
        if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
        #Gravi01 End
            _sub()
        
        await asyncio.sleep(delaySeconds)

async def dolphin_sync_task(ctx: Smsa2Context) -> None:
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                # if ctx.slot is not None:
                #     # await give_items(ctx)
                #     # await check_locations(ctx)
                #     # await check_current_stage_changed(ctx)
                #     # self._cmd_resync()
                # else:
                if ctx.awaiting_rom:
                    await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:   
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dme.hook()
                if dme.is_hooked():
                    if dme.read_bytes(0x80000000, 6) != b"GMSE21":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dme.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    dme_status = dme.get_status()
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dme.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue
        

async def arbitrary_ram_checks(ctx):
    activated_bits = dme.read_byte(addresses.ARB_NOZZLES_ENABLER)

    while dme.is_hooked():
        for noz in ctx.ap_nozzles_received:
            if noz < 5:
                activated_bits = bit_flagger(activated_bits, noz, True)
                dme.write_byte(addresses.ARB_FLUDD_ENABLER, 0x1)
                dme.write_byte(addresses.ARB_NOZZLES_ENABLER, activated_bits)
        await asyncio.sleep(delaySeconds)


def memory_changed(ctx: Smsa2Context):
    if debug: logger.info("memory_changed: " + str(curShines))
    bit_list = []
    for x in range(0, addresses.SMS_SHINE_BYTE_COUNT):
        bit_found = extract_bits((curShines[x]), x)
        bit_list.extend(bit_found)
        storedShines[x] = curShines[x]
    if debug: logger.info("bit_list: " + str(bit_list))
    parse_bits(bit_list, ctx)


def send_victory(ctx: Smsa2Context):
    if ctx.victory:
        return

    ctx.victory = True
    ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
    logger.info("Congratulations on completing your seed!")
    time.sleep(.05)
    logger.info("ARCHIPELAGO SUPER MARIO SUNSHINE ARCADE 2 CREDITS:")
    time.sleep(.05)
    logger.info("AugsSMSHacks - Super Mario Sunshine Arcade 2 Romhack")
    time.sleep(.05)
    logger.info("MightyMang0o - SMS Arcade 2 Maintainer")
    time.sleep(.05)
    logger.info("MrsMarinaRose, Hatkirby and Joshua MKW - Base SMS Client, Modding and Patching")
    time.sleep(.05)
    logger.info("SlimeGuy6675 - Adapted SMSA2 Client and Logic")
    time.sleep(.05)
    logger.info("FarrisTheAncient, Scipio, Palex00, Mysteryem, Exempt-Medic - Special Thanks")
    logger.info("All Archipelago core devs")
    time.sleep(.05)
    logger.info("Nintendo EAD")
    time.sleep(.05)
    logger.info("...and you. Thanks for playing!")
    return


def parse_bits(all_bits, ctx: Smsa2Context):
    if debug: logger.info("parse_bits: " + str(all_bits))
    if len(all_bits) == 0:
        return

    for x in all_bits:
        if x < 119:
            temp = x + location_offset
            ctx.locations_checked.add(temp)
            if debug: logger.info("checks to send: " + str(temp))
        elif 119 < x <= 549:
            temp = x + location_offset
            ctx.locations_checked.add(temp)
        if x == 119:
            send_victory(ctx)


def get_shine_id(location, value):
    temp = location + value - addresses.SMS_SHINE_LOCATION_OFFSET
    shine_id = int(temp)
    return shine_id


def refresh_item_count(ctx, item_id, targ_address):
    if (dme.read_byte(addresses.SMS_CURRENT_STAGE) == 13 and targ_address == addresses.SMS_SHINE_COUNTER) == False:
        counts = collections.Counter(received_item.item for received_item in ctx.items_received)
        temp = change_endian(counts[item_id])
        #Gravi01 Begin      #Stacktrace where the original Exception was thrown. Keeping the changes in this place as well, you still land here without connection, due to it being an async task
        if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
            try:
                dme.write_byte(targ_address, temp)
            except Exception:
                logger.info("Connection to Dolphin lost, reconnecting...")
                ctx.dolphin_status = CONNECTION_LOST_STATUS
                dme.un_hook()
        #Gravi01 End
    else:
        dme.write_byte(addresses.SMS_SHINE_COUNTER, 96)


def refresh_all_items(ctx: Smsa2Context):
    counts = collections.Counter(received_item.item for received_item in ctx.items_received)
    for items in counts:
        if counts[items] > 0:
            unpack_item(items, ctx, counts[items])
    if counts[523006] >= ctx.get_corona_goal():
        activate_ticket(999999)
        if not ctx.corona_message_given:
            logger.info("Goal Level requirements reached!")
            ctx.corona_message_given = True


def refresh_collection_counts(ctx):
    #if debug: logger.info("refresh_collection_counts")
    refresh_item_count(ctx, 523006, addresses.SMS_SHINE_COUNTER)
    refresh_item_count(ctx, 523014, addresses.SMS_BLUECOIN_COUNTER)
    refresh_all_items(ctx)


def check_world_flags(byte_location, byte_pos, bool_setting):
    if world_flags.get(byte_location):
        byte_value = world_flags.get(byte_location)
    else:
        byte_value = dme.read_byte(byte_location)
    byte_value = bit_flagger(byte_value, byte_pos, bool_setting)
    world_flags.update({byte_location: byte_value})
    return byte_value


def open_stage(ticket):
    value = check_world_flags(ticket.address, ticket.bit_position, True)
    dme.write_byte(ticket.address, value)
    return


def special_noki_handling():
    dme.write_double(addresses.SMS_NOKI_REQ, addresses.SMS_NOKI_LO)
    return


def unpack_item(item, ctx, amt=0):
    if 522999 < item < 523005:
        activate_nozzle(item, ctx)
    elif item == 523008:
        activate_dive_helmet()
    elif item == 523009:
        activate_long_jump()
    elif item == 523010:
        activate_fruit_gummies()
    elif 523013 <= item <= 523015:
        activate_cosmetic(item)
    elif 523030 <= item <= 523041:
        activate_ticket(item)

@dataclass
class Ticket:
    item_name: str
    item_id: int
    bit_position: int
    course_id: int
    episode_id: int
    address: int = 0x805789f8
    active: bool = False


TICKETS: list[Ticket] = [
    Ticket("World 1 Ticket", 523030, 5, 1, -1, 0x805789f8), 
    Ticket("World 2 Ticket", 523031, 5, 2, -1, 0x805789f8),
    Ticket("World 3 Ticket", 523032, 6, 3, -1, 0x805789f8),
    Ticket("World 4 Ticket", 523033, 7, 4, -1, 0x805789f8),
    Ticket("World 5 Ticket", 523034, 1, 5, -1, 0x805789f9),
    Ticket("World 6 Ticket", 523035, 3, 6, -1, 0x805789f9),
    Ticket("World 7 Ticket", 523036, 3, 7, -1, 0x805789fd), 
    Ticket("World 8 Ticket", 523037, 4, 8, -1, 0x805789f9),
    Ticket("World 9 Ticket", 523038, 3, 9, -1, 0x805789fd),
    Ticket("World 10 Ticket", 523039, 3, 10, -1, 0x805789fd), 
    Ticket("World 11 Ticket", 523040, 3, 11, -1, 0x805789fd), 
    Ticket("World 12 Ticket", 523041, 3, 12, -1, 0x805789fd), 
    Ticket("12-8 Ticket", 999999, 6, 12, 7, 0x805789fd)
]


def activate_ticket(id: int):
    for tickets in TICKETS:
        if id == tickets.item_id:
            tickets.active = True
            handle_ticket(tickets)
            if not ticket_listing.__contains__(tickets.item_name):
                ticket_listing.append(tickets.item_name)
                logger.info("Current Tickets: " + str(ticket_listing))


def handle_ticket(tick: Ticket):
    if not tick.active:
        return
    if tick.item_name == "World 9 Ticket":
        special_noki_handling()
    open_stage(tick)
    return


def refresh_all_tickets():
    for tickets in TICKETS:
        handle_ticket(tickets)


def extra_unlocks_needed():
    if not dme.is_hooked():
        return


def get_tracker_ctx(name):
    ctx = TrackerGameContext("", "", no_connection=True)
    ctx.run_generator()

    ctx.player_id = ctx.launch_multiworld.world_name_lookup[name]
    return ctx


def get_in_logic(ctx, items=[], locations=[]):
    ctx.items_received = [(item,) for item in items]  # to account for the list being ids and not Items
    ctx.missing_locations = locations
    return ctx.locations_available


def activate_nozzle(id, ctx):
    if id == 523000:
        if not ctx.ap_nozzles_received.__contains__(0):
            ctx.ap_nozzles_received.append(0)
    if id == 523001:
        if not ctx.ap_nozzles_received.__contains__(1):
            ctx.ap_nozzles_received.append(1)
    if id == 523002:
        if not ctx.ap_nozzles_received.__contains__(2):
            ctx.ap_nozzles_received.append(2)
        # rocket nozzle
    if id == 523003:
        if not ctx.ap_nozzles_received.__contains__(3):
            ctx.ap_nozzles_received.append(3)
        # turbo nozzle
    if id == 523004:
        if not ctx.ap_nozzles_received.__contains__(4):
            ctx.ap_nozzles_received.append(4)
        # bubble nozzle
    return

def activate_long_jump():
    dme.write_byte(addresses.ARB_LONG_JUMP_CHECKER, 1)

def activate_fruit_gummies():
    dme.write_byte(addresses.ARB_FRUIT_GUMMIES_CHECKER, 1)

def activate_dive_helmet():
    dme.write_byte(addresses.ARB_DIVE_HELMET_CHECKER, 1)

def activate_cosmetic(id):
    if id == 523013:
        dme.write_byte(addresses.ARB_SUNGLASSES_CHECKER, 1)
    elif id == 523014:
        dme.write_byte(addresses.ARB_SHINE_SHIRT_CHECKER, 1)
    elif id == 523015:
        dme.write_byte(addresses.ARB_CAP_CHECKER, 1)

async def resolve_tickets(stage, episode, ctx):
    for tick in TICKETS:
        if dme.read_byte(addresses.SMS_CURRENT_STAGE) == 13 and stage == 1 and (episode == 5 or episode == 7):
            logger.info("1-6 and 1-8 have issues with the memory addresses of thier Shines/Blue Coins, and are not locations in the randomizer for the time being. Initiating bootout...")
            dme.write_byte(addresses.SMS_NEXT_STAGE, 13)
            dme.write_byte(addresses.SMS_NEXT_EPISODE, 0)
            break
        if dme.read_byte(addresses.SMS_CURRENT_STAGE) == 13 and tick.course_id == stage and tick.episode_id == -1 and not (stage == 12 and episode == 7) and not tick.active:
            logger.info("Entering a stage without a ticket! Initiating bootout...")
            dme.write_byte(addresses.SMS_NEXT_STAGE, 13)
            dme.write_byte(addresses.SMS_NEXT_EPISODE, 0)
        if dme.read_byte(addresses.SMS_CURRENT_STAGE) == 13 and tick.course_id == 12 and tick.episode_id == 7 and stage == 12 and episode == 7 and not tick.active:
            logger.info("Entering a stage without a ticket! Initiating bootout...")
            dme.write_byte(addresses.SMS_NEXT_STAGE, 13)
            dme.write_byte(addresses.SMS_NEXT_EPISODE, 0)
        else:
            await send_map_id(stage, ctx)
    return

async def send_map_id(map_id, ctx):
    await ctx.send_msgs([{
        "cmd": "Set",
        "key": f"smsa2_map_{ctx.team}_{ctx.slot}",
        "default": 0,
        "want_reply": False,
        "operations": [{"operation": "replace", "value": map_id}]
    }])

async def handle_stages(ctx):
    while not ctx.exit_event.is_set():
        if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS: #Gravi01  change to connection status
            stage = dme.read_byte(addresses.SMS_NEXT_STAGE)
            cur_stage = dme.read_byte(addresses.SMS_CURRENT_STAGE)
            episode = dme.read_byte(addresses.SMS_NEXT_EPISODE)
            cur_episode = dme.read_byte(addresses.SMS_CURRENT_EPISODE)

            if cur_stage != stage:
                resolve_tickets(stage, episode, ctx)
            if cur_stage == 15:
                dme.write_byte(addresses.SMS_NEXT_STAGE, 13)
                dme.write_byte(addresses.SMS_NEXT_EPISODE, 0)
            if ((cur_episode != episode or cur_stage != stage) and cur_stage != 13 and stage >= 1 and stage <= 12) or stage == 14 or stage > 15:
                dme.write_byte(addresses.SMS_NEXT_STAGE, 13)
                #dme.write_byte(addresses.SMS_CURRENT_STAGE, 13)
                dme.write_byte(addresses.SMS_NEXT_EPISODE, 0)
                dme.write_byte(addresses.SMS_CURRENT_EPISODE, 0)
                await send_map_id(next_stage, ctx)
                
        await asyncio.sleep(0.1)


def main(connect= None, password= None):
    Utils.init_logging("SMSA2Client", exception_logger="Client")

    async def _main(connect, password):
        ctx = Smsa2Context(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        game_start()

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        # if dme.is_hooked():
        #     logger.info("Hooked to Dolphin!")

        progression_watcher = asyncio.create_task(game_watcher(ctx), name="Smsa2ProgressionWatcher")
        loc_watch = asyncio.create_task(location_watcher(ctx))
        stage_watch = asyncio.create_task(handle_stages(ctx))
        arbitrary = asyncio.create_task(arbitrary_ram_checks(ctx))

        await progression_watcher
        await loc_watch
        await stage_watch
        await arbitrary
        await asyncio.sleep(.25)

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task


    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser(description="Super Mario Sunshine Arcade 2 Client, for text interfacing.")
    args, rest = parser.parse_known_args()
    main(args.connect, args.password)
