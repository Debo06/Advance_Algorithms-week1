import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Support both package and script execution contexts
try:
    from .utils import savefig_no_style  # type: ignore
except Exception:
    from utils import savefig_no_style  # type: ignore

def basic_overview(df: pd.DataFrame, outdir: Path):
    (outdir / "eda_summary.txt").write_text(str(df.describe(include="all")), encoding="utf-8")

def plot_histograms(df: pd.DataFrame, outdir: Path, cols=None):
    if cols is None:
        cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    for c in cols:
        fig, ax = plt.subplots()
        ax.hist(df[c].dropna(), bins=30)
        ax.set_title(f"Histogram — {c}")
        ax.set_xlabel(c)
        ax.set_ylabel("Count")
        savefig_no_style(fig, outdir / f"hist_{c}.png")
        plt.close(fig)

def plot_boxplots(df: pd.DataFrame, outdir: Path, cols=None):
    if cols is None:
        cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    for c in cols:
        fig, ax = plt.subplots()
        ax.boxplot(df[c].dropna(), vert=True)
        ax.set_title(f"Boxplot — {c}")
        savefig_no_style(fig, outdir / f"box_{c}.png")
        plt.close(fig)

def plot_scatter(df: pd.DataFrame, outdir: Path, x: str, y: str):
    if x in df.columns and y in df.columns:
        fig, ax = plt.subplots()
        sub = df[[x, y]].dropna()
        ax.scatter(sub[x], sub[y], s=10)
        ax.set_xlabel(x); ax.set_ylabel(y)
        ax.set_title(f"Scatter — {x} vs {y}")
        savefig_no_style(fig, outdir / f"scatter_{x}_vs_{y}.png")
        plt.close(fig)
