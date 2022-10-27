# take test.csv -> make_dataset -> build_features 
# predict using saved model from train_model.py

import sys
sys.path.append('../src')
sys.path.append('../models')
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from utils import *
from data.preprocess import *
import pandas as pd


@click.command()
@click.argument('models_dir', type=click.Path(exists=True))
@click.argument('inf_data_path', type=click.Path(exists=True)) 

def main(models_dir, inf_data_path):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('training model on final data')
    
    inf_data = pd.read_pickle(inf_data_path)
    model = load_model(models_dir + '/catboost.sav')
    y_pred = model.predict(inf_data)

    pred=pd.DataFrame(y_pred)
    sub_df=pd.read_csv(r'../data\raw\sample_submission.csv')
    datasets=pd.concat([sub_df['Id'],pred], axis=1)
    datasets.columns=['Id','SalePrice']
    datasets.to_csv('submission.csv',index=False)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
