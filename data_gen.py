import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_synthetic_transactions(n_rows: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=int(x)) for x in rng.integers(0, 240, size=n_rows)]
    transaction_id = np.arange(1, n_rows + 1)
    customer_id = rng.integers(1000, 3000, size=n_rows)
    regions = ["NA", "EU", "APAC", "LATAM"]
    region = rng.choice(regions, size=n_rows, p=[0.45, 0.25, 0.2, 0.1])
    channels = ["online", "retail", "partner"]
    channel = rng.choice(channels, size=n_rows, p=[0.55, 0.35, 0.10])
    categories = ["electronics", "apparel", "home", "beauty", "sports"]
    product_category = rng.choice(categories, size=n_rows)

    base_price = {"electronics": 220.0, "apparel": 45.0, "home": 80.0, "beauty": 30.0, "sports": 120.0}
    unit_price = np.array([rng.normal(loc=base_price[c], scale=base_price[c]*0.15) for c in product_category]).clip(1.0, None)
    quantity = rng.poisson(lam=2.2, size=n_rows) + 1
    discount_rate = np.clip(rng.beta(2, 12, size=n_rows), 0, 0.9)
    payment_types = ["card", "wallet", "bank_transfer", "cash"]
    payment_type = rng.choice(payment_types, size=n_rows, p=[0.6, 0.2, 0.15, 0.05])

    df = pd.DataFrame({
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "transaction_date": pd.to_datetime(dates).date,
        "region": region,
        "channel": channel,
        "product_category": product_category,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount_rate": discount_rate,
        "payment_type": payment_type,
    })

    # Introduce some missing values & anomalies
    mask_missing_price = rng.random(n_rows) < 0.02
    df.loc[mask_missing_price, "unit_price"] = np.nan
    mask_missing_disc = rng.random(n_rows) < 0.02
    df.loc[mask_missing_disc, "discount_rate"] = np.nan
    # A few extreme quantities
    outlier_idx = rng.choice(df.index, size=max(3, n_rows // 500), replace=False)
    df.loc[outlier_idx, "quantity"] *= rng.integers(8, 15, size=len(outlier_idx))
    return df
