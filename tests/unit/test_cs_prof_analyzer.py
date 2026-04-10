import pytest
import tempfile
import os
from core.cs_prof_analyzer import CsProfAnalyzer

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
    return CsProfAnalyzer(temp_csv)

def test_data_loading(analyzer):
    analyzer.load_data()
    assert analyzer.df is not None
    assert len(analyzer.df) == 2

def test_initialization_success(analyzer):
    assert analyzer is not None
    assert analyzer.file_path is not None
