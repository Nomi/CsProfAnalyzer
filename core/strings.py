import json
import os
from types import MappingProxyType
from typing import Final

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
