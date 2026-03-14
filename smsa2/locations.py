from BaseClasses import Location
from .static_logic import ALL_REGIONS


class Smsa2Location(Location):
    game: str = "Super Mario Sunshine Arcade 2"


ALL_LOCATIONS_TABLE: dict[str, int] = {}

for region in ALL_REGIONS:
    for shine in region.shines:
        ALL_LOCATIONS_TABLE[f"{region.display} - {shine.name}"] = shine.id
    for blue_coin in region.blue_coins:
        ALL_LOCATIONS_TABLE[f"{region.display} - {blue_coin.name} Blue Coin"] = blue_coin.id
