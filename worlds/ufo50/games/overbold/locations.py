from enum import IntEnum
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Region, Location, Item, ItemClassification
from worlds.generic.Rules import add_rule

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World

class LocationInfo(NamedTuple):
    id_offset: int
    region_name: str

location_table: dict[str, LocationInfo] = {
    # Regions on credits won locations are estimates.
    "100 Credits Won": LocationInfo(1, "Round 1"),
    "200 Credits Won": LocationInfo(2, "Round 2"),
    "300 Credits Won": LocationInfo(3, "Round 2"),
    "400 Credits Won": LocationInfo(4, "Round 3"),
    "500 Credits Won": LocationInfo(5, "Round 3"),
    "600 Credits Won": LocationInfo(6, "Round 3"),
    "700 Credits Won": LocationInfo(7, "Round 4"),
    "800 Credits Won": LocationInfo(8, "Round 4"),
    "900 Credits Won": LocationInfo(9, "Round 4"),
    "1000 Credits Won": LocationInfo(10, "Round 5"),
    "1100 Credits Won": LocationInfo(11, "Round 5"),
    "1200 Credits Won": LocationInfo(12, "Round 5"),
    "1300 Credits Won": LocationInfo(13, "Round 6"),
    "1400 Credits Won": LocationInfo(14, "Round 6"),
    "1500 Credits Won": LocationInfo(15, "Round 6"),
    "1600 Credits Won": LocationInfo(16, "Round 6"),
    "Round 1 Won": LocationInfo(21, "Round 1"),
    "Round 2 Won": LocationInfo(22, "Round 2"),
    "Round 3 Won": LocationInfo(23, "Round 3"),
    "Round 4 Won": LocationInfo(24, "Round 4"),
    "Round 5 Won": LocationInfo(25, "Round 5"),
    "Round 6 Won": LocationInfo(26, "Round 6"),
    "Round 7 Won": LocationInfo(27, "Round 6"),
    "Final Fight Won": LocationInfo(28, "Boss"),
    "Garden": LocationInfo(997, "Menu"),
    "Gold": LocationInfo(998, "Boss"),
    "Cherry": LocationInfo(999, "Boss")
}


# this is for filling out location_name_to_id, it should be static regardless of yaml options
def get_locations() -> dict[str, int]:
    return {f"Overbold - {name}": data.id_offset + get_game_base_id("Overbold") for name, data in location_table.items()}


# this should return the location groups for this game, independent of yaml options
# you should include a group that contains all location for this game that is called the same thing as the game
def get_location_groups() -> dict[str, set[str]]:
    location_groups: dict[str, set[str]] = {"Overbold": {f"Overbold - {loc_name}" for loc_name in location_table.keys()}}
    return location_groups


# this is not a required function, but a recommended one -- the world class does not call this function
def create_locations(world: "UFO50World", regions: dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Cherry" and "Overbold" not in world.options.cherry_allowed_games:
            break
        if loc_name in ["Gold", "Cherry"] and "Overbold" in world.goal_games:
            if (loc_name == "Gold" and "Overbold" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Overbold - {loc_name}", None, regions[loc_data.region_name])
                loc.place_locked_item(Item("Completed Overbold", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"), lambda state: state.has("Completed Overbold", world.player))
                regions[loc_data.region_name].locations.append(loc)
                break
        loc = Location(world.player, f"Overbold - {loc_name}", get_game_base_id("Overbold") + loc_data.id_offset,
                       regions[loc_data.region_name])
        regions[loc_data.region_name].locations.append(loc)
