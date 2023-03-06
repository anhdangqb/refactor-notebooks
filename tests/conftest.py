import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def data_with_null():
    return pd.DataFrame(
        {
            "CustomerID": ["1234", np.nan, "3456"],
            "Quantity": [30, 40, np.nan],
            "UnitPrice": [10, 20, 30],
        }
    )


@pytest.fixture
def data_with_outliers():
    return pd.DataFrame(
        {
            "Quantity": [30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
            "UnitPrice": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        }
    )


@pytest.fixture
def outlier_policies():
    return {
        "Quantity": [0, 40],
        "UnitPrice": [0, 5],
    }
