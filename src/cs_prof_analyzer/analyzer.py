"""Module for core performance analysis logic."""

import sys
import time
from typing import Dict, Any, Optional
import pandas as pd
from tqdm import tqdm
from colorama import Fore, Style
from .strings import STRINGS, C_GREEN, C_RESET
from .config import CFG


class CS2Analyzer:
    """Class to load, analyze, and report on CS2 performance data."""

    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.df: Optional[pd.DataFrame] = None
        self.results: Dict[str, Dict[str, float]] = {}
        self.duration: float = 0.0
        self.server_diff: float = 0.0
        self.stutter_count: int = 0
        self.stutter_rate: float = 0.0

    def load_data(self) -> None:
        """Loads and cleans the profiling CSV data."""
        try:
            self.df = pd.read_csv(self.file_path, skipinitialspace=True, engine="python")
            self.df.columns = self.df.columns.str.strip()

            numeric_cols = [
                CFG.col_frame_fps,
                CFG.col_smooth_fps,
                CFG.col_frame_ms,
                CFG.col_smooth_ms,
                CFG.col_server_ms,
                CFG.col_time,
            ]

            for col in numeric_cols:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

            self.df.dropna(subset=[CFG.col_frame_ms], inplace=True)
            if self.df.empty:
                raise ValueError(STRINGS.MSG_NO_DATA)
        except (IOError, ValueError) as err:
            print(STRINGS.MSG_LOAD_ERR.format(error=str(err)))
            sys.exit(1)

    def _calculate_metrics(self, series: Any, reverse: bool = False) -> Dict[str, float]:
        stats: Dict[str, float] = {
            STRINGS.LBL_MEAN: float(series.mean()),
            STRINGS.LBL_MAX: float(series.max()),
            STRINGS.LBL_MIN: float(series.min()),
            STRINGS.LBL_JITTER: float(series.std()),
        }
        for percentile, base_label in CFG.percentile_map.items():
            label = (
                STRINGS.LBL_MEDIAN
                if percentile == 0.5
                else f"{base_label} {STRINGS.SUFFIX_LOW if reverse else STRINGS.SUFFIX_HIGH}"
            )
            val = (
                series.quantile(percentile)
                if reverse
                else series.quantile(1 - percentile)
            )
            stats[label] = float(val) if pd.notnull(val) else 0.0
        return stats

    def run_analysis(self) -> None:
        """Runs the performance analysis on the loaded dataframe."""
        tasks = [
            (CFG.col_frame_fps, True),
            (CFG.col_smooth_fps, True),
            (CFG.col_frame_ms, False),
            (CFG.col_smooth_ms, False),
        ]

        print(STRINGS.MSG_ANALYZING)
        for col, rev in tqdm(
            tasks, bar_format="{l_bar}%s{bar}%s{r_bar}" % (C_GREEN, C_RESET)
        ):
            time.sleep(0.05)
            self.results[col] = self._calculate_metrics(self.df[col], reverse=rev)

        self.duration = float(
            self.df[CFG.col_time].iloc[-1] - self.df[CFG.col_time].iloc[0]
        )
        self.server_diff = float(
            (self.df[CFG.col_server_ms] - self.df[CFG.col_frame_ms]).mean()
        )
        self.stutter_count = int(
            (self.df[CFG.col_frame_ms] > CFG.stutter_threshold_ms).sum()
        )
        self.stutter_rate = (self.stutter_count / len(self.df)) * 100

    def display_report(self) -> None:
        """Prints the analysis report to the terminal."""
        mag = Fore.MAGENTA + Style.BRIGHT
        cya = Fore.CYAN + Style.BRIGHT
        rst = Style.RESET_ALL
        print(f"\n{mag}{STRINGS.SECTION_LINE}")
        print(f"{mag}{STRINGS.SECTION_TITLE.format(duration=self.duration)}")
        print(f"{mag}{STRINGS.SECTION_LINE}{rst}")

        for category, metrics in self.results.items():
            print(f"\n{cya}[{category}]{rst}")
            unit = STRINGS.UNIT_MS if "MS" in category else STRINGS.UNIT_FPS
            for label, val in metrics.items():
                color = Fore.WHITE
                if label in (STRINGS.LBL_MEAN, STRINGS.LBL_MEDIAN):
                    color = Fore.GREEN
                elif STRINGS.SUFFIX_LOW in label or STRINGS.SUFFIX_HIGH in label:
                    color = Fore.YELLOW
                elif label == STRINGS.LBL_JITTER:
                    color = Fore.RED if val > 10 else Fore.GREEN
                print(f"  {color}{label:20}: {val:8.2f} {unit}{rst}")

        stutter_color = Fore.RED if self.stutter_count > 0 else Fore.GREEN
        print(f"\n{cya}[{STRINGS.SECTION_ENGINE}]{rst}")
        print(f"  {Fore.WHITE}{STRINGS.LBL_SERVER:20}: {self.server_diff:.2f} {STRINGS.UNIT_MS}")
        stutter_lbl = STRINGS.LBL_STUTTER.format(
            threshold=CFG.stutter_threshold_ms
        )
        print(
            f"  {stutter_color}{stutter_lbl:20}: "
            f"{self.stutter_count} ({self.stutter_rate:.2f}%){rst}"
        )
        print(f"{mag}{STRINGS.SECTION_LINE}{rst}\n")
