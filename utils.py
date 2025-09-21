from pathlib import Path
from typing import Tuple

ARTIFACTS = Path(__file__).resolve().parents[1] / "artifacts"
DATA = Path(__file__).resolve().parents[1] / "data"

def ensure_dirs() -> Tuple[Path, Path]:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)
    return ARTIFACTS, DATA

def savefig_no_style(fig, path: Path):
    # Save a Matplotlib figure without explicit style/colors.
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
