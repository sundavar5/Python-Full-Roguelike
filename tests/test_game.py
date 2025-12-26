import unittest
from roguelike.game import Game
from roguelike.entities import Entity, Fighter
from roguelike.status import StatusEffect

class MockEffect(StatusEffect):
    def __init__(self, duration):
        super().__init__("MockEffect", duration)
        self.ticked = 0
        self.removed = False

    def tick(self, entity, game):
        self.ticked += 1
        return super().tick(entity, game)

    def remove(self, entity, game):
        self.removed = True
        super().remove(entity, game)

class MockMap:
    def make_map(self, *args):
        pass

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        # Bypass map gen which requires complex init
        self.game.entities = []
        self.player = Entity(0, 0, "Player", "player")
        self.player.status_effects = []
        self.game.entities.append(self.player)

    def test_update_effects(self):
        effect = MockEffect(2)
        self.player.status_effects.append(effect)

        # Turn 1
        self.game.update_effects()
        self.assertEqual(effect.ticked, 1)
        self.assertEqual(effect.duration, 1)
        self.assertFalse(effect.removed)
        self.assertIn(effect, self.player.status_effects)

        # Turn 2
        self.game.update_effects()
        self.assertEqual(effect.ticked, 2)
        self.assertEqual(effect.duration, 0)
        self.assertTrue(effect.removed)
        self.assertNotIn(effect, self.player.status_effects)

if __name__ == '__main__':
    unittest.main()
