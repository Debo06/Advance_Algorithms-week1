import pandas as pd

def impute_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "unit_price" in df.columns and "product_category" in df.columns:
        df["unit_price"] = df["unit_price"].fillna(df.groupby("product_category")["unit_price"].transform("median"))
    if "discount_rate" in df.columns and "channel" in df.columns:
        df["discount_rate"] = df["discount_rate"].fillna(df.groupby("channel")["discount_rate"].transform("median"))
    for c in ["unit_price", "discount_rate"]:
        if c in df.columns:
            df[c] = df[c].fillna(df[c].median())
    return df

def cap_outliers_iqr(df: pd.DataFrame, col: str, k: float = 1.5) -> pd.DataFrame:
    df = df.copy()
    q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - k * iqr, q3 + k * iqr
    df[col] = df[col].clip(lower=lo, upper=hi)
    return df

def rule_bound(df: pd.DataFrame, col: str, lo: float, hi: float) -> pd.DataFrame:
    df = df.copy()
    df[col] = df[col].clip(lower=lo, upper=hi)
    return df

def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "quantity" in df.columns:
        df = cap_outliers_iqr(df, "quantity", k=1.5)
    if "unit_price" in df.columns:
        df = cap_outliers_iqr(df, "unit_price", k=1.5)
    if "discount_rate" in df.columns:
        df = rule_bound(df, "discount_rate", 0.0, 0.9)
    return df
