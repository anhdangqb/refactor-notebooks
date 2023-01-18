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

def remove_null_col(df: pd.DataFrame, cols: list) -> pd.DataFrame:
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

def winsorize_series(s, q_cut=[0.05, 0.95]):
    q = s.quantile(q_cut)
    if isinstance(q, pd.Series) and len(q) == 2:
        s[s < q.iloc[0]] = q.iloc[0]
        s[s > q.iloc[1]] = q.iloc[1]
    return s

def cap_floor_series(s, flr_cap):
    if isinstance(s, pd.Series) and len(flr_cap) == 2:
        s[s < flr_cap[0]] = flr_cap[0]
        s[s > flr_cap[1]] = flr_cap[1]
    return s