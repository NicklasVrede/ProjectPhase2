import sys
import os
import io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import random
import unittest
from unittest.mock import Mock
import builtins
import config.config
from config.config import welcome, read_options_from_file, gen_method, ini_woods, ini_fires, firefighter_num, firefighter_level, iter_num, config_final, change_setting
from config.config_utils import advanced_defaults


class TestConfig_part1(unittest.TestCase):
    def setUp(self) -> None:
        self.options = {
            "gen_method" : "random", #Generation method for patches. "random" or "read"
            "ini_woods" : 100, # Percentage of forrests in the graph, rest = rocks
            "firefighter_num" : "10%", # Number of firefighters a percentage have to be in quotation marks like "20%"
            "firefighter_level" : 3, # 1 (low), 2 (medium) or 3 (high)
            "ini_fires" : 20, # Percentage of fires in forrests
            "iter_num" : 10, # Number of sumulation iterations
            }
        self.options = advanced_defaults(self.options) #set advanced defaults

        config.config.config_final = Mock(return_value=1) #Exit for testing
        
        #Remove prints
        self.held = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self) -> None:
        #Restore prints
        sys.stdout = self.held
        config.config.config_final = config_final

    def test_navigation(self):
        builtins.input = Mock(side_effect = ["", "2"])
        self.assertEqual(welcome(self.options), 1) #Exit returns 1

    def test_read_options(self):
        list = ["", "a", "%", "1.5", "100", "2"] #2 for no read
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        read_options_from_file(self.options)
        #check if all inputs are called
        self.assertEqual(mock_input.call_count, len(list))

    def test_gen_method(self):
        del self.options["gen_method"]
        list = ["a", "%", "1.5", "100", "r"] #r for random
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input
        
        gen_method(self.options)
        self.assertEqual(gen_method(self.options), 1)
        self.assertEqual(self.options["gen_method"], "random")
        self.assertEqual(mock_input.call_count, len(list))

    def test_ini_woods(self):
        del self.options["ini_woods"]
        list = ["a", "%", "1.5", "100", "r"] #r for random
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input
        random.randint = Mock(return_value=88)

        ini_woods(self.options)
        self.assertEqual(self.options["ini_woods"], 88)
        self.assertEqual(mock_input.call_count, len(list))

    def test_ini_fires(self):
        del self.options["ini_fires"]
        list = ["", "a", "%", "1.5", "101", "-20", "d"] #d for default (20)
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        ini_fires(self.options)
        self.assertEqual(self.options["ini_fires"], 20)
        self.assertEqual(mock_input.call_count, len(list))

    def test_firefighter_num(self):
        del self.options["firefighter_num"]
        list = ["", "a", "%", "1.5", "-20", "d"] #d for default (10%)
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        firefighter_num(self.options)
        self.assertEqual(self.options["firefighter_num"], "10%")
        self.assertEqual(mock_input.call_count, len(list))

    def test_firefighter_level(self):
        del self.options["firefighter_level"]
        list = ["", "a", "%", "1.5", "101", "-20", "d"] #d for default (3)
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        firefighter_level(self.options)
        self.assertEqual(self.options["firefighter_level"], 3)
        self.assertEqual(mock_input.call_count, len(list))
    
    def test_iter_num(self):
        del self.options["iter_num"]
        list = ["", "a", "%", "1.5", "-30", "d"] #d for default (20)
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        iter_num(self.options)
        self.assertEqual(self.options["iter_num"], 20)
        self.assertEqual(mock_input.call_count, len(list))


    def test_change_setting(self):
        list = ["", "a", "%", "1.5", "100", "2", "d"] #2 for ini_woods, d for default (80)
        mock_input = Mock(side_effect=list)
        builtins.input = mock_input

        change_setting(self.options)
        self.assertEqual(self.options["ini_woods"], 80)
        self.assertEqual(mock_input.call_count, len(list))

        
if __name__ == '__main__':
    unittest.main()