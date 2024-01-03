import sys
import os
import io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from unittest.mock import Mock
import builtins
import config.config
from config.config import welcome, read_options_from_file, gen_method, ini_woods, ini_fires, firefighter_num, firefighter_level, iter_num

class TestConfig_part1(unittest.TestCase):
    def setUp(self) -> None:
        self.options = {
            "growth_rate" : 10, # Treestat fixed increase
            "burn_rate" : 20, # Fires effect on Treestat fixed.
            "new_forrest_probability" : 100, # Probability of new forrest in permille ie. 50 = 0,5 %
            "fire_spread_rate" : 30 # Percentage risk of fire to spread each iterations
            }
        
        #Remove prints
        self.held = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self) -> None:
        #Restore prints
        sys.stdout = self.held


    def test_navigation_full(self):
        builtins.input = Mock(side_effect = ["", "2"])
        self.assertEqual(welcome(self.options), 1)



if __name__ == '__main__':
    unittest.main()