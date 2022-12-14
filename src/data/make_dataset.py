# -*- coding: utf-8 -*-
import click
import logging
import sys

sys.path.append('../src')
sys.path.append('../data')
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
# from ..utils import save_as_pickle
# from src.utils import save_as_pickle
from utils import save_as_pickle
from config import CATBOOST_NUM_COLS, CAT_COLS

# import src 
from preprocess import preprocess, preprocess_target, extract_target
import pandas as pd



@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_data_filepath', type=click.Path())
@click.argument('output_target_filepath', type=click.Path())
def main(input_filepath, output_data_filepath, output_target_filepath=None):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    df = pd.read_csv(input_filepath)
    df = preprocess(df)

    if len(output_target_filepath) > 1:
        df = preprocess_target(df)
        df, target = extract_target(df)
        save_as_pickle(target, output_target_filepath)
    df = df[CATBOOST_NUM_COLS + CAT_COLS]
    save_as_pickle(df, output_data_filepath)

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
