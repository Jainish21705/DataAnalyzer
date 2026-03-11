import sys
import pandas as pd
import numpy as np
import json
from Exceptions.exception import CustomException

def get_numeric_column_statistics(df):
    numeric_columns = [column for column in df.select_dtypes(include=['float64','int64'])]
    numeric_columns_report = {}
    for column in numeric_columns:
        numeric_columns_report[column] = df[column].describe().to_dict()
        numeric_columns_report[column].update({"skewness":float(round(df[column].skew(),3))})
    
    return json.dumps(numeric_columns_report)

def get_categorical_column_statistics(df):
    categorical_columns = [column for column in df.select_dtypes(include=['str','object'])]
    categorical_columns_report = {}
    for column in categorical_columns:
        categorical_columns_report[column] = {"num_unique_values":df[column].nunique()}
        categorical_columns_report[column].update({"most_frequent":df[column].value_counts().index[0]})
        categorical_columns_report[column].update({"frequent_count":int(df[column].value_counts().iloc[0])})
    
    return json.dumps(categorical_columns_report)
    
