import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from firefighter import Firefighter
from land_rep import TreePatch
from graph_forrest import GraphInfo
from initialiser import (
    initialise_patches, 
    initialise_neighbours, 
    initialise_color_map
    )

class TestFirefighter(unittest.TestCase):
    def setUp(self):
        self.firefighter = Firefighter(1, 3, 1) # id, power, position
        firefighters = {1: self.firefighter}

        options = {
            "ini_woods" : 100, "ini_fires" : 0, 
            "firefighter_num" : 0, "firefighter_level" : 3
            }
        edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (2, 4), (4, 8)]
        patches =  initialise_patches(edges, None, options)
        color_map = initialise_color_map(patches)
        neighbour_id_register = initialise_neighbours(edges)

        self.graph_info = GraphInfo(
            options, patches, color_map, 
            firefighters, neighbour_id_register
            )

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
        self.graph_info.get_patch(2)._ignite()
        self.firefighter.move()
        self.assertEqual(self.firefighter._position, 2)

    def test_smart_move(self):
        position = self.graph_info.get_patch(1)
        self.graph_info.get_patch(8)._ignite()
        self.firefighter._smart_move(position)
        self.assertEqual(self.firefighter._target.get_id(), 8)
        self.assertEqual(self.firefighter._path, [8, 4]) #first step is poped imidiatly

    def test_find_least_steps(self):
        position = self.graph_info.get_patch(1)
        target = self.graph_info.get_patch(8)
        steps = self.firefighter._find_least_steps(position, target)
        self.assertEqual(steps, 3)


    def test_find_path(self):
        target = self.graph_info.get_patch(8)
        path = self.firefighter._find_path(target, 3)
        self.assertEqual(path, [8, 4, 2])


if __name__ == '__main__':
    unittest.main()