from enum import StrEnum
from typing import Optional, NamedTuple, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from worlds.smsa2 import Smsa2World


class Smsa2Location(Location):
    name: str
    address: Optional[int]
    smsa2_region: "Smsa2Region"
    loc_reqs: list["Requirements"]
    goal_level: bool

    def __init__(self, world: "Smsa2World", name: str, parent_region: "Smsa2Region", reqs: list["Requirements"]):
        self.address = world.location_name_to_id[name]
        self.loc_reqs = reqs
        self.smsa2_region = parent_region
        if not reqs:
            self.goal_level = False
        else:
            # Ensure we are looking at Requirements objects, not nested lists
            self.goal_level = any(getattr(loc_req, 'goal_level', False) for loc_req in reqs if not isinstance(loc_req, list))
        if parent_region.requirements:
            self.goal_level = self.goal_level or any(reg_loc.goal_level for reg_loc in parent_region.requirements)
        super(Smsa2Location, self).__init__(world.player, name, address=self.address, parent=world.get_region(parent_region.name))


class Smsa2RegionName(StrEnum):
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


class NozzleType(StrEnum):
    spray = "Spray Nozzle"
    hover = "Hover Nozzle"
    rocket = "Rocket Nozzle"
    turbo = "Turbo Nozzle"
    bubble = "Bubble Nozzle"
    yoshi = "Yoshi"

class Requirements(NamedTuple):
    nozzles: Optional[list[list[str]]] = None  # conjunctive normal form
    shines: Optional[int] = None  # number of shine sprites needed
    blue_coins: Optional[int] = None
    location: Optional[str] = None
    goal_level: bool = False  # is goal_level access needed (configurable)
    skip_forward: bool = None # Only in logic if tickets / fluddless are true


class Shine(NamedTuple):
    name: str
    requirements: Optional[list[Requirements]] | None = None
    standard: Optional[list[Requirements]] | None = None
    hard: Optional[list[Requirements]] | None = None
    expert: Optional[list[Requirements]] | None = None
    in_game_bit: int = None


class BlueCoin(NamedTuple):
    name: str
    requirements: Optional[list[Requirements]] | None = None
    standard: Optional[list[Requirements]] | None = None
    hard: Optional[list[Requirements]] | None = None
    expert: Optional[list[Requirements]] | None = None
    in_game_bit: int = None


class OneUp(NamedTuple):
    name: str
    requirements: Requirements = Requirements()
    standard: Optional[list[Requirements]] | None = None
    hard: Optional[list[Requirements]] | None = None
    expert: Optional[list[Requirements]] | None = None


# Yes, I'm going to include Shadow Mario Plaza chases as NozzleBox Locations
class NozzleBox(NamedTuple):
    name: str
    requirements: Optional[list[Requirements]] | None = None
    standard: Optional[list[Requirements]] | None = None
    hard: Optional[list[Requirements]] | None = None
    expert: Optional[list[Requirements]] | None = None
    in_game_bit: int = None


class Smsa2Region(NamedTuple):
    name: str
    requirements: Optional[list[Requirements]] | None = None
    shines: Optional[list[Shine]] | None = []
    blue_coins: Optional[list[BlueCoin]] | None = []
    nozzle_boxes: Optional[list[NozzleBox]] | None = []
    ticketed: str = ""
    trade: bool = False
    parent_region: str = None

# Common combinations of Nozzle Types
SPRAY_AND_HOVER: list[list[str]] = [
    [NozzleType.spray, NozzleType.hover]
]

SPRAY_AND_TURBO: list[list[str]] = [
    [NozzleType.spray, NozzleType.turbo]
]

SPRAY_AND_ROCKET: list[list[str]] = [
    [NozzleType.spray, NozzleType.rocket]
]

TURBO_AND_HOVER: list[list[str]] = [
    [NozzleType.turbo, NozzleType.hover]
]

TURBO_AND_ROCKET: list[list[str]] = [
    [NozzleType.turbo, NozzleType.rocket]
]

HOVER_AND_ROCKET: list[list[str]] = [
    [NozzleType.hover, NozzleType.rocket]
]

