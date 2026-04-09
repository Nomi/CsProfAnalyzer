"""Strings and UI resource management."""

import json
import os
import sys
from types import MappingProxyType
from typing import Final


class Strings:
    """Immutable UI strings loaded from locale-specific JSON."""

    def __init__(self, locale: str = "en-us") -> None:
        # Determine the directory where this script (strings.py) is located
        core_dir = os.path.dirname(os.path.abspath(__file__))

        # PyInstaller bundled location
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
            # PyInstaller puts `core/locale` at `locale/` in the bundle root
            strings_path = os.path.join(base_path, "locale", locale, "strings.json")
        else:
            # Script execution: strings.py is in 'core/', locale is in 'core/locale/'
            strings_path = os.path.join(core_dir, "locale", locale, "strings.json")

        if not os.path.exists(strings_path):
            raise FileNotFoundError(
                f"UI strings file for {locale} not found at: {strings_path}"
            )

        with open(strings_path, "r", encoding="utf-8") as file:
            self._data: Final[dict] = json.load(file)

    def __getattr__(self, name: str) -> str:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"No such UI string: {name}")

    @property
    def glossary_map(self) -> MappingProxyType:
        """Returns the glossary mapping."""
        return MappingProxyType(self._data["GLOSSARY_MAP"])

    @property
    def help_epilog(self) -> str:
        """Returns the help epilog."""
        return str(self._data["HELP_EPILOG"])


# ANSI Colors for terminal output
C_CYAN: Final = "\033[96m"
C_YELLOW: Final = "\033[93m"
C_GREEN: Final = "\033[92m"
C_RED: Final = "\033[91m"
C_MAGENTA: Final = "\033[95m"
C_BOLD: Final = "\033[1m"
C_RESET: Final = "\033[0m"

STRINGS = Strings()
