import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock, patch

from simulation import Simulation

class TestSimulation(unittest.TestCase):
    def setUp(self):
        options = {"growth_rate": 10, "burn_rate": 20, "fire_spread_rate": 30, "new_forrest_probability": 100}
        patches = {1: MagicMock(), 2: MagicMock(), 3: MagicMock()}
        color_map = {1: 100, 2: 0, 3: 100}
        firefighters = {1: MagicMock(), 2: MagicMock()}
        neighbour_id_register = {1: [2, 3], 2: [1, 3], 3: [2, 1]}
        graph_info = MagicMock()
        graph_info.get_patches.return_value = patches
        graph_info.get_firefighters.return_value = firefighters
        self.simulation = Simulation(graph_info)

    def test_evolve(self):
        # Mocking patch methods
        patch1 = self.simulation.graphinfo.get_patches().get(1)
        patch1.get_treestat.return_value = 0
        patch1.is_burning.return_value = False

        patch2 = self.simulation.graphinfo.get_patches().get(2)
        patch2.get_treestat.return_value = 50
        patch2.is_burning.return_value = False

        patch3 = self.simulation.graphinfo.get_patches().get(3)
        patch3.get_treestat.return_value = 100
        patch3.is_burning.return_value = True

        self.simulation.evolve()

        # Check if history is updated correctly
        self.assertEqual(len(self.simulation.get_history()), 1)
        self.assertEqual(self.simulation.get_history()[0]["Tree_population"], 1)
        self.assertEqual(self.simulation.get_history()[0]["Rock_population"], 1)
        self.assertEqual(self.simulation.get_history()[0]["Fire_population"], 1)

        # Check if patch methods are called correctly
        patch1.random_forrest.assert_called_once() #special method for mock objects
        patch2.updateland.assert_called_once()
        patch3.updateland.assert_called_once()

    def test_activate_firefighters(self):
        # Mocking firefighter methods
        firefighter1 = self.simulation.graphinfo.get_firefighters().get(1)
        firefighter2 = self.simulation.graphinfo.get_firefighters().get(2)

        self.simulation.activate_firefighters()

        # Check if firefighter methods are called correctly
        firefighter1.move.assert_called_once() 
        firefighter2.move.assert_called_once()

if __name__ == '__main__':
    unittest.main()