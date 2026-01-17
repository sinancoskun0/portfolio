import numpy as np
from src.statistics import summary_stats


def test_summary_stats_keys():
    data = np.random.rand(10, 100)
    stats = summary_stats(data)
    assert "mean_final_price" in stats
