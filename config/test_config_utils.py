import unittest
from config_utils import options_validater

class TestOptionsValidater(unittest.TestCase):
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
            "firefighter_num": 5
        }
        validated_options = options_validater(options)  #If 
        self.assertEqual(validated_options, options)

    def test_invalid_ini_woods(self):
        options = {
            "ini_woods": 150,
            "ini_fires": 10
        }
        validated_options = options_validater(options)
        self.assertIsNone(validated_options["ini_woods"])

    def test_invalid_ini_fires(self):
        options = {
            "ini_woods": 50,
            "ini_fires": -10
        }
        validated_options = options_validater(options)
        self.assertIsNone(validated_options["ini_fires"])

    def test_invalid_iter_num(self):
        options = {
            "iter_num": -100,
            "growth_rate": 2
        }
        validated_options = options_validater(options)
        self.assertIsNone(validated_options["iter_num"])

    def test_invalid_gen_method(self):
        options = {
            "gen_method": "invalid"
        }
        validated_options = options_validater(options)
        self.assertIsNone(validated_options["gen_method"])

    def test_invalid_firefighter_level(self):
        options = {
            "firefighter_level": 0
        }
        validated_options = options_validater(options)
        self.assertIsNone(validated_options["firefighter_level"])

    def test_invalid_firefighter_num(self):
        options = {
            "firefighter_num": -5
        }
        validated_options = options_validater(options)
        self.assertIsNone(validated_options["firefighter_num"])

if __name__ == '__main__':
    unittest.main()