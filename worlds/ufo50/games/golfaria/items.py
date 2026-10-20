from typing import TYPE_CHECKING, NamedTuple, Optional

from BaseClasses import ItemClassification as IC, Item

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class ItemInfo(NamedTuple):
    id_offset: int
    classification: IC
    quantity: int

item_table: dict[str, ItemInfo] = {
    "Club": ItemInfo(0, IC.progression, 20),
    "Scorecard": ItemInfo(1, IC.filler, 0),
    "Pencil": ItemInfo(2, IC.filler, 0),
    "Driver": ItemInfo(3, IC.filler, 0),
    "Parbot": ItemInfo(20, IC.filler, 10),
    "Tee 1": ItemInfo(30, IC.progression, 1),
    "Tee 2": ItemInfo(31, IC.progression, 1),
    "Tee 3": ItemInfo(32, IC.progression, 1),
    "Tee 4": ItemInfo(33, IC.progression, 1),
    "Temple North NPC": ItemInfo(40, IC.progression, 1),
    "Temple East NPC": ItemInfo(41, IC.progression, 1),
    "Desert Cave NPC": ItemInfo(42, IC.progression, 1),
    "Water Save Cave NPC": ItemInfo(43, IC.progression, 1),
    "Water Cave NPC": ItemInfo(44, IC.progression, 1),
    "Lake Center NPC": ItemInfo(45, IC.progression, 1),
    "Im Lost NPC": ItemInfo(46, IC.progression, 1),
    "Sandman NPC": ItemInfo(47, IC.progression, 1),
    "Brakes": ItemInfo(50, IC.progression, 1),
    "Block Buster": ItemInfo(51, IC.progression, 1),
    "Water Roll": ItemInfo(52, IC.progression, 1),
    "Sand Roll": ItemInfo(53, IC.progression, 1),
    "Wise Ball's Cave Checkpoint": ItemInfo(101, IC.progression, 1),
    "Calm Cave Checkpoint": ItemInfo(102, IC.progression, 1),
    "Gur Grotto Checkpoint": ItemInfo(103, IC.progression, 1),
    "Rooted Route Checkpoint": ItemInfo(104, IC.progression, 1),
    "Tee Temple Checkpoint": ItemInfo(105, IC.progression, 1),
    "Cave Town Checkpoint": ItemInfo(106, IC.progression, 1),
    "Downswing Dip Checkpoint": ItemInfo(107, IC.progression, 1),
    "Winding Wetway Checkpoint": ItemInfo(108, IC.progression, 1),
    "Bunker Below Checkpoint": ItemInfo(109, IC.progression, 1),
}

# this is for filling out item_name_to_id, it should be static regardless of yaml options
def get_items() -> dict[str, int]:
    return {f"Golfaria - {name}": data.id_offset + get_game_base_id("Golfaria") for name, data in item_table.items()}


# this should return the item groups for this game, independent of yaml options
def get_item_groups() -> dict[str, set[str]]:
    item_groups: dict[str, set[str]] = {"Golfaria": {f"Golfaria - {item_name}" for item_name in item_table.keys()}}
    return item_groups


# for when the world needs to create an item at random (like with random filler items)
def create_item(item_name: str, world: "UFO50World", item_class: IC = None) -> Item:
    base_id = get_game_base_id("Golfaria")
    if item_name.startswith("Golfaria - "):
        item_name = item_name.split(" - ", 1)[1]
    item_data = item_table[item_name]
    return Item(f"Golfaria - {item_name}", item_class or item_data.classification,
                base_id + item_data.id_offset, world.player)


# for when the world is getting the items to place into the multiworld's item pool
def create_items(world: "UFO50World") -> list[Item]:
    items_to_create: dict[str, int] = {item_name: data.quantity for item_name, data in item_table.items()}
    if world.options.golfaria_start_brakes:
        items_to_create["Brakes"] = 0
    golfaria_items: list[Item] = []
    for item_name, quantity in items_to_create.items():
        for _ in range(quantity):
            golfaria_items.append(create_item(item_name, world))
    return golfaria_items


def get_filler_item_name(world: "UFO50World") -> str:
    return world.random.choice(["Golfaria - Scorecard", "Golfaria - Pencil", "Golfaria - Driver"])
