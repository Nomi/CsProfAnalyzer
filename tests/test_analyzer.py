"""Unit tests for performance analyzer core logic."""

import unittest
import tempfile
import os
import json
from unittest.mock import patch, mock_open
from core.analyzer import CS2Analyzer
from core.config import AppConfig


class TestPerformanceAnalyzer(unittest.TestCase):
    """Test suite for performance analysis."""

    def setUp(self):
        # Create a temporary file for testing (for basic tests)
        self.test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
        self.test_file.write("Time,Frame FPS,Smooth FPS,Frame MS,Smooth MS,Server Frame MS\n")
        self.test_file.write("0.0,60,60,16.6,16.6,16.6\n")
        self.test_file.write("1.0,60,60,16.6,16.6,16.6\n")
        self.test_file.close()
        
        self.analyzer = CS2Analyzer(self.test_file.name)

    def tearDown(self):
        # Clean up temporary file
        if os.path.exists(self.test_file.name):
            os.remove(self.test_file.name)

    def test_dust2_metrics(self):
        """Test accuracy of metrics calculation using known dust2 data."""
        from pathlib import Path
        dust2_path = Path(__file__).parent / "data" / "prof_de_dust2.csv"
        self.dust2_analyzer = CS2Analyzer(str(dust2_path))
        self.dust2_analyzer.load_data()
        
        self.assertIsNotNone(self.dust2_analyzer.df)
        self.assertGreater(len(self.dust2_analyzer.df), 1000)
        
        from core.config import CFG
        stutter_count = (self.dust2_analyzer.df[CFG.col_frame_ms] > CFG.stutter_threshold_ms).sum()
        self.assertGreater(stutter_count, 1000)

    def test_load_data(self):
        """Test data loading functionality."""
        self.analyzer.load_data()
        self.assertIsNotNone(self.analyzer.df)
        self.assertEqual(len(self.analyzer.df), 2)

    def test_basic_initialization(self):
        """Test that analyzer initializes with a valid path."""
        self.assertIsNotNone(self.analyzer)
        self.assertEqual(self.analyzer.file_path, self.test_file.name)

    def test_config_loading(self):
        """Test that configuration loads correctly."""
        mock_json = json.dumps({
            "STUTTER_THRESHOLD_MS": 20.0,
            "PERCENTILE_MAP": {},
            "COL_TIME": "Time",
            "COL_FRAME_FPS": "Frame FPS",
            "COL_SMOOTH_FPS": "Smooth FPS",
            "COL_FRAME_MS": "Frame MS",
            "COL_SMOOTH_MS": "Smooth MS",
            "COL_SERVER_MS": "Server Frame MS"
        })
        
        # Patch exists and the open method on Path objects
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.open", mock_open(read_data=mock_json)):
            config = AppConfig("fake_config.json")
            self.assertEqual(config.stutter_threshold_ms, 20.0)


if __name__ == "__main__":
    unittest.main()
