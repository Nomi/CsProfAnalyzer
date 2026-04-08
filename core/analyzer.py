import sys
import time
from typing import Dict, Any, Optional
from .strings import STRINGS as STR, C_CYAN, C_GREEN, C_RED, C_RESET, C_BOLD
from .config import CFG

class CS2Analyzer:
    def __init__(self, file_path: str) -> None:
        self.file_path: str = file_path
        self.df: Optional[Any] = None 
        self.results: Dict[str, Dict[str, float]] = {}
        self.duration: float = 0.0
        self.server_diff: float = 0.0
        self.stutter_count: int = 0
        self.stutter_rate: float = 0.0

    def load_data(self) -> None:
        import pandas as pd
        try:
            self.df = pd.read_csv(self.file_path, skipinitialspace=True, engine='python')
            self.df.columns = self.df.columns.str.strip()
            
            numeric_cols = [CFG.COL_FRAME_FPS, CFG.COL_SMOOTH_FPS, CFG.COL_FRAME_MS, 
                            CFG.COL_SMOOTH_MS, CFG.COL_SERVER_MS, CFG.COL_TIME]

            for col in numeric_cols:
                if col in self.df.columns:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

            self.df.dropna(subset=[CFG.COL_FRAME_MS], inplace=True)
            if self.df.empty:
                raise ValueError(STR.MSG_NO_DATA)
        except Exception as e:
            print(STR.MSG_LOAD_ERR.format(error=str(e)))
            sys.exit(1)

    def _calculate_metrics(self, series: Any, reverse: bool = False) -> Dict[str, float]:
        import pandas as pd
        stats: Dict[str, float] = {
            STR.LBL_MEAN: float(series.mean()),
            STR.LBL_MAX: float(series.max()),
            STR.LBL_MIN: float(series.min()),
            STR.LBL_JITTER: float(series.std()),
        }
        for p, base_label in CFG.PERCENTILE_MAP.items():
            label = STR.LBL_MEDIAN if p == 0.5 else f"{base_label} {STR.SUFFIX_LOW if reverse else STR.SUFFIX_HIGH}"
            val = series.quantile(p) if reverse else series.quantile(1-p)
            stats[label] = float(val) if pd.notnull(val) else 0.0
        return stats

    def run_analysis(self) -> None:
        from tqdm import tqdm
        tasks = [(CFG.COL_FRAME_FPS, True), (CFG.COL_SMOOTH_FPS, True),
                 (CFG.COL_FRAME_MS, False), (CFG.COL_SMOOTH_MS, False)]

        print(STR.MSG_ANALYZING)
        for col, rev in tqdm(tasks, bar_format="{l_bar}%s{bar}%s{r_bar}" % (C_GREEN, C_RESET)):
            time.sleep(0.05) 
            self.results[col] = self._calculate_metrics(self.df[col], reverse=rev)

        self.duration = float(self.df[CFG.COL_TIME].iloc[-1] - self.df[CFG.COL_TIME].iloc[0])
        self.server_diff = float((self.df[CFG.COL_SERVER_MS] - self.df[CFG.COL_FRAME_MS]).mean())
        self.stutter_count = int((self.df[CFG.COL_FRAME_MS] > CFG.STUTTER_THRESHOLD_MS).sum())
        self.stutter_rate = (self.stutter_count / len(self.df)) * 100

    def display_report(self) -> None:
        from colorama import Fore, Style
        mag = Fore.MAGENTA + Style.BRIGHT
        cya = Fore.CYAN + Style.BRIGHT
        rst = Style.RESET_ALL
        print(f"\n{mag}{STR.SECTION_LINE}")
        print(f"{mag}{STR.SECTION_TITLE.format(duration=self.duration)}")
        print(f"{mag}{STR.SECTION_LINE}{rst}")

        for category, metrics in self.results.items():
            print(f"\n{cya}[{category}]{rst}")
            unit = STR.UNIT_MS if "MS" in category else STR.UNIT_FPS
            for label, val in metrics.items():
                color = Fore.WHITE
                if label in (STR.LBL_MEAN, STR.LBL_MEDIAN): color = Fore.GREEN
                elif STR.SUFFIX_LOW in label or STR.SUFFIX_HIGH in label: color = Fore.YELLOW
                elif label == STR.LBL_JITTER: color = Fore.RED if val > 10 else Fore.GREEN
                print(f"  {color}{label:20}: {val:8.2f} {unit}{rst}")

        stutter_color = Fore.RED if self.stutter_count > 0 else Fore.GREEN
        print(f"\n{cya}[{STR.SECTION_ENGINE}]{rst}")
        print(f"  {Fore.WHITE}{STR.LBL_SERVER:20}: {self.server_diff:.2f} {STR.UNIT_MS}")
        stutter_lbl = STR.LBL_STUTTER.format(threshold=CFG.STUTTER_THRESHOLD_MS)
        print(f"  {stutter_color}{stutter_lbl:20}: {self.stutter_count} ({self.stutter_rate:.2f}%){rst}")
        print(f"{mag}{STR.SECTION_LINE}{rst}\n")
