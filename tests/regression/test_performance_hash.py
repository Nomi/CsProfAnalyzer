import hashlib
import io
from contextlib import redirect_stdout
from pathlib import Path
from core.cs_prof_analyzer import CsProfAnalyzer

def test_analyzer_output_hash():
    """Regression test: Ensure analyzer --brief output matches known SHA256 hash."""
    dust2_path = Path(__file__).parent.parent / "data" / "prof_de_dust2.csv"
    dust2_analyzer = CsProfAnalyzer(str(dust2_path))
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
