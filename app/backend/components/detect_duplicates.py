import sys
import pandas as pd
import numpy as np
import json
from Exceptions.exception import CustomException

def detect_duplicates(df):
    try:
        duplicate_report = {}
        for column in df.columns:
            duplicate_count = sum(df[column].duplicated())
            duplicate_percentage = (duplicate_count/len(df))
            duplicate_report[column] = {
                "duplicate_count": int(duplicate_count),
                "duplicate_%":round(duplicate_percentage,2)
            }
        return json.dumps(duplicate_report)
    except Exception as e:
        raise CustomException(e, sys)   