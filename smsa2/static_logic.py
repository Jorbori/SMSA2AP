from enum import Flag, auto
from typing import Optional, NamedTuple

WORLD1 = "Delfino Plaza"
WORLD2 = "Bianco Hills"
WORLD3 = "Ricco Harbor"
WORLD4 = "Gelato Beach"
WORLD5 = "Pinna Park"
WORLD6 = "Night World"
WORLD7 = "Delfino Hotel"
WORLD8 = "Pianta Village"
WORLD9 = "Noki Bay"
WORLD10 = "Deep Deep Sea"
WORLD11 = "Corona Mountain"
WORLD12 = "Bonus World"
GOAL = "Goal Level"

class NozzleType(Flag):
    none = auto()
    spray = auto()
    hover = auto()
    rocket = auto()
    turbo = auto()
    sprayandhover = auto()
    sprayandturbo = auto()
    sprayandrocket = auto()
    turboandhover = auto()
    turboandrocket = auto()
    hoverandrocket = auto()
    bubble = auto()

class Requirements(NamedTuple):
    nozzles: list[NozzleType] = []  # conjunctive normal form
    shines: Optional[int] = None  # number of shine sprites needed
    corona: bool = False  # is corona access needed (configurable)
    blues: int = 0
    location: str = ""


class Shine(NamedTuple):
    name: str
    id: int
    standard: Requirements = Requirements()
    hard: Requirements = Requirements()
    expert: Requirements = Requirements()


class BlueCoin(NamedTuple):
    name: str
    id: int
    standard: Requirements = Requirements()
    hard: Requirements = Requirements()
    expert: Requirements = Requirements()
    available: [int] = []


class Smsa2Region(NamedTuple):
    name: str
    display: str
    requirements: Requirements = Requirements()
    shines: list[Shine] = []
    blue_coins: list[BlueCoin] = []
    ticketed: str = ""
    parent_region: str = "Menu"
    skipped: bool = False


ALL_REGIONS: list[Smsa2Region] = [
    # World 1 - Deflino Plaza
    Smsa2Region(WORLD1, WORLD1, Requirements(),
        [
            Shine("1-1 Shine", 523086),
            Shine("1-2 Shine", 523087),
            Shine("1-3 Shine", 523088, 
                  standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            Shine("1-4 Shine", 523089, 
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]), 
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            Shine("1-5 Shine", 523090),
            #Shine("1-6 Shine", 523091, 
            #    standard = Requirements([NozzleType.spray | NozzleType.hover]), 
            #    hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo]), 
            #    expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo])),
            Shine("1-7 Shine", 523092, 
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]), 
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            #Shine("1-8 Shine", 523093, 
            #    standard = Requirements([NozzleType.hover | NozzleType.bubble]), 
            #    hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]))
        ], [
            BlueCoin("1-1", 523121),
            BlueCoin("1-2", 523122),
            BlueCoin("1-3", 523123, 
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]), 
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("1-4", 523124, 
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            BlueCoin("1-5", 523125),
            #BlueCoin("1-6", 523126),
            BlueCoin("1-7", 523127, 
                standard = Requirements([NozzleType.rocket | NozzleType.bubble]), 
                hard = Requirements([NozzleType.rocket | NozzleType.turboandhover | NozzleType.bubble]), 
                expert = Requirements([NozzleType.rocket | NozzleType.turboandhover | NozzleType.sprayandturbo | NozzleType.bubble])),
            #BlueCoin("1-8", 523128, 
            #    standard = Requirements([NozzleType.hover]), 
            #    hard = Requirements([NozzleType.hover | NozzleType.rocket]), 
            #    expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo])),
        ], ticketed = "World 1 Ticket"),
    
    # World 2 - Bianco Hills
    Smsa2Region(WORLD2, WORLD2, Requirements(),
        [
            Shine("2-1 Shine", 523000),
            Shine("2-2 Shine", 523001),
            Shine("2-3 Shine", 523002,
                standard = Requirements([NozzleType.sprayandhover | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.sprayandhover | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.sprayandhover | NozzleType.turbo | NozzleType.bubble])),
            Shine("2-4 Shine", 523003),
            Shine("2-5 Shine", 523004),
            Shine("2-6 Shine", 523005,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            Shine("2-7 Shine", 523006,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("2-8 Shine", 523007,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]))
        ], [
            BlueCoin("2-1", 523171),
            BlueCoin("2-2", 523172),
            BlueCoin("2-3", 523173),
            BlueCoin("2-4", 523174),
            BlueCoin("2-5", 523175),
            BlueCoin("2-6", 523176),
            BlueCoin("2-7", 523177),
            BlueCoin("2-8", 523178,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
        ], ticketed = "World 2 Ticket"),

    # World 3 - Ricco Harbor
    Smsa2Region(WORLD3, WORLD3, Requirements(),
        [
            Shine("3-1 Shine", 523010,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("3-2 Shine", 523011,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("3-3 Shine", 523012),
            Shine("3-4 Shine", 523013,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("3-5 Shine", 523014,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("3-6 Shine", 523015,
                standard = Requirements([NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.rocket | NozzleType.bubble])),
            Shine("3-7 Shine", 523016,
                standard = Requirements([NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("3-8 Shine", 523017,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]))
        ], [
            BlueCoin("3-1", 523221,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            BlueCoin("3-2", 523222,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("3-3", 523223),
            BlueCoin("3-4", 523224,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("3-5", 523225,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("3-6", 523226),
            BlueCoin("3-7", 523227),
            BlueCoin("3-8", 523228,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
        ], ticketed = "World 3 Ticket"),
    
    # World 4 - Gelato Beach
    Smsa2Region(WORLD4, WORLD4, Requirements(),
        [
            Shine("4-1 Shine", 523020,
                standard = Requirements([NozzleType.turbo]),
                hard = Requirements([NozzleType.turbo]),
                expert = Requirements([NozzleType.turbo])),
            Shine("4-2 Shine", 523021),
            Shine("4-3 Shine", 523022),
            Shine("4-4 Shine", 523023,
                standard = Requirements([NozzleType.hover | NozzleType.sprayandrocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.sprayandrocket | NozzleType.turboandrocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            Shine("4-5 Shine", 523024,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("4-6 Shine", 523025),
            Shine("4-7 Shine", 523026,
                standard = Requirements([NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.rocket | NozzleType.bubble])),
            Shine("4-8 Shine", 523027,
                standard = Requirements([NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.rocket | NozzleType.hover | NozzleType.bubble]),
                expert = Requirements([NozzleType.rocket | NozzleType.hover | NozzleType.bubble]))
        ], [
            BlueCoin("4-1", 523271),
            BlueCoin("4-2", 523272),
            BlueCoin("4-3", 523273),
            BlueCoin("4-4", 523274,
                standard = Requirements([NozzleType.hover | NozzleType.sprayandrocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.sprayandrocket | NozzleType.turboandrocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            BlueCoin("4-5", 523275,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            BlueCoin("4-6", 523276),
            BlueCoin("4-7", 523277),
            BlueCoin("4-8", 523278,
                standard = Requirements([NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.rocket | NozzleType.hover | NozzleType.bubble]),
                expert = Requirements([NozzleType.rocket | NozzleType.hover | NozzleType.bubble])),
        ], ticketed = "World 4 Ticket"),
    
    # World 5 - Pinna Park
    Smsa2Region(WORLD5, WORLD5, Requirements(),
        [
            Shine("5-1 Shine", 523030),
            Shine("5-2 Shine", 523031),
            Shine("5-3 Shine", 523032),
            Shine("5-4 Shine", 523033),
            Shine("5-5 Shine", 523034,
                standard = Requirements([NozzleType.hover]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("5-6 Shine", 523035),
            Shine("5-7 Shine", 523036),
            Shine("5-8 Shine", 523037,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]))
        ], [
            BlueCoin("5-1", 523321),
            BlueCoin("5-2", 523322),
            BlueCoin("5-3", 523323),
            BlueCoin("5-4", 523324),
            BlueCoin("5-5", 523325,
                standard = Requirements([NozzleType.hover]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("5-6", 523326),
            BlueCoin("5-7", 523327),
            BlueCoin("5-8", 523328),
        ], ticketed = "World 5 Ticket"),
    
    # World 6 - Night World
    Smsa2Region(WORLD6, WORLD6, Requirements(),
        [
            Shine("6-1 Shine", 523040,
                standard = Requirements([NozzleType.hover]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("6-2 Shine", 523041,
                standard = Requirements([NozzleType.hover]),
                hard = Requirements([NozzleType.spray | NozzleType.hover]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble])),
            Shine("6-3 Shine", 523042),
            Shine("6-4 Shine", 523043),
            Shine("6-5 Shine", 523044,
                standard = Requirements([NozzleType.hover | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("6-6 Shine", 523045,
                standard = Requirements([NozzleType.hover | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.bubble])),
            Shine("6-7 Shine", 523046),
            Shine("6-8 Shine", 523047,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]))
        ], [
            BlueCoin("6-1", 523371,
                standard = Requirements([NozzleType.hover]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("6-2", 523372,
                standard = Requirements([NozzleType.hover | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("6-3", 523373),
            BlueCoin("6-4", 523374),
            BlueCoin("6-5", 523375),
            BlueCoin("6-6", 523376,
                standard = Requirements([NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("6-7", 523377),
            BlueCoin("6-8", 523378),
        ], ticketed = "World 6 Ticket"),
    
    # World 7 - Delfino Hotel
    Smsa2Region(WORLD7, WORLD7, Requirements(),
        [
            Shine("7-1 Shine", 523008,
                standard = Requirements([NozzleType.hover | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.sprayandturbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.turbo | NozzleType.sprayandrocket | NozzleType.bubble])),
            Shine("7-2 Shine", 523009,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble])),
            Shine("7-3 Shine", 523018,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("7-4 Shine", 523019,
                standard = Requirements([NozzleType.sprayandrocket | NozzleType.hoverandrocket]),
                hard = Requirements([NozzleType.sprayandrocket | NozzleType.hoverandrocket | NozzleType.turboandrocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.sprayandrocket | NozzleType.hoverandrocket | NozzleType.turboandrocket | NozzleType.bubble])),
            Shine("7-5 Shine", 523028,
                standard = Requirements([NozzleType.hover | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("7-6 Shine", 523029),
            Shine("7-7 Shine", 523038),
            Shine("7-8 Shine", 523039)
        ], [
            BlueCoin("7-1", 523379,
                standard = Requirements([NozzleType.hover]),
                hard = Requirements([NozzleType.hover | NozzleType.sprayandturbo | NozzleType.sprayandrocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.sprayandturbo | NozzleType.bubble])),
            BlueCoin("7-2", 523380),
            BlueCoin("7-3", 523381),
            BlueCoin("7-4", 523382,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("7-5", 523383,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("7-6", 523384,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("7-7", 523385),
            BlueCoin("7-8", 523386),
        ], ticketed = "World 7 Ticket"),
    
    # World 8 - Pianta Village
    Smsa2Region(WORLD8, WORLD8, Requirements(),
        [
            Shine("8-1 Shine", 523060),
            Shine("8-2 Shine", 523061,
                standard = Requirements([NozzleType.hover | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("8-3 Shine", 523062),
            Shine("8-4 Shine", 523063),
            Shine("8-5 Shine", 523064),
            Shine("8-6 Shine", 523065),
            Shine("8-7 Shine", 523066),
            Shine("8-8 Shine", 523067)
        ], [
            BlueCoin("8-1", 523421),
            BlueCoin("8-2", 523422,
                standard = Requirements([NozzleType.hover | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("8-3", 523423),
            BlueCoin("8-4", 523424),
            BlueCoin("8-5", 523425),
            BlueCoin("8-6", 523426),
            BlueCoin("8-7", 523427),
            BlueCoin("8-8", 523428),
        ], ticketed = "World 8 Ticket"),
    
    # World 9 - Noki Bay
    Smsa2Region(WORLD9, WORLD9, Requirements(),
        [
            Shine("9-1 Shine", 523050,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("9-2 Shine", 523051,
                standard = Requirements([NozzleType.hover | NozzleType.rocket]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("9-3 Shine", 523052,
                standard = Requirements([NozzleType.sprayandhover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            Shine("9-4 Shine", 523053,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            Shine("9-5 Shine", 523054),
            Shine("9-6 Shine", 523055),
            Shine("9-7 Shine", 523056,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("9-8 Shine", 523057)
        ], [
            BlueCoin("9-1", 523471),
            BlueCoin("9-2", 523472),
            BlueCoin("9-3", 523473,
                standard = Requirements([NozzleType.sprayandhover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            BlueCoin("9-4", 523474,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble])),
            BlueCoin("9-5", 523475),
            BlueCoin("9-6", 523476),
            BlueCoin("9-7", 523477),
            BlueCoin("9-8", 523478),
        ], ticketed = "World 9 Ticket"),
    
    # World 10 - Deep Deep Sea
    Smsa2Region(WORLD10, WORLD10, Requirements(),
        [
            Shine("10-1 Shine", 523048),
            Shine("10-2 Shine", 523049),
            Shine("10-3 Shine", 523058,
                standard = Requirements([NozzleType.turbo]),
                hard = Requirements([NozzleType.turbo]),
                expert = Requirements([NozzleType.turbo])),
            Shine("10-4 Shine", 523059),
            Shine("10-5 Shine", 523068),
            Shine("10-6 Shine", 523069),
            Shine("10-7 Shine", 523094),
            Shine("10-8 Shine", 523095)
        ], [
            BlueCoin("10-1", 523521),
            BlueCoin("10-2", 523522),
            BlueCoin("10-3", 523523),
            BlueCoin("10-4", 523524),
            BlueCoin("10-5", 523525),
            BlueCoin("10-6", 523526),
            BlueCoin("10-7", 523527),
            BlueCoin("10-8", 523528),
        ], ticketed = "World 10 Ticket"),
    
    # World 11 - Corona Mountain
    Smsa2Region(WORLD11, WORLD11, Requirements(),
        [
            Shine("11-1 Shine", 523096,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("11-2 Shine", 523097,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("11-3 Shine", 523098,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("11-4 Shine", 523099,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("11-5 Shine", 523100),
            Shine("11-6 Shine", 523101,
                standard = Requirements([NozzleType.hover | NozzleType.bubble])),
            Shine("11-7 Shine", 523102,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("11-8 Shine", 523103,
                standard = Requirements([NozzleType.hover]),
                hard = Requirements([NozzleType.hover | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]))
        ], [
            BlueCoin("11-1", 523129,
                standard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("11-2", 523130),
            BlueCoin("11-3", 523131,
                standard = Requirements([NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.rocket | NozzleType.turboandhover | NozzleType.bubble]),
                expert = Requirements([NozzleType.rocket | NozzleType.turboandhover | NozzleType.bubble])),
            BlueCoin("11-4", 523132,
                standard = Requirements([NozzleType.rocket | NozzleType.bubble]),
                hard = Requirements([NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.rocket | NozzleType.sprayandturbo | NozzleType.bubble])),
            BlueCoin("11-5", 523133),
            BlueCoin("11-6", 523134),
            BlueCoin("11-7", 523135),
            BlueCoin("11-8", 523136,
                standard = Requirements([NozzleType.hover]),
                hard = Requirements([NozzleType.hover | NozzleType.rocket | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
        ], ticketed = "World 11 Ticket"),
    
    # World 12 - Bonus World
    Smsa2Region(WORLD12, WORLD12, Requirements(),
        [
            Shine("12-1 Shine", 523104),
            Shine("12-2 Shine", 523105,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            Shine("12-3 Shine", 523106),
            Shine("12-4 Shine", 523107),
            Shine("12-5 Shine", 523116,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.bubble])),
            Shine("12-6 Shine", 523117),
            Shine("12-7 Shine", 523118)#,
            #Shine("12-8 Shine", 523119)
        ], [
            BlueCoin("12-1", 523137),
            BlueCoin("12-2", 523138),
            BlueCoin("12-3", 523139),
            BlueCoin("12-4", 523140),
            BlueCoin("12-5", 523141,
                standard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                hard = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.turbo | NozzleType.bubble]),
                expert = Requirements([NozzleType.spray | NozzleType.hover | NozzleType.rocket | NozzleType.turbo | NozzleType.bubble])),
            BlueCoin("12-6", 523142),
            BlueCoin("12-7", 523143),
            
        ], ticketed = "World 12 Ticket"),

    Smsa2Region(GOAL, GOAL, Requirements(corona=True),
        [
        ],
        [
            BlueCoin("12-8", 523144),
        ],)
]
