import unittest
from roguelike.entities import Entity, Fighter
from roguelike.combat import perform_attack
from roguelike.game import Game
from roguelike.ai import FleeingMonster, RangedMonster

class MockGame:
    def __init__(self):
        self.message_log = []
        self.entities = []
        self.player = None
        self.game_map = MockMap()

    def add_message(self, text, color=None):
        self.message_log.append(text)
        print(f"LOG: {text}")

    def get_blocking_entities(self, x, y):
        for entity in self.entities:
            if entity.blocks and entity.x == x and entity.y == y:
                return entity
        return None

class MockMap:
    def is_blocked(self, x, y):
        # Infinite empty plane
        return False

class TestMechanics(unittest.TestCase):
    def setUp(self):
        self.game = MockGame()
        self.attacker = Entity(0, 0, "Attacker", "sprite", blocks=True)
        self.attacker.fighter = Fighter(hp=20, defense=0, power=5, dexterity=10) # 5% crit

        self.target = Entity(1, 0, "Target", "sprite", blocks=True)
        self.target.fighter = Fighter(hp=20, defense=0, power=2, dexterity=10) # 0% dodge (base)

        self.game.entities.append(self.attacker)
        self.game.entities.append(self.target)

    def test_normal_attack(self):
        perform_attack(self.attacker, self.target, self.game, "normal")
        # Base damage 5. 5% crit chance.
        # Assuming no crit.
        # If crit, dmg = int(5 * 1.5) = 7
        # If normal, dmg = 5
        self.assertTrue(self.target.fighter.hp < 20)

    def test_dodge(self):
        # High dexterity target
        self.target.fighter.dexterity = 100 # > 50% dodge? Max is 50%
        # Let's force dodge by seeding or running multiple times, or mocking random?
        # For this test, let's just assert that dodge_chance is calculated correctly
        self.assertEqual(self.target.fighter.dodge_chance, 0.50)

        # Test property calculation
        self.target.fighter.dexterity = 20
        # (20-10)*0.02 = 0.20
        self.assertEqual(self.target.fighter.dodge_chance, 0.20)

    def test_crit_calculation(self):
        self.attacker.fighter.dexterity = 20
        # (20-10)*0.01 + 0.05 = 0.15
        self.assertAlmostEqual(self.attacker.fighter.crit_chance, 0.15)

    def test_stats_scaling(self):
        # Test Strength
        # Power 5, Strength 20 (+10 over 10) -> +5 bonus
        f = Fighter(hp=10, defense=0, power=5, strength=20)
        self.assertEqual(f.power, 10)

        # Test Constitution
        # HP 10, Con 20 (+10 over 10) -> +20 bonus
        f = Fighter(hp=10, defense=0, power=5, constitution=20)
        self.assertEqual(f.max_hp, 30)
        self.assertEqual(f.hp, 30)

    def test_fleeing_ai(self):
        monster = Entity(5, 5, "FleeingMonster", "orc", blocks=True)
        monster.fighter = Fighter(hp=2, defense=0, power=2) # Low HP
        monster.ai = FleeingMonster()

        player = Entity(4, 5, "Player", "player", blocks=True)
        player.fighter = Fighter(hp=10, defense=0, power=10)

        self.game.player = player
        self.game.entities = [monster, player]

        # Monster is at (5,5), Player at (4,5). Monster should move to (6,5)
        monster.ai.take_turn(monster, player, self.game)

        self.assertEqual(monster.x, 6)
        self.assertEqual(monster.y, 5)

    def test_ranged_ai(self):
        monster = Entity(5, 5, "Archer", "skel", blocks=True)
        monster.fighter = Fighter(hp=10, defense=0, power=2)
        monster.ai = RangedMonster()

        player = Entity(5, 7, "Player", "player", blocks=True) # Dist 2

        self.game.player = player

        # Too close (dist 2), should back away
        # Expected: move to (5, 4) (away from 5,7)
        monster.ai.take_turn(monster, player, self.game)

        self.assertEqual(monster.x, 5)
        self.assertEqual(monster.y, 4) # Increased distance

if __name__ == '__main__':
    unittest.main()
