from .smsa2_region_helper import *

WORLD5: Smsa2Region = Smsa2Region(
    Smsa2RegionName.WORLD5,
    ticketed = "World 5 Ticket",
    shines = [
        Shine("5-1 Shine", in_game_bit = 30),
        Shine("5-2 Shine", in_game_bit = 31),
        Shine("5-3 Shine", in_game_bit = 32),
        Shine("5-4 Shine", in_game_bit = 33),
        Shine("5-5 Shine", in_game_bit = 34,
            standard = Requirements([[NozzleType.hover]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        Shine("5-6 Shine", in_game_bit = 35),
        Shine("5-7 Shine", in_game_bit = 36),
        Shine("5-8 Shine", in_game_bit = 37,
            standard = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]))
    ],
    blue_coins = [
        BlueCoin("5-1", in_game_bit = 321),
        BlueCoin("5-2", in_game_bit = 322),
        BlueCoin("5-3", in_game_bit = 323),
        BlueCoin("5-4", in_game_bit = 324),
        BlueCoin("5-5", in_game_bit = 325,
            standard = Requirements([[NozzleType.hover]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        BlueCoin("5-6", in_game_bit = 326),
        BlueCoin("5-7", in_game_bit = 327),
        BlueCoin("5-8", in_game_bit = 328),
    ],
    parent_region = "Menu"
)