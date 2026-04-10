"""Application configuration module."""

import json
import sys
from pathlib import Path
from .utils import get_app_dir
from types import MappingProxyType
from typing import Dict, Any, Final


class AppConfig:
    """Read-only configuration loaded from JSON with schema validation."""

    SCHEMA = {
        "PERCENTILE_MAP": dict,
        "STUTTER_THRESHOLD_MS": (int, float),
        "COL_TIME": str,
        "COL_FRAME_FPS": str,
        "COL_SMOOTH_FPS": str,
        "COL_FRAME_MS": str,
        "COL_SMOOTH_MS": str,
        "COL_SERVER_MS": str,
    }

    def __init__(self, config_name: str = "config.json") -> None:
        base_path = get_app_dir()
        config_path = base_path / config_name
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with config_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            self._validate(data)
            self._data: Final[Dict[str, Any]] = data

    def _validate(self, data: Dict[str, Any]) -> None:
        for key, expected_type in self.SCHEMA.items():
            if key not in data:
                raise ValueError(f"Missing config key: {key}")
            if not isinstance(data[key], expected_type):
                raise TypeError(
                    f"Config key '{key}' expected {expected_type}, got {type(data[key])}"
                )

    @property
    def percentile_map(self) -> MappingProxyType:
        """Returns the percentile map."""
        return MappingProxyType(
            {float(k): v for k, v in self._data["PERCENTILE_MAP"].items()}
        )

    @property
    def stutter_threshold_ms(self) -> float:
        """Returns the stutter threshold in milliseconds."""
        return float(self._data["STUTTER_THRESHOLD_MS"])

    @property
    def col_time(self) -> str:
        """Returns the time column name."""
        return str(self._data["COL_TIME"])

    @property
    def col_frame_fps(self) -> str:
        """Returns the frame FPS column name."""
        return str(self._data["COL_FRAME_FPS"])

    @property
    def col_smooth_fps(self) -> str:
        """Returns the smooth FPS column name."""
        return str(self._data["COL_SMOOTH_FPS"])

    @property
    def col_frame_ms(self) -> str:
        """Returns the frame MS column name."""
        return str(self._data["COL_FRAME_MS"])

    @property
    def col_smooth_ms(self) -> str:
        """Returns the smooth MS column name."""
        return str(self._data["COL_SMOOTH_MS"])

    @property
    def col_server_ms(self) -> str:
        """Returns the server frame MS column name."""
        return str(self._data["COL_SERVER_MS"])


CFG = AppConfig()
