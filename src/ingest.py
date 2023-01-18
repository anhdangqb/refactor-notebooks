from utils import winsorize_series, cap_floor_series
from utils import remove_null_col
import pandas as pd

REMOVE_NULL_COLS = ["CustomerID"]
INGEST_DTYPES = {"CustomerID": str}
# WINSORIZE_COLS = ["Quantity", "UnitPrice"]
# Q_CUT = [0.05, 0.95]
OUTLIER_POLICY = {
    'use_winsorize': False,
    'q_cut': [0.05, 0.95],
    'outliers_cols': {
        "Quantity": [0, 40],
        'UnitPrice': [0, 10]
    }
}


def ingest_clean_data(
    raw_path: str,
    rm_null_cols=REMOVE_NULL_COLS,
    ingest_dtype_dict=INGEST_DTYPES,
    # winsorize_cols=WINSORIZE_COLS,
    # q_cut=Q_CUT,
    # use_winsorize=True,
    outlier_policy=OUTLIER_POLICY,
) -> pd.DataFrame:
    """Ingest function for Online Retail data
    1. Ingest excel file
    2. Remove nulls
    3. Winsorize
    4. Calculate order value
    Args:
        - raw_path: str
        - rm_null_cols: list
        - ingest_dtype_dict: dict
        - outlier_policy: dict
    Return:
        - pd.DataFrame
    """
    # TODO: Parameterize into config
    # Take parameters from policy

    df = pd.read_excel(raw_path, dtype=ingest_dtype_dict)
    df = remove_null_col(df, rm_null_cols)

    if outlier_policy['use_winsorize']:
        winsorize_cols = outlier_policy['outliers_cols'].keys()
        q_cut = outlier_policy['q_cut']
        df = winsorize_df(df, winsorize_cols, q_cut)
    else:
        for col, policy in outlier_policy['outliers_cols'].items():
            df[col] = cap_floor_series(df[col].copy(), policy)

    df["order_value"] = df["order_value"] = df.Quantity * df.UnitPrice
    df.dropna(inplace=True)
    return df


def winsorize_df(df, w_cols: list, q_cut=[0.05, 0.95]):
    for col in w_cols:
        df[col] = winsorize_series(df[col].copy(), q_cut)
    return df
