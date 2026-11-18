from typing import TYPE_CHECKING, NamedTuple, Optional

from BaseClasses import ItemClassification as IC, Item

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class ItemInfo(NamedTuple):
    id_offset: int
    classification: IC
    quantity: int
    group: str

item_table: dict[str, ItemInfo] = {
    #Gear
    "Extra HP": ItemInfo(0, IC.progression, 1, "Gear"),
    "Medkits": ItemInfo(1, IC.progression, 1, "Gear"),
    "Blast Shield": ItemInfo(2, IC.progression, 1, "Gear"),
    "Projectile Shield": ItemInfo(3, IC.progression, 1, "Gear"),
    "Faster Shooting": ItemInfo(4, IC.progression, 1, "Gear"),
    "Power Shot": ItemInfo(5, IC.progression, 1, "Gear"),
    "Spread Shot": ItemInfo(6, IC.progression, 1, "Gear"),
    "Bounce Shot": ItemInfo(7, IC.progression, 1, "Gear"),
    "Push Shot": ItemInfo(8, IC.progression, 1, "Gear"),
    "Drone": ItemInfo(9, IC.progression, 1, "Gear"),
    "Lava Walk": ItemInfo(10, IC.progression, 1, "Gear"),
    "Dash Attack": ItemInfo(11, IC.progression, 1, "Gear"),
    "Extra Bombs": ItemInfo(12, IC.progression, 1, "Gear"),
    "Remote Detonator": ItemInfo(13, IC.progression, 1, "Gear"),
    "Shrapnel Bombs": ItemInfo(14, IC.progression, 1, "Gear"),
    "Bomb Lure": ItemInfo(15, IC.progression, 1, "Gear"),
    #Other
    "Starting Bomb": ItemInfo(20, IC.filler, 3, "Other"),
    "Better Sales": ItemInfo(21, IC.filler, 1, "Other"),
}


# this is for filling out item_name_to_id, it should be static regardless of yaml options
def get_items() -> dict[str, int]:
    return {f"Overbold - {name}": data.id_offset + get_game_base_id("Overbold") for name, data in item_table.items()}


# this should return the item groups for this game, independent of yaml options
def get_item_groups() -> dict[str, set[str]]:
    item_groups: dict[str, set[str]] = {"Overbold": {
        f"Overbold - {item_name}" for item_name in item_table.keys()}}
    item_groups.update({
        "Overbold - Gear": {
            "Overbold - Extra HP",
            "Overbold - Medkits",
            "Overbold - Blast Shield",
            "Overbold - Projectile Shield",
            "Overbold - Faster Shooting",
            "Overbold - Power Shot",
            "Overbold - Spread Shot",
            "Overbold - Bounce Shot",
            "Overbold - Push Shot",
            "Overbold - Drone",
            "Overbold - Lava Walk",
            "Overbold - Dash Attack",
            "Overbold - Extra Bombs",
            "Overbold - Remote Detonator",
            "Overbold - Shrapnel Bombs",
            "Overbold - Bomb Lure"},
    })
    return item_groups


# for when the world needs to create an item at random (like with random filler items)
def create_item(item_name: str, world: "UFO50World", item_class: IC = None) -> Item:
    base_id = get_game_base_id("Overbold")
    if item_name.startswith("Overbold - "):
        item_name = item_name.split(" - ", 1)[1]
    item_data = item_table[item_name]
    return Item(f"Overbold - {item_name}", item_class or item_data.classification,
                base_id + item_data.id_offset, world.player)


# for when the world is getting the items to place into the multiworld's item pool
def create_items(world: "UFO50World") -> list[Item]:
    items_to_create: dict[str, int] = {item_name: data.quantity for item_name, data in item_table.items()}
    overbold_items: list[Item] = []
    for item_name, quantity in items_to_create.items():
        for _ in range(quantity):
            overbold_items.append(create_item(item_name, world))
    return overbold_items


def get_filler_item_name(world: "UFO50World") -> str:
    return "Overbold - Starting Bomb"
