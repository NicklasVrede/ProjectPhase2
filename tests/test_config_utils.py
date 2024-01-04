import sys
import os
import io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from config.config_utils import options_validater

class TestOptionsValidater(unittest.TestCase):
    def setUp(self) -> None:
        # Before tests, we assign a new StringIO object to sys.stdout.
        # Test print statements will write to this object, not the console.
        self.held = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self) -> None:
        # We restore sys.stdout after each test to avoid affecting other tests.
        sys.stdout = self.held

    def test_valid_options(self):
        options = {
            "ini_woods": 80,
            "ini_fires": 10,
            "iter_num": 100,
            "growth_rate": 10,
            "burn_rate": 20,
            "new_forrest_probability": 100,
            "fire_spread_rate": 30,
            "gen_method": "random",
            "firefighter_level": 3,
            "firefighter_num": "10%"
        }
        validated_options = options_validater(options)  #If 
        self.assertEqual(validated_options, options)

    def test_invalid_1(self):
        list = ["", "a", "%", "1.5", "101", "-20", "0", "   "]
        for option in list:
            options = {"ini_woods": option,
                        "ini_fires": option,
                        "firefighter_level": option,
                        "gen_method": option,
                        "fire_spread_rate": option,
                       }
            validated_options = options_validater(options)
            self.assertIsNone(validated_options["ini_woods"])
    
    def test_invalid_new_forrest_probability(self):
        list = ["", "a", "%", "1.5", "10001", "-20", "0", "   "]
        for option in list:
            options = {"new_forrest_probability": option}
            validated_options = options_validater(options)
            self.assertIsNone(validated_options["new_forrest_probability"])

    def test_invalid_no_max(self):
        list = ["", "a", "%", "1.5", "-20", "0", "   "]
        for option in list:
            options = {"growth_rate": option,
                        "burn_rate": option,
                        "fire_spread_rate": option,
                        "iter_num": option,
                       }
            validated_options = options_validater(options)
            self.assertIsNone(validated_options["growth_rate"])

if __name__ == '__main__':
    unittest.main()