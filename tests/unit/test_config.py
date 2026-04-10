import pytest
import json
from unittest.mock import patch, mock_open
from core.config import Config

def test_configuration_loading():
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
    
    with patch("pathlib.Path.exists", return_value=True), \
         patch("pathlib.Path.open", mock_open(read_data=mock_json)):
        config = Config("fake_config.json")
        assert config.stutter_threshold_ms == 20.0
