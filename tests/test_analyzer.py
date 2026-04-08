"""Unit tests for performance analyzer core logic."""

import unittest
import os
from core.analyzer import CS2Analyzer
from core.config import AppConfig

class TestPerformanceAnalyzer(unittest.TestCase):
    """Test suite for performance analysis."""

    def setUp(self):
        self.config_path = "config.json"
        self.analyzer = CS2Analyzer("test_data.csv")
        
        # Create a dummy CSV file
        with open("test_data.csv", "w", encoding="utf-8") as f:
            f.write("Time,Frame FPS,Smooth FPS,Frame MS,Smooth MS,Server Frame MS\n")
            f.write("0.0,60,60,16.6,16.6,16.6\n")
            f.write("1.0,60,60,16.6,16.6,16.6\n")

    def tearDown(self):
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

    def test_load_data(self):
        """Test data loading functionality."""
        self.analyzer.load_data()
        self.assertIsNotNone(self.analyzer.df)
        self.assertEqual(len(self.analyzer.df), 2)

    def test_config_loading(self):
        """Test that configuration loads correctly."""
        config = AppConfig(self.config_path)
        self.assertIsInstance(config.stutter_threshold_ms, float)

if __name__ == "__main__":
    unittest.main()
