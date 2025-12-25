from roguelike.config import COLOR_GREEN, COLOR_RED

class StatusEffect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.max_duration = duration

    def apply(self, entity, game):
        # Called once when applied
        game.add_message(f"{entity.name} is affected by {self.name}!", COLOR_RED)

    def tick(self, entity, game):
        # Called every turn
        self.duration -= 1
        return self.duration <= 0

    def remove(self, entity, game):
        # Called when expired
        game.add_message(f"{self.name} wears off {entity.name}.", COLOR_GREEN)

class Poison(StatusEffect):
    def __init__(self, duration, damage):
        super().__init__("Poison", duration)
        self.damage = damage

    def tick(self, entity, game):
        if entity.fighter:
            entity.fighter.take_damage(self.damage)
            game.add_message(f"{entity.name} takes {self.damage} poison damage.", (100, 255, 100))
            if entity.fighter.hp <= 0:
                 # Handle death externally usually, or here
                 from roguelike.combat import kill_entity
                 kill_entity(game.player, entity, game) # Assuming player source for now? Or env
        return super().tick(entity, game)

class Regen(StatusEffect):
    def __init__(self, duration, amount):
        super().__init__("Regeneration", duration)
        self.amount = amount

    def tick(self, entity, game):
        if entity.fighter:
            entity.fighter.heal(self.amount)
        return super().tick(entity, game)

class Stun(StatusEffect):
    def __init__(self, duration):
        super().__init__("Stun", duration)

    # Stun logic needs to be checked in AI/Input handling
