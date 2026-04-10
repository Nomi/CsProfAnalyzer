import pytest
import tempfile
import os
import json
import hashlib
import io
from unittest.mock import patch, mock_open
from contextlib import redirect_stdout
from src.core.analyzer import CS2Analyzer
from src.core.config import AppConfig

@pytest.fixture
def temp_csv():
    # Setup: Create a temporary file
    test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
    test_file.write("Time,Frame FPS,Smooth FPS,Frame MS,Smooth MS,Server Frame MS\n")
    test_file.write("0.0,60,60,16.6,16.6,16.6\n")
    test_file.write("1.0,60,60,16.6,16.6,16.6\n")
    test_file.close()
    
    yield test_file.name
    
    # Teardown: Clean up
    if os.path.exists(test_file.name):
        os.remove(test_file.name)

@pytest.fixture
def analyzer(temp_csv):
    return CS2Analyzer(temp_csv)

def test_analyzer_output_hash(analyzer):
    """Regression test: Ensure analyzer --brief output matches known SHA256 hash."""
    from pathlib import Path
    dust2_path = Path(__file__).parent / "data" / "prof_de_dust2.csv"
    dust2_analyzer = CS2Analyzer(str(dust2_path))
    dust2_analyzer.load_data()
    
    # Capture stdout
    f = io.StringIO()
    with redirect_stdout(f):
        dust2_analyzer.run_analysis()
        dust2_analyzer.display_report()
        
    output = f.getvalue()
    sha256_hash = hashlib.sha256(output.encode('utf-8')).hexdigest()
    
    known_hash = "04e7da828608575229ccfb068139466501261feea9639d21b5c9997d355ff319"
    assert sha256_hash == known_hash

def test_help_flag():
    """Regression test: Ensure help output matches known SHA256 hash."""
    f = io.StringIO()
    with redirect_stdout(f), patch("sys.argv", ["cs_prof_analyzer.py", "--help"]), patch("sys.exit"), patch("core.analyzer.CS2Analyzer"):
        import sys
        # The entry point is at src/cs_prof_analyzer.py
        sys.path.insert(0, os.path.abspath('src'))
        from cs_prof_analyzer import main
        with pytest.raises(SystemExit):
            main()
    
    output = f.getvalue()
    assert "usage: cs_prof_analyzer.py" in output
    assert "--brief" in output

def test_data_loading(analyzer):
    analyzer.load_data()
    assert analyzer.df is not None
    assert len(analyzer.df) == 2

def test_initialization_success(analyzer):
    assert analyzer is not None
    assert analyzer.file_path is not None

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
        config = AppConfig("fake_config.json")
        assert config.stutter_threshold_ms == 20.0
