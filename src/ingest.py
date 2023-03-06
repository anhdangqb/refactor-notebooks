"""Functions for ingesting data"""
from typing import Dict

import pandas as pd

# OUTLIER_POLICY = {
#     "Quantity": [0, 40],
#     "order_value": [0, 60],
# }


def process_data(
    df: pd.DataFrame, null_cols: list, outliers_cols: Dict
) -> pd.DataFrame:
    """Process data for analysis
    1. Remove null values
    2. Remove outliers
    3. Transform date columns
    Args:
        - df (pd.DataFrame): Dataframe to process
    Return:
        - df (pd.DataFrame): Processed dataframe
    """
    df = remove_null(df, null_cols)
    df = treat_outlier_df(df, outliers_cols)
    # TODO: df = transform_date_cols(df)
    return df


def remove_null(df: pd.DataFrame, cols_ls: list) -> pd.DataFrame:
    """Remove null values from CustomerID column"""
    for col in cols_ls:
        if col not in df.columns:
            raise Exception(f"{col} not in df.columns")
        else:
            df = df[~df[col].isnull()].copy()
    return df


def treat_outlier_series(s: pd.Series, cap_flr: list) -> pd.Series:
    """Treat outlier in a series
    Args:
        - s (pd.Series): Series to treat
        - cap_flr (list): List of cap and floor values
    Return:
        - s (pd.Series): Series with outliers treated
    """
    s = s.clip(cap_flr[0], cap_flr[1])
    return s


def treat_outlier_df(df: pd.DataFrame, outlier_policies: Dict) -> pd.DataFrame:
    """Treat outlier in a series
    Args:
        - df (pd.DataFrame): DataFrame to treat
        - outlier_policies (Dict): Dictionary of outlier policies
    Return:
        - df (pd.DataFrame): DataFrame with outliers treated
    """
    for col, cap_flr in outlier_policies.items():
        df[col] = treat_outlier_series(df[col], cap_flr)
    return df
