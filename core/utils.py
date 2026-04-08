"""Utility functions for dependency validation and glossary display."""

import sys
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
