from typing import TYPE_CHECKING

from BaseClasses import Region, CollectionState
from rule_builder import rules
from worlds.generic.Rules import set_rule


if TYPE_CHECKING:
    from ... import UFO50World




def create_rules(world: "UFO50World", regions: dict[str, Region]) -> None:
    player = world.player
    menu = regions["Menu"]
    one = regions["Round 1"]
    two = regions["Round 2"]
    three = regions["Round 3"]
    four = regions["Round 4"]
    five = regions["Round 5"]
    six = regions["Round 6"]
    boss = regions["Boss"]
    # Game is entirely skill based so logic is just based on vibes.
    hasgear3 = rules.HasGroup("Overbold - Gear", count=3)
    hasgear6 = rules.HasGroup("Overbold - Gear", count=6)
    # Extra Bombs are given special treatment because there's important upgrades that are dependent on them.
    hasgear9 = rules.HasGroup("Overbold - Gear", count=9) & rules.Has("Overbold - Extra Bombs")
    hasgear12 = rules.HasGroup("Overbold - Gear", count=12)
    hasgear16 = rules.HasGroup("Overbold - Gear", count=16)
    menu.connect(one)
    one.connect(two)
    world.create_entrance(two, three, hasgear3)
    world.create_entrance(three, four, hasgear6)
    world.create_entrance(four, five, hasgear9)
    world.create_entrance(five, six, hasgear12)
    world.create_entrance(six, boss, hasgear16)
    #could add a hard mode where there's no logic. If we have enough ideas for other options then we'll do them all as a batch.