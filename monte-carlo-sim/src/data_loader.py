import pandas as pd
from pathlib import Path


def load_price_data(csv_path: str) -> pd.Series:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(
        path,
        sep=";",                # <-- important
        decimal=".",            # explicit, though default
        parse_dates=["Datum"]
    )

    df = df.sort_values("Datum")

    prices = df["Schlusskurs"].astype(float)

    prices.index = df["Datum"]
    prices.name = "Adj Close"

    return prices
