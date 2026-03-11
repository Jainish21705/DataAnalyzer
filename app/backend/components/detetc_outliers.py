import sys
import pandas as pd
import numpy as np
import json
from Exceptions.exception import CustomException

def detect_outliers(df):
    try:
        outlier_report = {}
        for column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce')
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            upper_limit = Q3 + 1.5 * IQR
            lower_limit = Q1 - 1.5 * IQR

            outlier_count = df[
            (df[column] > upper_limit) | (df[column] < lower_limit)
                ].shape[0]
            
            outlier_percentage = (outlier_count/len(df))
            outlier_report[column] = {
                "outlier_count": int(outlier_count),
                "outlier_%":round(outlier_percentage,5)
            }
        return json.dumps(outlier_report)
    except Exception as e:
        raise CustomException(e, sys)   