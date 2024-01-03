import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock
from initialiser import generate_edges, read_edges, check_connections, initialise_patches, initialise_neighbours, initialise_color_map, initialise_firefighters, planar_positions
from land_rep import TreePatch, RockPatch
import graph_helper
import builtins
import random
import io

class TestInitialiser(unittest.TestCase):
    def setUp(self) -> None:
        # Before each test, we create a new StringIO object and assign it to sys.stdout.
        # This means that all print statements in the tests will write to this object instead of the console.
        self.held = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self) -> None:
        # After each test, we restore sys.stdout to its original value. Or it can affect other tests.
        sys.stdout = self.held


    def test_generate_edges_read(self):
        options = {
            "gen_method": "read",
        }
        builtins.input = Mock(return_value='graphs/graph1.dat')
        edges, positions = generate_edges(options)
        self.assertEqual(edges, [(0, 1), (1, 2), (2, 3), (3, 0)])
        self.assertIsNotNone(positions)
        self.assertEqual(len(positions), 4)
        self.assertIsInstance(positions[0], tuple)
        self.assertIsInstance(positions[0][0], float)
        self.assertIsInstance(positions[0][1], float)
        
    def test_generate_edges_random(self):
        options = {
            "gen_method": "random"
        }
        builtins.input = Mock(return_value='r')
        random.randint = Mock(return_value=10)
        edges, positions = generate_edges(options)
        graph_helper.edges_planar = Mock(return_value=[(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4), (6, 7), (7, 8), (8, 9), (9, 10)])
        self.assertGreaterEqual(len(edges), 9)
        self.assertLessEqual(len(positions), len(edges))


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

    def test_planar_positions(self): #check if the function returns a dictionary with the correct keys and values
        edges = [(1, 2), (2, 3), (3, 1)]
        positions = planar_positions(edges)
        self.assertIsInstance(positions, dict)
        self.assertEqual(len(positions), 3)
        for i in range(1, 3):
            self.assertIn(i, positions)
            self.assertIsInstance(positions[i], tuple)
            self.assertIsInstance(positions[i][0], float)
            self.assertIsInstance(positions[i][1], float)

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