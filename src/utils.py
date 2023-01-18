"""This is to test."""
import pandas as pd


def print_hello_world() -> str:
    return "Hello World"


def print_hello_by_name(name: str) -> str:
    """
    This is an example functions to test.
    Args:
        - name: str
    Returns:
        - str
    """
    if name:
        return f"Hello {name}"
    else:
        # return "Sorry, no name provided."
        raise Exception("Sorry, no name provided.")


def remove_null_col(cols: list, df: pd.DataFrame) -> pd.DataFrame:
    """
    Take a list of cols name and remove any row with null in that col from the dataframe.
    Args:
        - cols: list
        - df: pd.DataFrame
    Returns:
        - pd.DataFrame
    """
    for col in cols:
        if col not in df.columns:
            raise Exception(f"Sorry, {col} is not in the dataframe.")
        else:
            df = df[~df[col].isnull()].copy()
    return df
