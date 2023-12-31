import unittest
from unittest.mock import MagicMock, patch

import sys
sys.path.append('')

from your_package.modules import your_module

from land_rep import TreePatch, RockPatch
from firefighter import Firefighter
from graph_forrest import GraphInfo

class TestTreePatch(unittest.TestCase):
    def setUp(self):
        options = {"growth_rate": 10, "burn_rate": 20, "fire_spread_rate": 30, "new_forrest_probability": 100}
        self.patch = TreePatch(1, 100)
        patches = {1: self.patch, 2: RockPatch(2, 0), 3: TreePatch(3, 100)}
        color_map = {1: 100, 3: 100}
        firefighters = {1: Firefighter(1, 3, 1), 2: Firefighter(2, 3, 2)}
        neighbour_id_register = {1: [2, 3], 2: [1, 3], 3: [2, 1]}
        self.graph_info = GraphInfo(options, patches, color_map, firefighters, neighbour_id_register)
        

    def test_get_color(self):
        self.assertEqual(self.patch.get_color(), 100)
        self.patch._ignite()
        self.patch._firestat = 100
        self.assertEqual(self.patch.get_color(), -256)

    def test_update_color(self):
        self.graph_info.update_color(1, 42)
        self.assertEqual(self.graph_info.get_color_map().get(1), 42)

    def test_reduce_firestat(self):
        self.patch._ignite()
        self.assertEqual(self.patch._firestat, 10)
        self.patch.reduce_firestat(10)
        self.assertTrue(self.patch._burning)
        self.assertEqual(self.patch._firestat, 0)

    def test_ignite(self):
        self.patch._ignite()
        self.assertTrue(self.patch._burning)
        self.assertEqual(self.patch._firestat, 10)

    def test_spread_fire(self):
        neighbour_mock = MagicMock()
        self.patch.get_neighbours = MagicMock(return_value=[neighbour_mock]) #mocking get_neighbours

        #Mock random.randint to 1:  #does this work as intended?
        with patch('random.randint') as randint_mock:  #patch from unittest.mock!
            randint_mock.return_value = 1
            self.patch._spread_fire()
            self.assertTrue(neighbour_mock._burning)

    def test_evolve_firestat(self):
        self.patch._ignite()
        self.assertEqual(self.patch._firestat, 10)
        self.patch._evolve_firestat()
        self.assertEqual(self.patch._firestat, 21.0)
        for _ in range(10):
            self.patch._evolve_firestat()
        self.assertEqual(self.patch._firestat, 100)
        self.assertEqual(self.patch.get_color(), -256)

    def test_evolve_treestat(self):
        self.patch._burning = True
        self.patch._evolve_treestat()
        self.assertEqual(self.patch._treestat, 80)
        for _ in range(10):
            self.patch._evolve_treestat()
        self.assertIsInstance(self.graph_info.get_patch(1), RockPatch)

    def test_spread_forrest(self):
        with patch('random.randint') as randint_mock:
            randint_mock.return_value = 1
            self.patch._spread_forrest()
            self.assertIsInstance(self.graph_info.get_patch(2), TreePatch)

    def test_updateland(self):
        self.patch.updateland()
        self.assertEqual(self.patch._treestat, 110)
        self.patch._ignite()
        self.patch.updateland()
        self.assertEqual(self.patch._treestat, 90)

    def test_mutate(self):
        self.patch._mutate()
        self.assertIsInstance(self.graph_info.get_patch(1), RockPatch)
        self.assertFalse(self.graph_info.get_patch(1)._burning)

if __name__ == '__main__':
    unittest.main()