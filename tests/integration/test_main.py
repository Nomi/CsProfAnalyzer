import pytest
import os
import io
import sys
from unittest.mock import patch
from contextlib import redirect_stdout

# Add src to path so main can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
import main

def test_help_flag():
    """Integration test: Ensure help output is triggered and correct."""
    f = io.StringIO()
    # Patch CsProfAnalyzer in the entry point module where it's actually imported
    with patch("core.cs_prof_analyzer.CsProfAnalyzer") as MockAnalyzer:
        # Prevent analysis execution
        MockAnalyzer.return_value.load_data.return_value = None
        MockAnalyzer.return_value.run_analysis.return_value = None
        MockAnalyzer.return_value.display_report.return_value = None

        # Pass empty sys.argv, which triggers parser.print_help() and sys.exit(0)
        with redirect_stdout(f), patch("sys.argv", ["main.py"]):
            
            # The code calls sys.exit(0) when no file is provided
            with pytest.raises(SystemExit) as e:
                main.main()
            assert e.value.code == 0

    output = f.getvalue()
    # Verify basic help content presence
    assert "usage: main.py" in output
    assert "--brief" in output
