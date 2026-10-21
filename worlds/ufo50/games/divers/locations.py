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
    # Shallows
    "Shallows Piranha Chest": LocationInfo(10, "Shallows"),
    "Shallows Hidden Chest Near Gate": LocationInfo(11, "Shallows"),
    "Shallows Ruins Entrance Chest": LocationInfo(12, "Shallows"),
    "Shallows Bomb Blocked Chest 1": LocationInfo(13, "Shallows"),
    "Shallows Bomb Blocked Chest 2": LocationInfo(14, "Shallows"),
    "Ruins Left of Entrance Chest": LocationInfo(20, "Shallows"),
    "Ruins Center Chest": LocationInfo(21, "Ruins"),
    "Southwest of Ruins Chest": LocationInfo(22, "Spider"),
    "Piranha Cave Bomb Blocked Chest": LocationInfo(23, "Jelly"),
    "Piranha Cave Bottom Right Chest": LocationInfo(24, "Jelly"),
    "Boss Area Chest": LocationInfo(30, "Jelly"),
    "Slime Cave Upper Chest": LocationInfo(40, "Slime"),
    "Slime Cave Lower Chest": LocationInfo(41, "Slime"),
    "Eastern Cave Gift Chest": LocationInfo(50, "Shallows"),
    "Upper Spider Cave Chest": LocationInfo(60, "Spider"),
    "Lower Spider Cave Chest": LocationInfo(61, "Spider"),
    "Jelly Cave Chest": LocationInfo(70, "Jelly"),
    "Shallows Lever": LocationInfo(90, "Shallows"),
    "Ruins North Lever": LocationInfo(91, "Ruins"),
    "Boss Lever 1": LocationInfo(92, "Spider"),
    "Boss Lever 2": LocationInfo(93, "Jelly"),
    "Ruins Northeast Lever": LocationInfo(94, "Jelly"),
    "Ruins Southeast Lever": LocationInfo(95, "Jelly"),
    "Ruins Southwest Lever": LocationInfo(96, "Spider"),
    "Gift Area Emblem": LocationInfo(100, "Shallows"),
    "Slime Cave Emblem": LocationInfo(101, "Slime"),
    "Piranha Cave Emblem": LocationInfo(102, "Jelly"),
    "Slime Stick Store": LocationInfo(110, "Sticks"),
    "Slime Lance Store": LocationInfo(111, "Sticks"),
    "Slime Trident Store": LocationInfo(112, "Sticks"),
    "Shell Stick Store": LocationInfo(113, "Sticks"),
    "Shell Lance Store": LocationInfo(114, "Sticks"),
    "Shell Trident Store": LocationInfo(115, "Sticks"),
    "Elec Stick Store": LocationInfo(116, "Sticks"),
    "Elec Lance Store": LocationInfo(117, "Sticks"),
    "Elec Trident Store": LocationInfo(118, "Sticks"),
    "Slime Mallet Store": LocationInfo(120, "Mallets"),
    "Slime Sledge Store": LocationInfo(121, "Mallets"),
    "Shell Mallet Store": LocationInfo(122, "Mallets"),
    "Shell Sledge Store": LocationInfo(123, "Mallets"),
    "Elec Mallet Store": LocationInfo(124, "Mallets"),
    "Elec Sledge Store": LocationInfo(125, "Mallets"),
    "Slime Lid Store": LocationInfo(130, "Lids"),
    "Slime Buckler Store": LocationInfo(131, "Lids"),
    "Slime Tower Store": LocationInfo(132, "Lids"),
    "Shell Lid Store": LocationInfo(133, "Lids"),
    "Shell Buckler Store": LocationInfo(134, "Lids"),
    "Shell Tower Store": LocationInfo(135, "Lids"),
    "Elec Lid Store": LocationInfo(136, "Lids"),
    "Elec Buckler Store": LocationInfo(137, "Lids"),
    "Elec Tower Store": LocationInfo(138, "Lids"),
    "Small Potion Store": LocationInfo(140, "Potions"),
    "Medium Potion Store": LocationInfo(141, "Potions"),
    "Holy Potion Store": LocationInfo(142, "Potions"),
    "Evil Potion Store": LocationInfo(143, "Potions"),
    "Egg Store": LocationInfo(144, "Potions"),
    "Bomb Store": LocationInfo(150, "Bombs"),
    "Mist Orb Store": LocationInfo(151, "Bombs"),
    "Godblood Store": LocationInfo(152, "Bombs"),
    "Defeat Guelap": LocationInfo(200, "Ruins"),
    "Garden": LocationInfo(997, "Shallows"),
    "Gold": LocationInfo(998, "Boss"),
    "Cherry": LocationInfo(999, "Boss")
}


# this is for filling out location_name_to_id, it should be static regardless of yaml options
def get_locations() -> dict[str, int]:
    return {f"Divers - {name}": data.id_offset + get_game_base_id("Divers") for name, data in location_table.items()}


# this should return the location groups for this game, independent of yaml options
# you should include a group that contains all location for this game that is called the same thing as the game
def get_location_groups() -> dict[str, set[str]]:
    location_groups: dict[str, set[str]] = {"Divers": {f"Divers - {loc_name}" for loc_name in location_table.keys()}}
    return location_groups


# this is not a required function, but a recommended one -- the world class does not call this function
def create_locations(world: "UFO50World", regions: dict[str, Region]) -> None:
    for loc_name, loc_data in location_table.items():
        if loc_name == "Cherry" and "Divers" not in world.options.cherry_allowed_games:
            break
        if loc_name in ["Gold", "Cherry"] and "Divers" in world.goal_games:
            if (loc_name == "Gold" and "Divers" not in world.options.cherry_allowed_games) or loc_name == "Cherry":
                loc = Location(world.player, f"Divers - {loc_name}", None, regions[loc_data.region_name])
                loc.place_locked_item(Item("Completed Divers", ItemClassification.progression, None, world.player))
                add_rule(world.get_location("Completed All Games"), lambda state: state.has("Completed Divers", world.player))
                regions[loc_data.region_name].locations.append(loc)
                break
        loc = Location(world.player, f"Divers - {loc_name}", get_game_base_id("Divers") + loc_data.id_offset,
                       regions[loc_data.region_name])
        regions[loc_data.region_name].locations.append(loc)
