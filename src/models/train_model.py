# -*- coding: utf-8 -*-
import sys

sys.path.append('../src')
sys.path.append('../data')

import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from sklearn.model_selection import train_test_split
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error
import config as cfg
import json 
from utils import *



@click.command()
@click.argument('train_data_filepath', type=click.Path(exists=True)) 
@click.argument('target_data_filepath', type=click.Path(exists=True)) 
@click.argument('output_model_filepath', type=click.Path()) 
def main(train_data_filepath, target_data_filepath, output_model_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    train = pd.read_pickle(train_data_filepath)
    target = pd.read_pickle(target_data_filepath)

    X_train, X_val, y_train, y_val = train_test_split(train, target, train_size=0.8, random_state=42)

    metrics = {}

    model = CatBoostRegressor(
            learning_rate=0.01,
            early_stopping_rounds=200,
            verbose=100,
            eval_metric='RMSE',
            )

    model.fit(X_train, y_train, eval_set=(X_val, y_val), cat_features=cfg.CAT_COLS)
    save_model(model, output_model_filepath + '/catboost.sav')

    y_pred = model.predict(X_val)
    metrics['rmse'] = mean_squared_error(y_val, y_pred, squared=False)

    with open("metrics.json", "w") as outfile:
        json.dump(metrics, outfile)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
