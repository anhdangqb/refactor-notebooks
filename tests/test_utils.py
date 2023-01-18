from src.utils import (
    print_hello_world,
    print_hello_by_name,
    remove_null_col,
    winsorize_series,
    cap_floor_series,
)
import pytest
import pandas as pd
import numpy as np


class TestHelloWorld:
    def test_print_hello_world(self):
        assert print_hello_world() == "Hello World"

    def test_print_hello_by_name(self):
        assert print_hello_by_name("John") == "Hello John"

    def test_print_hello_by_name_with_no_name(self):
        with pytest.raises(Exception):
            print_hello_by_name("")


class TestRemoveNull:
    def test_remove_null_col(self, data_null):
        # data_null is from conftest.py
        assert remove_null_col(data_null, ["CustomerID"]).shape[0] == 2

    def test_remove_null_cols(self, data_null):
        assert remove_null_col(data_null, ["CustomerID", "Quantity"]).shape[0] == 1


class TestWinsorzieSeries:
    def test_winsorize_series_flr(self, data_for_winsorize):
        assert winsorize_series(data_for_winsorize["Quantity"]).min() > 30
    def test_winsorize_series_cap(self, data_for_winsorize):
        assert winsorize_series(data_for_winsorize["Quantity"]).max() < 120

class TestCapFloorSeries:
    def test_cap_floor_series_flr(self, data_for_winsorize):
        assert cap_floor_series(data_for_winsorize["Quantity"], [50, 100]).max() == 100