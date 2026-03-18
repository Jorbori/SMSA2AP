from .smsa2_region_helper import *

GOAL: Smsa2Region = Smsa2Region(
    Smsa2RegionName.GOAL,
    requirements=[Requirements(goal_level = True)],
    blue_coins = [
        BlueCoin("12-8", in_game_bit = 144)
    ],
    parent_region = "Hub"
)