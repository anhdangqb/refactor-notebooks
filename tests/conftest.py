import pytest
import pandas as pd
import numpy as np

# Fixture is used to create the test data to run test on functions
## Fixture is accessible across multiple test files (reuse the data)
## Decorator: turn the fixture function, into the object that test func can call as DF
@pytest.fixture
def data_null():
    return pd.DataFrame(
        {
            "CustomerID": ["1234", np.nan, "3456"],
            "Quantity": [30, 40, np.nan],
            "UnitPrice": [1, 2, 3],
        }
    )

@pytest.fixture
def data_for_winsorize():
    return pd.DataFrame(
        {
            "Quantity": [30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
            "UnitPrice": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        }
    )
