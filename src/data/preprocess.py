import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
import config as cfg
from sklearn.feature_selection import SelectKBest, f_regression


def set_idx(df: pd.DataFrame, idx_col: str) -> pd.DataFrame:
    df = df.set_index(idx_col)
    return df

def process_binary(df: pd.DataFrame) -> pd.DataFrame:
    df[cfg.BIN_COL] = df[cfg.BIN_COL].map(dict(Y=1, N=0))
    return df

def replace_nans(df: pd.DataFrame) -> pd.DataFrame:
    df = df.fillna(0)
    return df

def process_rate_cat_cols(df: pd.DataFrame) -> pd.DataFrame:
    df[['FireplaceQu', 'KitchenQual', 'ExterQual', 'ExterCond','BsmtQual', 'BsmtCond', 'HeatingQC', 'GarageQual', 'GarageCond']] \
    = df[['FireplaceQu', 'KitchenQual', 'ExterQual', 'ExterCond','BsmtQual', 'BsmtCond', 'HeatingQC', 'GarageQual', 'GarageCond']] \
        .replace(['Ex', 'Gd', 'TA', 'Fa', 'Po'], [5,4,3,2,1])
    df[['BsmtExposure']] = df[['BsmtExposure']].replace(['Gd', 'Av', 'Mn', 'No'], [4,3,2,1])
    df[['BsmtFinType1', 'BsmtFinType2']] = df[['BsmtFinType1', 'BsmtFinType2']].replace(['GLQ', 'ALQ', 'BLQ', 'Rec', 'LwQ', 'Unf'], [6,5,4,3,2,1])
    df[['GarageFinish']] = df[['GarageFinish']].replace(['Fin', 'RFn', 'Unf'], [3,2,1])

    return df

def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    df[cfg.CAT_COLS] = df[cfg.CAT_COLS].astype('category') # +
    df[cfg.RATE_CAT_COLS] = df[cfg.RATE_CAT_COLS].astype(np.int32) # +
    df[cfg.RATE_COLS] = df[cfg.RATE_COLS].astype(np.int32) # +
    df[cfg.BIN_COL] = df[cfg.BIN_COL].astype(np.int32) # +
    df[cfg.DISCRETE_COLS] = df[cfg.DISCRETE_COLS].astype(np.int32) # +
    df[cfg.REAL_COLS] = df[cfg.REAL_COLS].astype(np.int32)
    
    return df

def drop_nan_cols(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    df = df.drop(cols, axis=1)
    return df

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = set_idx(df, cfg.ID_COL)
    df = drop_nan_cols(df, cfg.NAN_COLS)
    df = process_binary(df)
    df = replace_nans(df)
    df = process_rate_cat_cols(df)
    df = cast_types(df)
    return df

def extract_target(df: pd.DataFrame):
    df, target = df.drop(cfg.TARGET_COL, axis=1), df[cfg.TARGET_COL]
    return df, target

def preprocess_target(df: pd.DataFrame) -> pd.DataFrame:
    df[cfg.TARGET_COL] = df[cfg.TARGET_COL].astype(np.int32)
    return df

def select_features(df: pd.DataFrame, target: pd.Series):
	fs = SelectKBest(score_func=f_regression, k=20)
	fs.fit(df, target)
	cols = fs.get_support(indices=True)
	df_fs = df.iloc[:,cols]

	return df_fs, fs