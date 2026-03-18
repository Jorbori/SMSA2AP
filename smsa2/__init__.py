"""
Archipelago init file for Super Mario Sunshine Arcade 2
"""
import math
from dataclasses import fields
import os, logging
from typing import Dict, Any, ClassVar
import settings

import Options
from BaseClasses import ItemClassification, MultiWorld, Tutorial, Item, Location
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

from .items import ALL_ITEMS_TABLE, REGULAR_PROGRESSION_ITEMS, OTHER_ITEMS, USEFUL_ITEMS, ALL_PROGRESSION_ITEMS, TICKET_ITEMS, JUNK_ITEMS, Smsa2Item
from .options import *
from .regions import create_regions, ALL_REGIONS
from .iso_helper.smsa2_rom import SMSA2PlayerContainer
from .regions import get_location_name_to_id

logger = logging.getLogger()


def run_client(*args):
    from .SMSA2Client import main
    launch_subprocess(main, name="SMSA2 Client", args=args)

components.append(
    Component("Super Mario Sunshine Arcade 2 Client", func=run_client, component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apsmsa2")))

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
    option_groups = [
        Options.OptionGroup("SMSA2 Basic", [
            options.Difficulty,
            options.ShineCount,
            options.GoalLevelShines,
            options.ShineSanity,
            options.BlueCoinSanity,
            options.ShuffleBubbleNozzle,
            options.ShuffleLongJump,
            options.ShuffleFruitGummies,
            options.ShuffleDiveHelmet,
            options.ShuffleSunglasses,
            options.ShuffleShineShirt,
            options.ShuffleCap,
            options.DeathLink
        ])
    ]

    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Super Mario Sunshine Arcade 2 software on your computer. This guide covers"
        "single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "smsa2/en",
        ["Joshark"]
    )

    tutorials = [setup]

class Smsa2World(World):
    """
    The second Super Mario game to feature 3D gameplay. Coupled with F.L.U.D.D. (a talking water tank that can be used
    as a jetpack), Mario must clean the graffiti off of Delfino Isle and return light to the sky.
    """
    game = "Super Mario Sunshine Arcade 2"
    web = Smsa2WebWorld()

    data_version = 1

    options_dataclass = Smsa2Options
    options: Smsa2Options

    item_name_to_id = ALL_ITEMS_TABLE
    location_name_to_id = get_location_name_to_id()

    settings: ClassVar[SuperMarioSunshineArcade2Settings]
    goal_shines: int = 0
    possible_shines = 0

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    def generate_early(self):
        chosen_tick: str = str(self.random.choice(list(TICKET_ITEMS.keys())))
        self.multiworld.push_precollected(self.create_item(chosen_tick))
        if self.options.shuffle_cap == False: self.multiworld.push_precollected(self.create_item("Cap"))

    def create_regions(self):
        create_regions(self)

    def create_items(self):

        start_inv: list[str] = [start_item.name for start_item in self.multiworld.precollected_items[self.player]]

        # Removes any progression item not in the starting items
        pool = [self.create_item(prog_name) for prog_name in REGULAR_PROGRESSION_ITEMS.keys() if not prog_name in start_inv]
        if self.options.shuffle_bubble_nozzle == True: pool.append(self.create_item("Bubble Nozzle"))
        if self.options.shuffle_long_jump == True: pool.append(self.create_item("Long Jump"))
        if self.options.shuffle_fruit_gummies == True: pool.append(self.create_item("Fruit Gummies"))
        if self.options.shuffle_dive_helmet == True: pool.append(self.create_item("Dive Helmet"))
        if self.options.shuffle_sunglasses == True: pool.append(self.create_item("Sunglasses"))
        if self.options.shuffle_shine_shirt == True: pool.append(self.create_item("Shine Shirt"))
        if self.options.shuffle_cap == True: pool.append(self.create_item("Cap"))
        
        pool += [self.create_item(tick_name) for tick_name in TICKET_ITEMS.keys() if tick_name not in start_inv]

        if len(self.multiworld.get_locations(self.player)) - len(pool) - 1 < self.options.shine_count.value:
            logger.warning(f"SMSA2: Player's Yaml {self.player_name} had shine count higher than maximum locations "
                f"available to them. Adjusting their shine count down to {len(self.multiworld.get_locations(self.player)) - len(pool) - 1}...")
            self.options.shine_count.value = len(self.multiworld.get_locations(self.player)) - len(pool) - 1

        if self.options.goal_level_shines > self.options.shine_count.value:
            logger.warning(f"SMSA2: Player's Yaml {self.player_name} had goal level shines higher than shine count "
                f"available to them. Adjusting their shine count down to {self.options.shine_count.value}...")
            self.options.goal_shines.value = self.options.shine_count.value

        for i in range(0, self.options.shine_count.value):
            pool.append(self.create_item("Shine Sprite"))
            self.possible_shines += 1

        for i in range(0, len(self.multiworld.get_locations(self.player)) - len(pool) - 1):
            pool.append(self.create_item("Green Coin"))

        self.multiworld.itempool += pool

    def create_item(self, name: str):
        if not name in ALL_ITEMS_TABLE:
            raise Exception(f"Invalid SMSA2 item name: {name}")

        if name in ALL_PROGRESSION_ITEMS or name == "Bubble Nozzle":
            if name == "Shine Sprite" or name == "Blue Coin":
                classification = ItemClassification.progression_deprioritized_skip_balancing
            else:
                classification = ItemClassification.progression
        elif name in USEFUL_ITEMS:
            classification = ItemClassification.useful
        else:
            classification = ItemClassification.filler

        return Smsa2Item(name, classification, ALL_ITEMS_TABLE[name], self.player)

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    @classmethod
    def stage_fill_hook(cls, multiworld: MultiWorld, progitempool: list[Item], usefulitempool: list[Item],
        filleritempool: list[Item], fill_locations: list[Location]) -> None:

        # Credit to @Mysteryem for this hook and the sort_fuc.
        game_players = multiworld.get_game_players(cls.game)
        # Get all player IDs that require either corona mountain shines to complete their goal or have blue coins
        smsa2_excessive_prog_items = {player for player in game_players if
            multiworld.worlds[player].goal_shines > 0 or multiworld.worlds[player].blue_coins_required > 0}
        # Get the player IDs of those that are using minimal accessibility.
        smsa2_minimal_players = {player for player in game_players
            if multiworld.worlds[player].options.accessibility == "minimal"}

        def sort_func(item: Item):
            # Credit once again for @Mysteryem for this function AND very nice description
            if item.player in smsa2_excessive_prog_items and item.name in ["Shine Sprite"]:
                if item.player in smsa2_minimal_players:
                    # For minimal players, place goal macguffins first. This helps prevent fill from dumping logically
                    # relevant items into unreachable locations and reducing the number of reachable locations to fewer
                    # than the number of items remaining to be placed.
                    #
                    # Placing only the non-required goal macguffins first or slightly more than the number of
                    # non-required goal macguffins first was also tried, but placing all goal macguffins first seems to
                    # give fill the best chance of succeeding.
                    #
                    # All shine sprites and blue coins are given the *deprioritized* classification for minimal players,
                    # which avoids them being placed on priority locations, which would otherwise occur due to them
                    # being sorted to be placed first. They also skip progression balancing in larger multiworlds.
                    return 1
                else:
                    # For non-minimal players, place goal macguffins last. The helps prevent fill from filling most/all
                    # reachable locations with the goal macguffins that are only required for the goal.
                    return -1
            else:
                # Python sorting is stable, so this will leave everything else in its original order.
                return 0

        progitempool.sort(key=sort_func)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "goal_shines": self.options.goal_shines.value,
            "blue_coin_sanity": self.options.blue_coin_sanity.value,
            "starting_nozzle": self.options.starting_nozzle.value,
            "ticket_mode": self.options.level_access.value,
            "boathouse_maximum": self.options.trade_shine_maximum.value,
            "coin_shine_enabled": self.options.enable_coin_shines.value,
            "death_link": self.options.death_link.value,
            "seed": self.multiworld.seed
        }

    def generate_output(self, output_directory: str):
        from .SMSA2Client import CLIENT_VERSION, AP_WORLD_VERSION_NAME

        output_data = {
            "Seed": self.multiworld.seed,
            "Slot": self.player,
            "Name": self.player_name,
            "Options": {},
            AP_WORLD_VERSION_NAME: CLIENT_VERSION
        }

        for field in fields(self.options):
            output_data["Options"][field.name] = getattr(self.options, field.name).value

        patch_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
            f"{SMSA2PlayerContainer.patch_file_ending}")
        smsa2_container = SMSA2PlayerContainer(output_data, patch_path, self.multiworld.player_name[self.player], self.player)
        smsa2_container.write()

# def launch_client():
#     from .SMSA2Client import main
#     launch_subprocess(main, name="SMSA2 client")


# def add_client_to_launcher() -> None:
#     version = "0.2.0"
#     found = False
#     for c in components:
#         if c.display_name == "Super Mario Sunshine Client":
#             found = True
#             if getattr(c, "version", 0) < version:
#                 c.version = version
#                 c.func = launch_client
#                 return
#     if not found:
#         components.append(Component("Super Mario Sunshine Client", "SMSA2Client",
#                                     func=launch_client))


# add_client_to_launcher()
