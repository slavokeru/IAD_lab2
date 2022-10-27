import pickle
from pandas import DataFrame


def save_as_pickle(df: DataFrame, path: str) -> None:
    df.to_pickle(path)

def save_model(model, path: str) -> None:
    pickle.dump(model, open(path, 'wb'))

def load_model(path: str):
    return pickle.load(open(path, 'rb'))
