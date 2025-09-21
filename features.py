import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["line_total"] = df["quantity"] * df["unit_price"] * (1 - df["discount_rate"])
    df["is_weekend"] = df["transaction_date"].dt.weekday >= 5

    df = df.sort_values(["customer_id", "transaction_date"])
    df["days_since_prev_txn"] = df.groupby("customer_id")["transaction_date"].diff().dt.days
    df["days_since_prev_txn"] = df["days_since_prev_txn"].fillna(df["days_since_prev_txn"].median())

    df["txn_count_30d"] = 0
    df["basket_value_30d"] = 0.0
    for cust, sub in df.groupby("customer_id", group_keys=False):
        s = sub.copy()
        cnts, vals = [], []
        for _, row in s.iterrows():
            past = s[(s["transaction_date"] < row["transaction_date"]) & (s["transaction_date"] >= (row["transaction_date"] - pd.Timedelta(days=30)))]
            cnts.append(len(past))
            vals.append(past["line_total"].sum())
        df.loc[s.index, "txn_count_30d"] = cnts
        df.loc[s.index, "basket_value_30d"] = vals
    return df

def scale_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    numeric_cols = ["quantity", "unit_price", "discount_rate", "line_total", "days_since_prev_txn", "txn_count_30d", "basket_value_30d"]
    present = [c for c in numeric_cols if c in df.columns]

    std_cols = [c for c in present if c != "discount_rate"]
    mm_cols = ["discount_rate"] if "discount_rate" in present else []

    if std_cols:
        std = StandardScaler()
        df[[f"{c}_std" for c in std_cols]] = std.fit_transform(df[std_cols])
    if mm_cols:
        mm = MinMaxScaler()
        df[[f"{c}_mm" for c in mm_cols]] = mm.fit_transform(df[mm_cols])
    return df
