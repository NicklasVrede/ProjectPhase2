import unittest
from firefighter import Firefighter
from land_rep import TreePatch, RockPatch

class TestFirefighter(unittest.TestCase):
    def setUp(self):
        self.firefighter = Firefighter(1, 3, 1)

    def test_initialisation(self):
        self.assertEqual(self.firefighter._id, 1)
        self.assertEqual(self.firefighter._position, 1)
        self.assertEqual(self.firefighter._power, 35)
        self.assertEqual(self.firefighter._brain, True)
        self.assertEqual(self.firefighter._path, [])

    def test_get_position(self):
        position = self.firefighter.get_position()
        self.assertEqual(position, 1)

    def test_extinguish_fire(self):
        firestat = 50
        patch = TreePatch(1, 100, True, None)
        patch._firestat = firestat
        self.firefighter._extinguish_fire(patch)
        self.assertEqual(patch._firestat, firestat-self.firefighter._power)

    def test_move(self):
        # TODO: Implement test cases for the move method
        pass

    def test_smart_move(self):
        # TODO: Implement test cases for the _smart_move method
        pass

    def test_find_least_steps(self):
        # TODO: Implement test cases for the _find_least_steps method
        pass

    def test_find_path(self):
        # TODO: Implement test cases for the _find_path method
        pass

if __name__ == '__main__':
    unittest.main()