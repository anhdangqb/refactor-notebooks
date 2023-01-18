from src.utils import (
    print_hello_world,
    print_hello_by_name,
    remove_null_col,
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
        assert remove_null_col(["CustomerID"], data_null).shape[0] == 2
