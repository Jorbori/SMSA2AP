from .smsa2_region_helper import *

WORLD12: Smsa2Region = Smsa2Region(
    Smsa2RegionName.WORLD12,
    ticketed = "World 12 Ticket",
    shines = [
        Shine("12-1 Shine", in_game_bit = 104),
        Shine("12-2 Shine", in_game_bit = 105,
            standard = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.turbo], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.turbo], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        Shine("12-3 Shine", in_game_bit = 106),
        Shine("12-4 Shine", in_game_bit = 107),
        Shine("12-5 Shine", in_game_bit = 116,
            standard = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.bubble]])),
        Shine("12-6 Shine", in_game_bit = 117),
        Shine("12-7 Shine", in_game_bit = 118)
    ],
    blue_coins = [
        BlueCoin("12-1", in_game_bit = 137),
        BlueCoin("12-2", in_game_bit = 138),
        BlueCoin("12-3", in_game_bit = 139),
        BlueCoin("12-4", in_game_bit = 140),
        BlueCoin("12-5", in_game_bit = 141,
            standard = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.turbo], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.turbo], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        BlueCoin("12-6", in_game_bit = 142),
        BlueCoin("12-7", in_game_bit = 143),
    ],
    parent_region = "Menu"
)