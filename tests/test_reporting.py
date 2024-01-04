import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock
import matplotlib.pyplot as plt

from reporting import reporting


class TestReporting(unittest.TestCase):
    def setUp(self): #Mocking plt methods to avoid opening a window
        plt.plot = Mock()
        plt.xlabel = Mock()
        plt.ylabel = Mock()
        plt.legend = Mock()
        plt.show = Mock()

    def test_reporting(self):
        history = {
            1: {"Rock_population": 10, "Fire_population": 5, "Tree_population": 20},
            2: {"Rock_population": 8, "Fire_population": 3, "Tree_population": 18},
            3: {"Rock_population": 6, "Fire_population": 1, "Tree_population": 15}
        }

        reporting(history)

        for method in [plt.xlabel, plt.ylabel, plt.legend, plt.show]:
            method.assert_called_once()
        assert plt.plot.call_count == len(history[1])


if __name__ == '__main__':
    unittest.main()