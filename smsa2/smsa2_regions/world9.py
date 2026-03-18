from .smsa2_region_helper import *

WORLD9: Smsa2Region = Smsa2Region(
    Smsa2RegionName.WORLD9,
    ticketed = "World 9 Ticket",
    shines = [
        Shine("9-1 Shine", in_game_bit = 50,
            standard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        Shine("9-2 Shine", in_game_bit = 51,
            standard = Requirements([[NozzleType.hover], [NozzleType.rocket]]),
            hard = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        Shine("9-3 Shine", in_game_bit = 52,
            standard = Requirements([[SPRAY_AND_HOVER], [NozzleType.rocket], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]])),
        Shine("9-4 Shine", in_game_bit = 53,
            standard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]])),
        Shine("9-5 Shine", in_game_bit = 54),
        Shine("9-6 Shine", in_game_bit = 55),
        Shine("9-7 Shine", in_game_bit = 56,
            standard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.spray], [NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        Shine("9-8 Shine", in_game_bit = 57)
    ],
    blue_coins = [
        BlueCoin("9-1", in_game_bit = 471),
        BlueCoin("9-2", in_game_bit = 472),
        BlueCoin("9-3", in_game_bit = 473,
            standard = Requirements([[SPRAY_AND_HOVER], [NozzleType.rocket], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]])),
        BlueCoin("9-4", in_game_bit = 474,
            standard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]])),
        BlueCoin("9-5", in_game_bit = 475),
        BlueCoin("9-6", in_game_bit = 476),
        BlueCoin("9-7", in_game_bit = 477),
        BlueCoin("9-8", in_game_bit = 478),
    ],
    parent_region = "Menu"
)