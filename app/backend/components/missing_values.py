import sys
import pandas as pd
import numpy as np
import json
from Exceptions.exception import CustomException

def find_missing_values(df):
    try:
        missing_values_report = {}
        for column in df.columns:
            missing_count = df[column].isnull().sum()
            missing_percentage = (missing_count / len(df)) * 100
            missing_values_report[column] = {
                'missing_count': int(missing_count),
                'missing_%': round(missing_percentage, 2)
            }
        return json.dumps(missing_values_report)
    except Exception as e:
        raise CustomException(e, sys)