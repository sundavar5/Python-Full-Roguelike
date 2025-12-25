from roguelike.combat import perform_attack
from roguelike.ai_states import AdvancedMonster
from roguelike.status import Stun

def basic_monster_turn(monster, target, game):
    # Check for Stun
    for effect in monster.status_effects:
        if isinstance(effect, Stun):
            return

    if monster.distance_to(target) >= 2:
        # Move towards player
        dx = target.x - monster.x
        dy = target.y - monster.y

        distance = (dx ** 2 + dy ** 2) ** 0.5
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not game.game_map.is_blocked(monster.x + dx, monster.y + dy):
             if not game.get_blocking_entities(monster.x + dx, monster.y + dy):
                 monster.move(dx, dy)
    elif target.fighter.hp > 0:
        perform_attack(monster, target, game, "normal")

def enemy_turn(game):
    for entity in game.entities:
        if entity.ai:
            if isinstance(entity.ai, AdvancedMonster):
                entity.ai.take_turn(entity, game)
            else:
                basic_monster_turn(entity, game.player, game)
