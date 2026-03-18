from .smsa2_region_helper import *

WORLD10: Smsa2Region = Smsa2Region(
    Smsa2RegionName.WORLD10,
    ticketed = "World 10 Ticket",
    shines = [
        Shine("10-1 Shine", in_game_bit = 48),
        Shine("10-2 Shine", in_game_bit = 49),
        Shine("10-3 Shine", in_game_bit = 58,
            standard = Requirements([[NozzleType.turbo]]),
            hard = Requirements([[NozzleType.turbo]]),
            expert = Requirements([[NozzleType.turbo]])),
        Shine("10-4 Shine", in_game_bit = 59),
        Shine("10-5 Shine", in_game_bit = 68),
        Shine("10-6 Shine", in_game_bit = 69),
        Shine("10-7 Shine", in_game_bit = 94),
        Shine("10-8 Shine", in_game_bit = 95)
    ],
    blue_coins = [
        BlueCoin("10-1", in_game_bit = 521),
        BlueCoin("10-2", in_game_bit = 522),
        BlueCoin("10-3", in_game_bit = 523),
        BlueCoin("10-4", in_game_bit = 524),
        BlueCoin("10-5", in_game_bit = 525),
        BlueCoin("10-6", in_game_bit = 526),
        BlueCoin("10-7", in_game_bit = 527),
        BlueCoin("10-8", in_game_bit = 528),
    ],
    parent_region = "Menu"
)