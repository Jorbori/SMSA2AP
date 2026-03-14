from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Region, ItemClassification
from .items import Smsa2Item
from .locations import Smsa2Location
from .static_logic import ALL_REGIONS, Smsa2Region, Shine, BlueCoin, Requirements, NozzleType

if TYPE_CHECKING:
    from . import Smsa2World


def smsa2_requirements_satisfied(state: CollectionState, requirements: Requirements, world: "Smsa2World"):
    my_nozzles: NozzleType = NozzleType.none
    if state.has("Spray Nozzle", world.player):
        my_nozzles |= NozzleType.spray
    if state.has("Hover Nozzle", world.player):
        my_nozzles |= NozzleType.hover
    if state.has("Rocket Nozzle", world.player):
        my_nozzles |= NozzleType.rocket
    if state.has("Turbo Nozzle", world.player):
        my_nozzles |= NozzleType.turbo
    if state.has("Spray Nozzle", world.player) and state.has("Hover Nozzle", world.player):
        my_nozzles |= NozzleType.sprayandhover
    if state.has("Spray Nozzle", world.player) and state.has("Turbo Nozzle", world.player):
        my_nozzles |= NozzleType.sprayandturbo
    if state.has("Spray Nozzle", world.player) and state.has("Rocket Nozzle", world.player):
        my_nozzles |= NozzleType.sprayandrocket
    if state.has("Turbo Nozzle", world.player) and state.has("Hover Nozzle", world.player):
        my_nozzles |= NozzleType.turboandhover
    if state.has("Turbo Nozzle", world.player) and state.has("Rocket Nozzle", world.player):
        my_nozzles |= NozzleType.turboandrocket
    if state.has("Hover Nozzle", world.player) and state.has("Rocket Nozzle", world.player):
        my_nozzles |= NozzleType.hoverandrocket
    if state.has("Bubble Nozzle", world.player) and state.has("Bubble Nozzle", world.player):
        my_nozzles |= NozzleType.bubble
        


    for req in requirements.nozzles:
        if my_nozzles & req == NozzleType(0):
            return False

    if requirements.shines is not None and not state.has("Shine Sprite", world.player, requirements.shines):
        return False

    if requirements.blues is not None and not state.has("Blue Coin", world.player, requirements.blues):
        return False

    if requirements.corona and not state.has("Shine Sprite", world.player, world.options.goal_level_shines.value):
        return False

    if requirements.location != "" and not state.can_reach(requirements.location, "Location", world.player):
        return False

    return True


def smsa2_can_get_shine(state: CollectionState, shine: Shine, world: "Smsa2World"):
    if world.options.difficulty == 0: return smsa2_requirements_satisfied(state, shine.standard, world)
    elif world.options.difficulty == 1: return smsa2_requirements_satisfied(state, shine.hard, world)
    elif world.options.difficulty == 2: return smsa2_requirements_satisfied(state, shine.expert, world)


def smsa2_can_get_blue_coin(state: CollectionState, blue_coin: BlueCoin, world: "Smsa2World"):
    if world.options.difficulty == 0: return smsa2_requirements_satisfied(state, blue_coin.standard, world)
    elif world.options.difficulty == 1: return smsa2_requirements_satisfied(state, blue_coin.hard, world)
    elif world.options.difficulty == 2: return smsa2_requirements_satisfied(state, blue_coin.expert, world)


def smsa2_can_use_entrance(state: CollectionState, region: Smsa2Region, world: "Smsa2World"):
    if region.ticketed:
        return state.has(region.ticketed, world.player)
    else:
        return smsa2_requirements_satisfied(state, region.requirements, world)


def make_shine_lambda(shine: Shine, world: "Smsa2World"):
    return lambda state: smsa2_can_get_shine(state, shine, world)


def make_blue_coin_lambda(blue_coin: BlueCoin, world: "Smsa2World"):
    return lambda state: smsa2_can_get_blue_coin(state, blue_coin, world)


def make_entrance_lambda(region: Smsa2Region, world: "Smsa2World"):
    return lambda state: smsa2_can_use_entrance(state, region, world)


def create_region(region: Smsa2Region, world: "Smsa2World"):
    new_region = Region(region.name, world.player, world.multiworld)
    if world.options.shine_sanity == True or world.options.blue_coin_sanity == False:
        for shine in region.shines:
            new_location = Smsa2Location(world.player, f"{region.display} - {shine.name}", shine.id, new_region)
            new_location.access_rule = make_shine_lambda(shine, world)
            new_region.locations.append(new_location)
    if world.options.blue_coin_sanity == True:
        for blue_coin in region.blue_coins:
            new_location = Smsa2Location(
                world.player, f"{region.display} - {blue_coin.name} Blue Coin", blue_coin.id, new_region)
            new_location.access_rule = make_blue_coin_lambda(blue_coin, world)
            new_region.locations.append(new_location)

    if region.name == "Goal Level":
        new_location = Smsa2Location(world.player, "12-8 Shine", None, new_region)
        new_location.access_rule = lambda state: smsa2_requirements_satisfied(state, Requirements(corona = True),
                                                                            world)
        new_region.locations.append(new_location)

        event_item = Smsa2Item("Victory", ItemClassification.progression, None, world.player)
        new_location.place_locked_item(event_item)
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)

    return new_region


def create_regions(world: "Smsa2World"):
    regions = {
        "Menu": Region("Menu", world.player, world.multiworld)
    }

    for region in ALL_REGIONS:
        regions[region.name] = create_region(region, world)
        regions[region.parent_region].connect(regions[region.name], None, make_entrance_lambda(region, world))

    world.multiworld.regions += regions.values()
