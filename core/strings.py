import json
import os
from types import MappingProxyType
from typing import Final

# ANSI Colors for terminal output
C_CYAN: Final = "\033[96m"
C_YELLOW: Final = "\033[93m"
C_GREEN: Final = "\033[92m"
C_RED: Final = "\033[91m"
C_MAGENTA: Final = "\033[95m"
C_BOLD: Final = "\033[1m"
C_RESET: Final = "\033[0m"

class Strings:
    """Immutable UI strings loaded from locale-specific JSON."""
    _data: Final[dict]

    def __init__(self, locale: str = "en-us"):
        strings_path = os.path.join(os.path.dirname(__file__), "locale", locale, "strings.json")
        
        if not os.path.exists(strings_path):
            raise FileNotFoundError(f"UI strings file for {locale} not found at: {strings_path}")
        
        with open(strings_path, 'r') as f:
            self._data = json.load(f)

    def __getattr__(self, name: str) -> str:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"No such UI string: {name}")

    @property
    def GLOSSARY_MAP(self) -> MappingProxyType:
        return MappingProxyType(self._data["GLOSSARY_MAP"])

    @property
    def HELP_EPILOG(self) -> str:
        return str(self._data["HELP_EPILOG"])

STRINGS = Strings()
