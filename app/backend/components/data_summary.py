import sys
import pandas as pd
import numpy as np
import json
from Exceptions.exception import CustomException

def get_data_summary(df):
    try:
        summary = {
            'num_rows': df.shape[0],
            'num_columns': df.shape[1],
            'column_names': df.columns.tolist(),
            'data_types': df.dtypes.apply(lambda x: x.name).to_dict(),
        }
        return json.dumps(summary)
    except Exception as e:
        raise CustomException(e, sys)   