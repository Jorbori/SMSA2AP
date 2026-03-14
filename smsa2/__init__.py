"""
Archipelago init file for Super Mario Sunshine Arcade 2
"""
import random
from typing import Dict, Any
import os

from BaseClasses import ItemClassification, Item, Location, MultiWorld
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch_subprocess, icon_paths
from .items import ALL_ITEMS_TABLE, REGULAR_PROGRESSION_ITEMS, USEFUL_ITEMS, ALL_PROGRESSION_ITEMS, TICKET_ITEMS, Smsa2Item
from .locations import ALL_LOCATIONS_TABLE
from .options import Smsa2Options
from .regions import create_regions

logger = logging.getLogger()


def run_client(*args):
    from .SMSA2Client import main
    launch_subprocess(main, name="SMSA2 Client", args=args)

components.append(
    Component("Super Mario Sunshine Arcade 2 Client", func=run_client, component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apsms")))

class SuperMarioSunshineArcade2Settings(settings.Group):
    class ISOFile(settings.UserFilePath):
        description = "Super Mario Sunshine Arcade 2 (USA) NTSC-U ISO File"
        copy_to = None

    class DolphinProcessName(str):
        """The name of the Dolphin process to connect to. Leave blank for system default."""

    iso_file: ISOFile = ISOFile(ISOFile.copy_to)
    dolphin_process_name: DolphinProcessName = ""

class Smsa2WebWorld(WebWorld):
    theme = "ocean"


class Smsa2World(World):
    """
    Created by Augs SMSHacks, Super Mario Sunshine Arcade 2 is a Romhack for Super Mario Sunshine. Featuring 96 platforming gauntlets
    based on mechanics and locations from the base game, the player is given the chance to experience Sunshine's mechanics in a whole
    new light.
    """
    game = "Super Mario Sunshine Arcade 2"
    web = Smsa2WebWorld()

    data_version = 1

    options_dataclass = Smsa2Options
    options: Smsa2Options

    item_name_to_id = ALL_ITEMS_TABLE
    location_name_to_id = ALL_LOCATIONS_TABLE

    goal_shines: int
    possible_shines = 0

    def ticket_item_group() -> str:
        """Item group for World Tickets."""
        res = set()
        ticket_items = ["World 1 Ticket", "World 2 Ticket", "World 3 Ticket", "World 4 Ticket", "World 5 Ticket", "World 6 Ticket", "World 7 Ticket", "World 8 Ticket", "World 9 Ticket", "World 10 Ticket", "World 11 Ticket", "World 12 Ticket"]
        for item in ticket_items:
            res.add(item)
        return res
    
    def nozzle_item_group() -> str:
        """Item group for Nozzles."""
        res = set()
        nozzle_items = ["Spray Nozzle", "Hover Nozzle", "Rocket Nozzle", "Turbo Nozzle", "Bubble Nozzle"]
        for item in nozzle_items:
            res.add(item)
        return res
    
    item_name_groups = {
        "Tickets": ticket_item_group(),
        "Nozzles": nozzle_item_group(),
    }

    def generate_early(self):
        pick = self.random.choice(list(TICKET_ITEMS.keys()))
        tick = str(pick)
        #print(tick)
        self.multiworld.push_precollected(self.create_item(tick))
        if self.options.shuffle_cap == False: self.multiworld.push_precollected(self.create_item("Cap"))

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        start_inv: list[str] = [start_item.name for start_item in self.multiworld.precollected_items[self.player]]

        # Removes any progression item not in the starting items
        pool = [self.create_item(prog_name) for prog_name in REGULAR_PROGRESSION_ITEMS.keys() if not prog_name in start_inv]

        pool = [self.create_item(name) for name in REGULAR_PROGRESSION_ITEMS.keys()]
        if self.options.shuffle_bubble_nozzle == True: pool.append(self.create_item("Bubble Nozzle"))
        if self.options.shuffle_long_jump == True: pool.append(self.create_item("Long Jump"))
        if self.options.shuffle_fruit_gummies == True: pool.append(self.create_item("Fruit Gummies"))
        if self.options.shuffle_dive_helmet == True: pool.append(self.create_item("Dive Helmet"))
        if self.options.shuffle_sunglasses == True: pool.append(self.create_item("Sunglasses"))
        if self.options.shuffle_shine_shirt == True: pool.append(self.create_item("Shine Shirt"))
        if self.options.shuffle_cap == True: pool.append(self.create_item("Cap"))

        pool += [self.create_item(name) for name in TICKET_ITEMS.keys()]

        
        if len(self.multiworld.get_locations(self.player)) - len(pool) - 1 < self.options.shine_count.value:
            self.options.shine_count.value = len(self.multiworld.get_locations(self.player)) - len(pool) - 1

        if self.options.goal_level_shines > self.options.shine_count.value:
            self.options.goal_level_shines.value = self.options.shine_count.value

        for i in range(0, self.options.shine_count.value):
            pool.append(self.create_item("Shine Sprite"))
            self.possible_shines += 1

        for i in range(0, len(self.multiworld.get_locations(self.player)) - len(pool) - 1):
            pool.append(self.create_item("Green Coin"))

        self.multiworld.itempool += pool

    def create_item(self, name: str):
        if name in ALL_PROGRESSION_ITEMS or name == "Bubble Nozzle":
            classification = ItemClassification.progression
        elif name in USEFUL_ITEMS:
            classification = ItemClassification.useful
        else:
            classification = ItemClassification.filler

        return Smsa2Item(name, classification, ALL_ITEMS_TABLE[name], self.player)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
        self.goal_shines = self.options.goal_level_shines
        if self.goal_shines > self.possible_shines:
            self.goal_shines = self.possible_shines
    
    @classmethod
    def stage_fill_hook(cls,
                        multiworld: MultiWorld,
                        progitempool: list[Item],
                        usefulitempool: list[Item],
                        filleritempool: list[Item],
                        fill_locations: list[Location]
                        ) -> None:
        game_player_ids = set(multiworld.get_game_players(cls.game))
        game_minimal_player_ids = {player for player in game_player_ids
                                   if multiworld.worlds[player].options.accessibility == "minimal"}

        def sort_func(item: Item):
            if item.player in game_player_ids and (item.name == "Shine Sprite"):
                if item.player in game_minimal_player_ids:
                    # For minimal players, place Shines first. This helps prevent fill from dumping logically relevant
                    # items into unreachable locations and reducing the number of reachable locations to fewer than the
                    # number of items remaining to be placed.
                    #
                    # Placing only the non-required Shines first or slightly more than the number of non-required
                    # Shines first was also tried, but placing all Shines first seems to give fill the best chance
                    # of succeeding.
                    #
                    # Forcing Shines first has the unfortunately sideeffect of priority fill picking Shines first,
                    # but that will just have to be put up with in order to generate well. Maybe a small buffer of
                    # non-Shines items could be placed first so that the items in the buffer end up on priority
                    # locations.
                    return 1
                else:
                    # For non-minimal players, place Shines last. The helps prevent fill from filling most/all
                    # reachable locations with the Shines macguffins that are only required for the goal.
                    return -1
            else:
                # Python sorting is stable, so this will leave everything else in its original order.
                return 0

        progitempool.sort(key=sort_func)

    
    def fill_slot_data(self) -> Dict[str, Any]:
        return {"difficulty": self.options.difficulty.value,
                "shine_count": self.options.shine_count.value,
                "goal_level_shines": self.options.goal_level_shines.value,
                "shine_sanity": self.options.shine_sanity.value,
                "blue_coin_sanity": self.options.blue_coin_sanity.value,
                "shuffle_bubble_nozzle": self.options.shuffle_bubble_nozzle.value,
                "shuffle_long_jump": self.options.shuffle_long_jump.value,
                "shuffle_fruit_gummies": self.options.shuffle_fruit_gummies.value,
                "shuffle_dive_helmet": self.options.shuffle_dive_helmet.value,
                "shuffle_sunglasses": self.options.shuffle_sunglasses.value,
                "shuffle_shine_shirt": self.options.shuffle_shine_shirt.value,
                "shuffle_cap": self.options.shuffle_cap.value}
    
    def interpret_slot_data(self, slot_data: dict[str, Any]) -> None:
        if "starting_location" in slot_data:
            self.origin_region_name = slot_data["starting_location"]

        if "entrances" in slot_data:
            # Update entrance connections for ER
            entrances = {
                entrance.name: entrance
                for region in self.get_regions()
                for entrance in region.entrances
            }
            for source_exit, target_entrance in slot_data["entrances"]:
                entrances[source_exit].connected_region = entrances[target_entrance].parent_region

# def launch_client():
#    from .SMSA2Client import main
#    launch_subprocess(main, name="SMSA2 client")
# 
# 
# def add_client_to_launcher() -> None:
#     version = "0.4.0"
#     found = False
#     for c in components:
#         if c.display_name == "Super Mario Sunshine Arcade 2 Client":
#             found = True
#             if getattr(c, "version", 0) < version:
#                 c.version = version
#                 c.func = launch_client
#                 return
#     if not found:
#         icon_paths["smsa2_ico"] = f"ap:{__name__}/icon.png"
#         components.append(Component("Super Mario Sunshine Arcade 2 Client", "SMSA2 Client", func=launch_client, component_type=Type.CLIENT, icon="smsa2_ico"))
# 
# 
# add_client_to_launcher()
