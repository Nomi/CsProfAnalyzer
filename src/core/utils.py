import sys
from pathlib import Path

def get_app_dir():
    # If running as an EXE via PyInstaller
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    # If running as a script (module is src/core/utils.py, so go up 2 levels to src/)
    return Path(__file__).resolve().parent.parent

"""Utility functions for dependency validation and glossary display."""
from colorama import Fore, Style
from .strings import STRINGS, C_YELLOW, C_RESET


def validate_dependencies() -> None:
    """Validates that required external packages are installed."""
    required = ["pandas", "numpy", "tqdm", "colorama"]
    missing = [
        pkg
        for pkg in required
        if not __import__("importlib").util.find_spec(pkg)
    ]
    if missing:
        pkgs = ", ".join(missing)
        print(STRINGS.MSG_MISSING_DEPS.format(pkg_list=pkgs))
        print(STRINGS.MSG_INSTALL)
        print(STRINGS.MSG_PIP.format(pkg_list=pkgs))
        sys.exit(1)


def show_help_glossary() -> None:
    """Displays the metrics glossary."""
    print(STRINGS.SECTION_GLOSSARY)
    for key, value in STRINGS.glossary_map.items():
        print(f"{C_YELLOW}{key:18}{C_RESET}: {value}")
    print("-" * 50)
