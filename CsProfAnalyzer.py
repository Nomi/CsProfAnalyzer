import sys
import argparse
from core.strings import STRINGS as STR
from core.utils import validate_dependencies, show_help_glossary
from core.analyzer import CS2Analyzer

def main() -> None:
    # Use properties as attributes, now dynamically loaded
    parser = argparse.ArgumentParser(
        description=STR.APP_DESC,
        epilog=STR.HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("file", nargs='?', help="Path to your profiling CSV")
    parser.add_argument("-b", "--brief", action="store_true", help="Omit the metrics glossary from output")
    
    args = parser.parse_args()
    
    if not args.file:
        parser.print_help()
        sys.exit(0)
        
    if not args.brief:
        show_help_glossary()
        
    validate_dependencies()
    
    from colorama import init
    init(autoreset=True)

    engine = CS2Analyzer(args.file)
    engine.load_data()
    engine.run_analysis()
    engine.display_report()

if __name__ == "__main__":
    main()
