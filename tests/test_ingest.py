# import pytest
# import pandas as pd
# import numpy as np
from src.ingest import winsorize_df

class TestWinsorizeDf:
    def test_winsorize_df_one_col(self, data_for_winsorize):
        assert winsorize_df(data_for_winsorize, ["Quantity"]).min().Quantity > 30
    def test_winsorize_df_two_cols(self, data_for_winsorize):
        assert winsorize_df(data_for_winsorize, ["Quantity", "UnitPrice"]).min().Quantity > 30
        assert winsorize_df(data_for_winsorize, ["Quantity", "UnitPrice"]).min().UnitPrice > 1