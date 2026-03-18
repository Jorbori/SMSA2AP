from .smsa2_region_helper import *

WORLD2: Smsa2Region = Smsa2Region(
    Smsa2RegionName.WORLD2,
    ticketed = "World 2 Ticket",
    shines = [
        Shine("2-1 Shine", in_game_bit = 0),
        Shine("2-2 Shine", in_game_bit = 1),
        Shine("2-3 Shine", in_game_bit = 2,
            standard = Requirements([[SPRAY_AND_HOVER], [NozzleType.turbo], [NozzleType.bubble]]),
            hard = Requirements([[SPRAY_AND_HOVER], [NozzleType.turbo], [NozzleType.bubble]]),
            expert = Requirements([[SPRAY_AND_HOVER], [NozzleType.turbo], [NozzleType.bubble]])),
        Shine("2-4 Shine", in_game_bit = 3),
        Shine("2-5 Shine", in_game_bit = 4),
        Shine("2-6 Shine", in_game_bit = 5,
            standard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.bubble]])),
        Shine("2-7 Shine", in_game_bit = 6,
            standard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
        Shine("2-8 Shine", in_game_bit = 7,
            standard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]))
    ],
    blue_coins = [
        BlueCoin("2-1", in_game_bit = 171),
        BlueCoin("2-2", in_game_bit = 172),
        BlueCoin("2-3", in_game_bit = 173),
        BlueCoin("2-4", in_game_bit = 174),
        BlueCoin("2-5", in_game_bit = 175),
        BlueCoin("2-6", in_game_bit = 176),
        BlueCoin("2-7", in_game_bit = 177),
        BlueCoin("2-8", in_game_bit = 178,
            standard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]),
            hard = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]]),
            expert = Requirements([[NozzleType.hover], [NozzleType.rocket], [NozzleType.turbo], [NozzleType.bubble]])),
    ],
    parent_region = "Menu"
)