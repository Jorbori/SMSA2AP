from typing import TYPE_CHECKING

from ..generic.Rules import add_rule
from BaseClasses import Entrance, Region

from .smsa2_regions.smsa2_region_helper import Smsa2Location, Smsa2RegionName, Smsa2Region, Shine, BlueCoin
from .smsa2_regions.world1 import (WORLD1)
from .smsa2_regions.world2 import (WORLD2)
from .smsa2_regions.world3 import (WORLD3)
from .smsa2_regions.world4 import (WORLD4)
from .smsa2_regions.world5 import (WORLD5)
from .smsa2_regions.world6 import (WORLD6)
from .smsa2_regions.world7 import (WORLD7)
from .smsa2_regions.world8 import (WORLD8)
from .smsa2_regions.world9 import (WORLD9)
from .smsa2_regions.world10 import (WORLD10)
from .smsa2_regions.world11 import (WORLD11)
from .smsa2_regions.world12 import (WORLD12)
from .smsa2_regions.goal import (GOAL)

if TYPE_CHECKING:
    from . import Smsa2World


def get_location_name_to_id():
    dict_locs: dict[str, int] = {}
    for smsa2_reg in ALL_REGIONS.values():
        for shine_loc in smsa2_reg.shines:
            dict_locs.update({f"{smsa2_reg.name} - {shine_loc.name}": len(dict_locs)+1})
        for blue_loc in smsa2_reg.blue_coins:
            dict_locs.update({f"{smsa2_reg.name} - {blue_loc.name}": len(dict_locs)+1})
        for nozz_loc in smsa2_reg.nozzle_boxes:
            dict_locs.update({f"{smsa2_reg.name} - {nozz_loc.name}": len(dict_locs)+1})
    return dict_locs


ALL_REGIONS: dict[str, Smsa2Region] = {
    "Manu": Smsa2Region("Menu"),
    Smsa2RegionName.WORLD1: WORLD1,
    Smsa2RegionName.WORLD2: WORLD2,
    Smsa2RegionName.WORLD3: WORLD3,
    Smsa2RegionName.WORLD4: WORLD4,
    Smsa2RegionName.WORLD5: WORLD5,
    Smsa2RegionName.WORLD6: WORLD6,
    Smsa2RegionName.WORLD7: WORLD7,
    Smsa2RegionName.WORLD8: WORLD8,
    Smsa2RegionName.WORLD9: WORLD9,
    Smsa2RegionName.WORLD10: WORLD10,
    Smsa2RegionName.WORLD11: WORLD11,
    Smsa2RegionName.WORLD12: WORLD12,
    Smsa2RegionName.GOAL: GOAL
    
}


def create_region(region: Smsa2Region, world: "Smsa2World"):
    curr_region = Region(region.name, world.player, world.multiworld)
    world.multiworld.regions.append(curr_region)

    if region.name == "Hub":
        return curr_region

    # Add Entrance to the parent region and set the requirements to be used later on
    new_entrance: Entrance = world.get_region(region.parent_region).connect(curr_region)
    new_entrance.requirements = region.requirements

    # Require that the player has the ticket required for the region when ticket mode is enabled
    curr_region.ticket_str = region.ticketed
    add_rule(new_entrance, (lambda state, ticket_str=region.ticketed: state.has(ticket_str, world.player)))

    if world.options.shine_sanity == True or world.options.blue_coin_sanity == False:
        for shine in region.shines:
            if (region.trade and world.options.blue_coin_sanity.value > 0 and
                len([reg_loc for reg_loc in curr_region.get_locations()]) >= world.options.trade_shine_maximum.value):
                continue

            shine_loc: Smsa2Location = Smsa2Location(world, f"{curr_region.name} - {shine.name}", region, smsa2_can_get_shine(shine, world))
            curr_region.locations.append(shine_loc)

    if world.options.blue_coin_sanity.value == True:
        for blue_coin in region.blue_coins:
            blue_loc: Smsa2Location = Smsa2Location(world, f"{curr_region.name} - {blue_coin.name}", region, smsa2_can_get_blue_coin(blue_coin, world))
            curr_region.add_event(blue_loc.name, "Blue Coin",
                (lambda state, temp_loc=blue_loc: temp_loc.access_rule(state)))
            curr_region.locations.append(blue_loc)

    for nozzle_box in region.nozzle_boxes:
        nozzle_loc: Smsa2Location = Smsa2Location(world, f"{curr_region.name} - {nozzle_box.name}", region, nozzle_box.requirements)
        curr_region.locations.append(nozzle_loc)

    return curr_region

def smsa2_can_get_shine(shine: Shine, world: "Smsa2World"):
    if world.options.difficulty == 0: return shine.standard
    elif world.options.difficulty == 1: return shine.hard
    elif world.options.difficulty == 2: return shine.expert


def smsa2_can_get_blue_coin(blue_coin: BlueCoin, world: "Smsa2World"):
    if world.options.difficulty == 0: return blue_coin.standard
    elif world.options.difficulty == 1: return blue_coin.hard
    elif world.options.difficulty == 2: return blue_coin.expert

def create_regions(world: "Smsa2World"):
    for region_name, region_data in ALL_REGIONS.items():
        create_region(region_data, world)

    goal_region: Region = world.get_region(Smsa2RegionName.GOAL)
    goal_region.add_event(f"{Smsa2RegionName.GOAL} - 12-8 Shine", "Victory")