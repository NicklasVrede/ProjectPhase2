import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock
from simulation import Simulation

class TestSimulation(unittest.TestCase):
    def setUp(self):
        self.graphInfo = Mock()
        self.patches = {1: Mock(), 2: Mock(), 3: Mock()}
        patches = self.patches
        self.graphInfo.get_patches.return_value = patches
        for patch in patches.values():
            patch.updateland.return_value = None
        patches[1].get_treestat.return_value = 100
        patches[1].is_burning.return_value = False
        patches[2].get_treestat.return_value = 0
        patches[2].random_forrest.return_value = None
        patches[3].get_treestat.return_value = 100
        patches[3].is_burning.return_value = True
        self.graphInfo.activate_firefighters.return_value = None
        self.simulation = Simulation(self.graphInfo)

    def test_evolve(self):
        self.simulation.evolve()

        # Check if graphInfo is updated correctly
        self.graphInfo.activate_firefighters.assert_called_once()
        self.assertEqual(self.graphInfo.get_patches.call_count, 1)
        self.assertEqual(self.patches[1].get_treestat.call_count, 2)
        self.assertEqual(self.patches[1].updateland.call_count, 1)
        self.assertEqual(self.patches[2].get_treestat.call_count, 2)
        self.assertEqual(self.patches[2].updateland.call_count, 0)
        self.assertEqual(self.patches[2].random_forrest.call_count, 1)
        self.assertEqual(self.patches[3].get_treestat.call_count, 2)
        self.assertEqual(self.patches[3].updateland.call_count, 1)
        self.assertEqual(self.patches[3].is_burning.call_count, 1)

        # Check if history is updated correctly
        self.assertEqual(len(self.simulation.get_history()), 1)
        self.assertEqual(self.simulation.get_history()[0]["Tree_population"], 1)
        self.assertEqual(self.simulation.get_history()[0]["Rock_population"], 1)
        self.assertEqual(self.simulation.get_history()[0]["Fire_population"], 1)

        


if __name__ == '__main__':
    unittest.main()