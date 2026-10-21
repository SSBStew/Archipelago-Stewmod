from typing import TYPE_CHECKING

from BaseClasses import Region, CollectionState
from rule_builder import rules


if TYPE_CHECKING:
    from ... import UFO50World




def create_rules(world: "UFO50World", regions: dict[str, Region]) -> None:
    bomb = "Divers - Bomb"
    brelic = "Divers - B relic"
    menu = regions["Menu"]
    shallows = regions["Shallows"]
    ruins = regions["Ruins"]
    slime = regions["Slime"]
    spider = regions["Spider"]
    jelly = regions["Jelly"]
    boss = regions["Boss"]
    sticks = regions["Sticks"]
    mallets = regions["Mallets"]
    lids = regions["Lids"]
    potions = regions["Potions"]
    bombs = regions["Bombs"]
    hasweapons = rules.HasGroup("Divers - Weapons", count=3)
    haspotion = rules.HasGroup("Divers - Potions")
    hasbomb = rules.Has(bomb)
    hasb = rules.Has(brelic)
    malletrule = rules.Has("Divers - Mallets Store Page")
    lidrule = rules.Has("Divers - Lids Store Page")
    potionrule = rules.Has("Divers - Potions Store Page")
    bombrule = rules.Has("Divers - Bombs Store Page")
    slimegate = rules.Has("Divers - Slime Cave Gate")
    northgate = rules.Has("Divers - Ruins North Gate")
    northeastgate = rules.Has("Divers - Ruins Northeast Gate")
    southeastgate = rules.Has("Divers - Ruins Northwest Gate")
    southwestgate = rules.Has("Divers - Ruins Southwest Gate")
    jellygate = northeastgate | southeastgate
    menu.connect(shallows)
    world.create_entrance(shallows, slime, slimegate)
    world.create_entrance(shallows, ruins, northgate)
    world.create_entrance(ruins, spider, southwestgate)
    world.create_entrance(ruins, jelly, jellygate)
    bossgate = rules.Has("Divers - Boss Gate 1") & rules.Has("Divers - Boss Gate 2") & rules.Has("Divers - Mist Orb") & haspotion & hasweapons
    world.create_entrance(jelly, boss, bossgate)
    menu.connect(sticks)
    world.create_entrance(sticks, mallets, malletrule)
    world.create_entrance(sticks, lids, lidrule)
    world.create_entrance(sticks, potions, potionrule)
    world.create_entrance(sticks, bombs, bombrule)
    world.set_rule(world.get_location("Divers - Shallows Bomb Blocked Chest 1"), hasbomb)
    world.set_rule(world.get_location("Divers - Shallows Bomb Blocked Chest 2"), hasbomb)
    world.set_rule(world.get_location("Divers - Piranha Cave Bomb Blocked Chest"), hasbomb)
    world.set_rule(world.get_location("Divers - Holy Potion Store"), hasb)
    temprule = hasweapons & haspotion & northgate
    world.set_rule(world.get_location("Divers - Mist Orb Store"), temprule)
    slimerule = slimegate & hasweapons
    ingotrule = northgate & hasweapons
    crossrule = northgate & southwestgate & hasweapons
    world.set_rule(world.get_location("Divers - Slime Lance Store"), slimerule)
    temprule = slimerule & crossrule
    world.set_rule(world.get_location("Divers - Slime Trident Store"), temprule)
    world.set_rule(world.get_location("Divers - Shell Lance Store"), slimerule)
    world.set_rule(world.get_location("Divers - Shell Trident Store"), crossrule)
    world.set_rule(world.get_location("Divers - Elec Lance Store"), ingotrule)
    world.set_rule(world.get_location("Divers - Elec Trident Store"), crossrule)
    temprule2 = slimerule & ingotrule
    world.set_rule(world.get_location("Divers - Slime Sledge Store"), temprule2)
    world.set_rule(world.get_location("Divers - Shell Sledge Store"), ingotrule)
    world.set_rule(world.get_location("Divers - Elec Sledge Store"), crossrule)
    world.set_rule(world.get_location("Divers - Slime Buckler Store"), slimerule)
    temprule = slimerule & crossrule
    world.set_rule(world.get_location("Divers - Slime Tower Store"), temprule)
    world.set_rule(world.get_location("Divers - Shell Tower Store"), crossrule)
    world.set_rule(world.get_location("Divers - Elec Tower Store"), crossrule)
    world.set_rule(world.get_location("Divers - Holy Potion Store"), crossrule)
    world.set_rule(world.get_location("Divers - Egg Store"), ingotrule)
    hasemblems = rules.Has("Divers - Mooncat Emblem") & rules.Has("Divers - Barbuta Emblem") & rules.Has("Divers - Divers Emblem")
    if "Divers" in world.options.cherry_allowed_games:
        world.set_rule(world.get_location("Divers - Cherry"), hasemblems)
