import pytest
from src.data_loader import load_price_data


def test_load_price_data():
    series = load_price_data("data/AAPL.csv")
    assert not series.empty
