import json
import sys
from components.missing_values import find_missing_values
from components.data_summary import get_data_summary
from components.detect_duplicates import detect_duplicates
from components.detetc_outliers import detect_outliers
from components.column_statistics import get_categorical_column_statistics,get_numeric_column_statistics
from utils.data_loader  import  load_data
from Exceptions.exception import CustomException

# dataset = load_data('C:/Users/HP/OneDrive/Desktop/ML_Exercies/movies.csv')
# print(find_missing_values(dataset))

class DataAnalyzer:
    def __init__(self):
        self.output = {}
        self.data = None

    def load_dataset(self,file_path):
        try:
            self.data = load_data(file_path)
        except Exception as e:
            raise CustomException(e,sys)
    
    def analyze_data_summary(self):
        try:
            self.output['data_summary'] = json.loads(get_data_summary(self.data))
        except Exception as e:
            raise CustomException(e,sys)
    
    def analyze_numeric_columns_statistics(self):
        try:
            self.output['numeric_columns_statistics'] = json.loads(get_numeric_column_statistics(self.data))
        except Exception as e:
            raise CustomException(e,sys)
        
    def analyze_categorical_columns_statistics(self):
        try:
            self.output['categorical_columns_statistics'] = json.loads(get_categorical_column_statistics(self.data))
        except Exception as e:
            raise CustomException(e,sys)

    def analyze_missing_values(self):
        try:
            self.output['missing_values'] = json.loads(find_missing_values(self.data))
        except Exception as e:
            raise CustomException(e,sys)
    
    def analyze_duplicates(self):
        try:
            self.output['duplicates'] = json.loads(detect_duplicates(self.data))
        except Exception as e:
            raise CustomException(e,sys)
    
    def analyze_outliers(self):
        try:
            self.output['outliers'] = json.loads(detect_outliers(self.data))
        except Exception as e:
            raise CustomException(e,sys)
    def return_output(self):
        return self.output

    
    def run_pipeline(self, file_path):
        try:
            self.load_dataset(file_path)
            self.analyze_data_summary()
            self.analyze_numeric_columns_statistics()
            self.analyze_categorical_columns_statistics()
            self.analyze_missing_values()
            self.analyze_duplicates()
            self.analyze_outliers()
            return self.return_output()
        except Exception as e:
            raise CustomException(e,sys)

if __name__=='__main__':
    file_path = 'C:/Users/HP/OneDrive/Desktop/ML_Exercies/movies.csv'
    analyzer = DataAnalyzer()
    print(analyzer.run_pipeline(file_path))