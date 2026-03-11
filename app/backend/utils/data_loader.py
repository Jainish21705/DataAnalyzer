import sys
import pandas as pd
from Exceptions.exception import CustomException

def load_data(path):
    try:
        if path.endswith('.csv'):
            df = pd.read_csv(path)
            return df
        else:
            df = pd.read_excel(path)
            return df
    except Exception as e:
        raise CustomException(e, sys)