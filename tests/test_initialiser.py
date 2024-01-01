import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, Mock
from initialiser import generate_edges, read_edges, check_connections, initialise_patches, initialise_neighbours, initialise_color_map, initialise_firefighters
from land_rep import TreePatch, RockPatch
import random

class TestInitialiser(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @patch('initialiser.read_edges', return_value=[(1, 2), (2, 3), (3, 1)])
    def test_generate_edges_read(self, mock_read_edges):
        options = {
            "gen_method": "read",
            "edges_file": "test_edges.txt"
        }
        patch('builtins.input', return_value='test_edges.txt').start()
        
        edges, positions = generate_edges(options)

        self.assertEqual(edges, [(1, 2), (2, 3), (3, 1)])
        self.assertIsNone(positions)

    @patch('graph_helper.voronoi_to_edges', return_value=([(1, 2), (2, 3), (3, 1), (4, 5)], {1: (0.1, 0.1), 2: (0.2, 0.2), 3: (0.3, 0.3), 4: (0.4, 0.4)}))
    def test_generate_edges_random(self, mock_voronoi_to_edges):
        options = {
            "gen_method": "random"
        }
        patch('builtins.input', return_value='r').start()
        random.randint = Mock(return_value=5)
        edges, positions = generate_edges(options)

        self.assertEqual(len(edges), 4)
        self.assertEqual(edges, [(1, 2), (2, 3), (3, 1), (4, 5)])
        self.assertIsNotNone(positions)
        
    def test_read_edges(self):
        edges = read_edges("graphs/graph1.dat")
        self.assertEqual(edges, [(0, 1), (1, 2), (2, 3), (3, 0)])
        edges = read_edges("graphs/graph3.dat")
        self.assertEqual(edges, [(1,2), (2,8), (8,1), (6,7)])
        edges = read_edges("graphs/graph4.dat")
        self.assertEqual(edges, [(1, 2), (2, 8), (8, 1)])
        edges = read_edges("graphs/graph5.dat")


    def test_check_connections(self):
        edges = [(1, 2), (2, 3), (3, 1)]
        self.assertTrue(check_connections(edges))
        edges = [(1, 6), (2, 3), (3, 4), (4, 5)]
        self.assertFalse(check_connections(edges))

    def test_initialise_patches(self):
        edges = [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4), (6, 7), (7, 8), (8, 9), (9, 10)]
        positions = None
        options = {
            "ini_woods": 80,
            "ini_fires": 10,
        }
        random.sample = Mock(side_effect = [[x for x in range(8)], [3,7]]) #mocking 2 different results
        patches = initialise_patches(edges, positions, options)

        self.assertEqual(len(patches), 11)
        self.assertEqual(patches.get(1).get_id(), 1)
        for i in range(8):
            self.assertIsInstance(patches.get(i), TreePatch)
        self.assertIsInstance(patches.get(9), RockPatch)
        self.assertIsInstance(patches.get(10), RockPatch)
        self.assertTrue(patches.get(3).is_burning())
        self.assertTrue(patches.get(7).is_burning())


    def test_initialise_neighbours(self):
        edges = [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4), (6, 7), (7, 8), (8, 9)]
        neighbour_id_register = initialise_neighbours(edges)
        self.assertEqual(len(neighbour_id_register), 9)
        self.assertEqual(neighbour_id_register[1], [2, 3])
        self.assertEqual(neighbour_id_register[2], [1, 3])	
        self.assertEqual(neighbour_id_register[3], [2, 1])
        self.assertEqual(neighbour_id_register[4], [5, 6])
        self.assertEqual(neighbour_id_register[5], [4, 6])
        self.assertEqual(neighbour_id_register[6], [5, 4, 7])
        self.assertEqual(neighbour_id_register[7], [6, 8])
        self.assertEqual(neighbour_id_register[8], [7, 9])
        self.assertEqual(neighbour_id_register[9], [8])

    def test_initialise_color_map(self):
        patches = {1: TreePatch(1, 100, True), 2: TreePatch(2, 100, False), 3: TreePatch(3, 100, False), 4: RockPatch(4, 0), 5: TreePatch(5, 100, False)}
        color_map = initialise_color_map(patches)

        self.assertEqual(len(color_map), 4)
        self.assertEqual(color_map.get(1), -25)
        self.assertEqual(color_map.get(2), 100)
        self.assertEqual(color_map.get(3), 100)
        self.assertNotIn(4, color_map)
        self.assertEqual(color_map.get(5), 100)

    def test_initialise_firefighters(self):
        options = {
            "firefighter_level": 3,
            "firefighter_num": 5
        }
        patches = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None}  #We dont need patch obects
        random.sample = Mock(return_value=[1, 2, 3, 4, 5])
        firefighters = initialise_firefighters(patches, options)
        self.assertEqual(len(firefighters), 5)
        self.assertNotIn(0, firefighters)
        self.assertEqual(firefighters[1]._power, 35)
        self.assertTrue(firefighters[1]._brain)
        self.assertNotIn(6, firefighters)
        self.assertNotIn(7, firefighters)
        self.assertNotIn(8, firefighters)


if __name__ == '__main__':
    unittest.main()