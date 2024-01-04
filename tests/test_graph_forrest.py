import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock
from graph_forrest import GraphInfo
from firefighter import Firefighter
from land_rep import TreePatch, RockPatch

class TestGraphInfo(unittest.TestCase):
    def setUp(self):  #Run for each method test.
        options = {"option1": 1, "option2": 2}
        patches = {1: TreePatch(1, 100), 2: RockPatch(2, 0), 3: TreePatch(3, 100)}
        color_map = {1: 100, 3: 100}
        firefighters = {1: Firefighter(1, 3, 1), 2: Firefighter(2, 3, 2)}
        neighbour_id_register = {1: [2, 3], 2: [1, 3], 3: [2, 1]}
        self.graph_info = GraphInfo(
            options, patches, color_map, 
            firefighters, neighbour_id_register
            )

    def test_get_patch(self):
        patch = self.graph_info.get_patch(1)
        self.assertIsInstance(patch, TreePatch)
        self.assertEqual(patch.get_id(), 1)

    def test_get_patches(self):
        patches = self.graph_info.get_patches()
        self.assertIsInstance(patches, dict)
        self.assertEqual(len(patches), 3)
        self.assertIsInstance(patches[1], TreePatch)
        self.assertIsInstance(patches[2], RockPatch)
        self.assertIsInstance(patches[3], TreePatch)

    def test_update_patch(self):
        patch = RockPatch(3, 0, self.graph_info)
        self.graph_info.update_patch(patch)
        updated_patch = self.graph_info.get_patch(3)
        self.assertEqual(updated_patch.get_id(), 3)
        self.assertIsInstance(updated_patch, RockPatch)

    def test_get_neighbours_ids(self):
        neighbours = self.graph_info.get_neighbours_ids(1)
        self.assertIsInstance(neighbours, list)
        self.assertEqual(len(neighbours), 2)
        self.assertIn(2, neighbours)
        self.assertIn(3, neighbours)

    def test_update_color(self):
        self.graph_info.update_color(3, -100)
        color_map = self.graph_info.get_color_map()
        self.assertEqual(len(color_map), 2)
        self.assertEqual(color_map[3], -100)

    def test_remove_color(self):
        self.assertEqual(len(self.graph_info.get_color_map()), 2)
        self.graph_info.remove_color(3)
        self.assertEqual(len(self.graph_info.get_color_map()), 1)

    def test_get_color_map(self):
        color_map = self.graph_info.get_color_map()
        self.assertIsInstance(color_map, dict)
        self.assertEqual(len(color_map), 2)
        self.assertEqual(color_map[1], 100)
        self.assertEqual(color_map[3], 100)

    def test_get_firefighter_positions(self):
        positions = self.graph_info.get_firefighter_positions()
        self.assertIsInstance(positions, list)
        self.assertEqual(len(positions), 2)
        self.assertIn(1, positions)
        self.assertIn(2, positions)

    def test_activate_firefighters(self):
        self.held = Firefighter.move
        Firefighter.move = Mock(return_value=None)
        self.graph_info.activate_firefighters()
        self.assertEqual(Firefighter.move.call_count, len(self.graph_info._firefighters.keys()))

        #undo changes
        Firefighter.move = self.held
if __name__ == '__main__':
    unittest.main()