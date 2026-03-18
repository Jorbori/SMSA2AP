from .smsa2_region_helper import *

WORLD8: Smsa2Region = Smsa2Region(
    Smsa2RegionName.WORLD8,
    ticketed = "World 8 Ticket",
    shines = [
        Shine("8-1 Shine", in_game_bit = 60),
        Shine("8-2 Shine", in_game_bit = 61,
            standard = Requirements([[NozzleType.hover], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        Shine("8-3 Shine", in_game_bit = 62),
        Shine("8-4 Shine", in_game_bit = 63),
        Shine("8-5 Shine", in_game_bit = 64),
        Shine("8-6 Shine", in_game_bit = 65),
        Shine("8-7 Shine", in_game_bit = 66),
        Shine("8-8 Shine", in_game_bit = 67)
    ],
    blue_coins = [
        BlueCoin("8-1", in_game_bit = 421),
        BlueCoin("8-2", in_game_bit = 422,
            standard = Requirements([[NozzleType.hover], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        BlueCoin("8-3", in_game_bit = 423),
        BlueCoin("8-4", in_game_bit = 424),
        BlueCoin("8-5", in_game_bit = 425),
        BlueCoin("8-6", in_game_bit = 426),
        BlueCoin("8-7", in_game_bit = 427),
        BlueCoin("8-8", in_game_bit = 428),
    ],
    parent_region = "Menu"
)