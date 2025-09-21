import argparse
from pathlib import Path
import sys

# Allow running as a script without package context
_THIS = Path(__file__).resolve()
sys.path.append(str(_THIS.parent))

import pandas as pd  # noqa
from utils import ensure_dirs  # noqa
import data_gen  # noqa
import eda  # noqa
import cleaning  # noqa
import features  # noqa

def run_pipeline(mode: str, rows: int, input_path: str):
    artifacts_dir, data_dir = ensure_dirs()

    if mode == "synthetic":
        df = data_gen.generate_synthetic_transactions(n_rows=rows, seed=42)
        raw_path = data_dir / "raw_transactions.csv"
        df.to_csv(raw_path, index=False)
    elif mode == "csv":
        raw_path = Path(input_path)
        if not raw_path.exists():
            raise FileNotFoundError(f"CSV not found: {raw_path}")
        df = pd.read_csv(raw_path)
    else:
        raise ValueError("mode must be 'synthetic' or 'csv'")

    eda.basic_overview(df, artifacts_dir)
    eda.plot_histograms(df, artifacts_dir, cols=["quantity", "unit_price", "discount_rate"])
    eda.plot_boxplots(df, artifacts_dir, cols=["quantity", "unit_price"])
    if "unit_price" in df.columns and "quantity" in df.columns:
        eda.plot_scatter(df, artifacts_dir, x="unit_price", y="quantity")

    df_clean = cleaning.impute_missing(df)
    df_clean = cleaning.handle_outliers(df_clean)
    clean_path = data_dir / "cleaned_transactions.csv"
    df_clean.to_csv(clean_path, index=False)

    df_feat = features.engineer_features(df_clean)
    df_feat = features.scale_features(df_feat)
    feat_path_csv = data_dir / "engineered_features.csv"
    df_feat.to_csv(feat_path_csv, index=False)
    try:
        df_feat.to_parquet(data_dir / "engineered_features.parquet", index=False)
    except Exception:
        pass

    print(f"Raw: {raw_path}")
    print(f"Cleaned: {clean_path}")
    print(f"Features (CSV): {feat_path_csv}")
    print(f"Artifacts (plots, summaries): {artifacts_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Week 1 EDA → Cleaning → Features → Scaling pipeline')
    parser.add_argument('--mode', choices=['synthetic', 'csv'], default='synthetic')
    parser.add_argument('--rows', type=int, default=1000, help='Rows for synthetic generation')
    parser.add_argument('--input_path', type=str, default='data/raw_transactions.csv', help='Used when mode=csv')
    args = parser.parse_args()
    run_pipeline(args.mode, args.rows, args.input_path)
