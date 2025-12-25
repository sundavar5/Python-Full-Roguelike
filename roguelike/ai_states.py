from roguelike.combat import perform_attack
from roguelike.status import Stun
import random

class AIState:
    def update(self, owner, game):
        pass

class Sleeping(AIState):
    def update(self, owner, game):
        # 10% chance to wake up if player is close
        if owner.distance_to(game.player) < 5:
            if random.random() < 0.1:
                owner.ai_state = Hunting()
                game.add_message(f"{owner.name} wakes up!", (255, 100, 0))

class Wandering(AIState):
    def update(self, owner, game):
        if owner.distance_to(game.player) < 8:
            # If player visible (simple dist check for now), start hunting
            owner.ai_state = Hunting()
            return

        # Move randomly
        dx = random.randint(-1, 1)
        dy = random.randint(-1, 1)
        if dx != 0 or dy != 0:
            if not game.game_map.is_blocked(owner.x + dx, owner.y + dy):
                 if not game.get_blocking_entities(owner.x + dx, owner.y + dy):
                     owner.move(dx, dy)

class Hunting(AIState):
    def update(self, owner, game):
        target = game.player
        if owner.distance_to(target) >= 2:
            # A* or simple move
            dx = target.x - owner.x
            dy = target.y - owner.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))

            if not game.game_map.is_blocked(owner.x + dx, owner.y + dy):
                 if not game.get_blocking_entities(owner.x + dx, owner.y + dy):
                     owner.move(dx, dy)
        elif target.fighter.hp > 0:
            perform_attack(owner, target, game, "normal")

class Fleeing(AIState):
    def update(self, owner, game):
        target = game.player
        # Move away
        dx = owner.x - target.x
        dy = owner.y - target.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance == 0: distance = 1 # avoid div zero
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not game.game_map.is_blocked(owner.x + dx, owner.y + dy):
             if not game.get_blocking_entities(owner.x + dx, owner.y + dy):
                 owner.move(dx, dy)

class AdvancedMonster:
    def __init__(self, start_state=None):
        self.state = start_state if start_state else Wandering()

    def take_turn(self, owner, game):
        # Check Stun
        for effect in owner.status_effects:
            if isinstance(effect, Stun):
                return

        # Check HP for Fleeing
        if owner.fighter.hp < owner.fighter.max_hp * 0.2:
            if not isinstance(self.state, Fleeing):
                self.state = Fleeing()
                game.add_message(f"{owner.name} flees in terror!", (255, 255, 0))

        # Delegate to state (monkey-patching owner.ai_state transition support)
        # Ideally AI class holds state, but state might need to change self.
        # We'll let state return new state or modify owner.ai.state directly if we link it.

        # We need to link owner.ai_state to self.state if we use the classes above which update `owner.ai_state`
        # But `owner.ai` IS this instance. So let's inject `ai_state` property on owner?
        # Or just have this class manage it.

        # Let's adjust classes above to set `owner.ai.state`
        # But for now, let's just implement logic here or pass `self` to update

        if hasattr(owner, 'ai_state'):
             owner.ai_state.update(owner, game)
        else:
             # Init
             owner.ai_state = Wandering()
             owner.ai_state.update(owner, game)
