from dataclasses import dataclass

from Options import Choice, DeathLink, PerGameCommonOptions, Range, Toggle


class Difficulty(Choice):
    """The difficulty of the randomizer's logic.
    Standard: Logic only requires tricks at a similar level of difficulty to the base game
    Hard: Logic requires some advanced tech and more difficult execution compared to the base game
    Expert: Logic requires glitches and extremely difficult execution"""
    display_name = "Difficulty"
    option_standard = 0
    alias_normal = 0
    alias_medium = 0
    option_hard = 1
    option_expert = 2
    alias_extreme = 2
    alias_salty_tears = 2
    alias_tears = 2
    default = 0

class ShineCount(Range):
    """How many Shine Sprite items appear in the item pool
    If this number of shines is less than the availiable locations, it will be adjusted to the number of availible locations"""
    display_name = "Shine Count"
    range_start = 1
    range_end = 171
    default = 75

class GoalLevelShines(Range):
    """How many Shine Sprites are required to access level 12-8.
    If less than this number of Shines exist in the pool, it will be adjusted to the total Shine count."""
    display_name = "Goal Level Shines"
    range_start = 0
    range_end = 170
    default = 40

class ShineSanity(Toggle):
    """Enables Shine Sprites in the location pool. 
    Note that if Blue Coin Sanity is also disabled, this will be forcefully enabled"""
    display_name = "Shine Sanity"
    default = True

class BlueCoinSanity(Toggle):
    """Enables Blue Coins in the location pool. 
    Note that if this is the only location option selected, you may find yourself saving and qutting the game regularly to exit levels"""
    display_name = "Blue Coin Sanity"

class ShuffleBubbleNozzle(Toggle):
    """Includes the Underwater Hover Nozzle from Noki Bay (called the Bubble Nozzle for brevity) in the item pool.
    When obtained, you can switch to it with D-Pad Up."""
    display_name = "Shuffle Bubble Nozzle"

class ShuffleLongJump(Toggle):
    """Includes the Long Jump move in the item pool.
    Use it by holding Z and pressing A while moving."""
    display_name = "Shuffle Long Jump"

class ShuffleFruitGummies(Toggle):
    """Includes the Fruit Gummies in the item pool.
    Fruit Gummies allow Yoshi eggs to be hatched without bringing them fruit.
    However, Yoshi will not be able to spray juice without eating an actual fruit."""

class ShuffleDiveHelmet(Toggle):
    """Includes the Dive Helmet in the item pool."""
    display_name = "Shuffle Dive Helmet"

class ShuffleSunglasses(Toggle):
    """Includes the Suglasses in the item pool."""
    display_name = "Shuffle Sunglasses"

class ShuffleShineShirt(Toggle):
    """Includes the Shine Shirt in the item pool."""
    display_name = "Shuffle Shine Shirt"

class ShuffleCap(Toggle):
    """Strips Mario's Cap and includes it in the item pool.
    This is only a visual change""" #- the overheating functionality is tied to shuffle_sunscreen

@dataclass
class Smsa2Options(PerGameCommonOptions):
    difficulty: Difficulty
    shine_count: ShineCount
    goal_level_shines: GoalLevelShines
    shine_sanity: ShineSanity
    blue_coin_sanity: BlueCoinSanity
    shuffle_bubble_nozzle: ShuffleBubbleNozzle
    shuffle_long_jump: ShuffleLongJump
    shuffle_fruit_gummies: ShuffleFruitGummies
    shuffle_dive_helmet: ShuffleDiveHelmet
    shuffle_sunglasses: ShuffleSunglasses
    shuffle_shine_shirt: ShuffleShineShirt
    shuffle_cap: ShuffleCap
    death_link: DeathLink
