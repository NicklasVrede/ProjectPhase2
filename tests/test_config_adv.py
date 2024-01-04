import sys
import os
import io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from unittest.mock import Mock
import builtins

import config.config
from config.config import (
    growth_rate, 
    burn_rate, 
    new_forrest_probability, 
    fire_spread_rate 
    )

class TestConfig_part1(unittest.TestCase):
    def setUp(self) -> None:
        self.options = {
            "growth_rate" : 10, # Treestat fixed increase
            "burn_rate" : 20, # Fires effect on Treestat fixed.
            "new_forrest_probability" : 100, # (1%)
            "fire_spread_rate" : 30 # (30%)
            }
        
        config.config.config_final = Mock(return_value=1) #Exit for testing

        #Remove prints
        self.held = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self) -> None:
        #Restore prints
        sys.stdout = self.held

    def test_navigation(self):
        self.assertEqual(growth_rate(self.options), 1) #Exit returns 1

    def test_growth_rate(self):
        del self.options["growth_rate"]
        list = ["", "a", "%", "1.5", "-20", "d"] #d for default (10)
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        growth_rate(self.options)
        self.assertEqual(self.options.get("growth_rate"), 10)
        self.assertEqual(mock_input.call_count, len(list))

    def test_burn_rate(self):
        del self.options["burn_rate"]
        list = ["", "a", "%", "1.5", "-20", "d"] #d for default (20)
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        burn_rate(self.options)
        self.assertEqual(self.options.get("burn_rate"), 20)
        self.assertEqual(mock_input.call_count, len(list))

    def test_new_forrest_probability(self):
        del self.options["new_forrest_probability"]
        list = ["", "a", "%", "1.5", "10001", "-20", "d"] #d for default (100)
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        new_forrest_probability(self.options)
        self.assertEqual(self.options.get("new_forrest_probability"), 100)
        self.assertEqual(mock_input.call_count, len(list))

    def test_fire_spread_rate(self):
        del self.options["fire_spread_rate"]
        list = ["", "a", "%", "1.5", "101", "-20", "d"] #d for default (30)
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        fire_spread_rate(self.options)
        self.assertEqual(self.options.get("fire_spread_rate"), 30)
        self.assertEqual(mock_input.call_count, len(list))


if __name__ == '__main__':
    unittest.main()