import json
import os
from types import MappingProxyType
from typing import Dict, Any, Final

class AppConfig:
    """Read-only configuration loaded from JSON with schema validation."""
    _data: Final[Dict[str, Any]]

    # Schema definition for validation
    SCHEMA = {
        "PERCENTILE_MAP": dict,
        "STUTTER_THRESHOLD_MS": (int, float),
        "COL_TIME": str,
        "COL_FRAME_FPS": str,
        "COL_SMOOTH_FPS": str,
        "COL_FRAME_MS": str,
        "COL_SMOOTH_MS": str,
        "COL_SERVER_MS": str
    }

    def __init__(self, config_path: str = "config.json"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            data = json.load(f)
            self._validate(data)
            self._data = data

    def _validate(self, data: Dict[str, Any]):
        for key, expected_type in self.SCHEMA.items():
            if key not in data:
                raise ValueError(f"Missing config key: {key}")
            if not isinstance(data[key], expected_type):
                raise TypeError(f"Config key '{key}' expected {expected_type}, got {type(data[key])}")

    @property
    def PERCENTILE_MAP(self) -> MappingProxyType:
        return MappingProxyType({float(k): v for k, v in self._data["PERCENTILE_MAP"].items()})

    @property
    def STUTTER_THRESHOLD_MS(self) -> float:
        return float(self._data["STUTTER_THRESHOLD_MS"])

    @property
    def COL_TIME(self) -> str:
        return str(self._data["COL_TIME"])

    @property
    def COL_FRAME_FPS(self) -> str:
        return str(self._data["COL_FRAME_FPS"])

    @property
    def COL_SMOOTH_FPS(self) -> str:
        return str(self._data["COL_SMOOTH_FPS"])

    @property
    def COL_FRAME_MS(self) -> str:
        return str(self._data["COL_FRAME_MS"])

    @property
    def COL_SMOOTH_MS(self) -> str:
        return str(self._data["COL_SMOOTH_MS"])

    @property
    def COL_SERVER_MS(self) -> str:
        return str(self._data["COL_SERVER_MS"])

CFG = AppConfig()
