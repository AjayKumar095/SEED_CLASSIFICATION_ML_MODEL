from sklearn.model_selection import train_test_split
from DataBase.DataQuery import insert_data
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from utils.logger import logging
import pandas as pd 
import os


class DataIntake:
    
    def __init__(self) -> None:
        pass

    def split_data(self, row_data_path: str)-> str:
        
        directory='artifacts/Data'
        os.makedirs(directory, exist_ok=True)
        
        logging.info('Checking the file type in DataIntake Class.')
        if row_data_path.endswith('.csv'):
            df=pd.read_csv(row_data_path)
            logging.info('Reading the file as Pandas dataframe.')
            X=df.iloc[:,:-1]
            y=df['seedType']

            # Split the data into training and test sets
            logging.info('Split the data into training and test sets.')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            test_df=pd.concat([X_test, y_test], axis=1)
            train_df=pd.concat([X_train, y_train], axis=1)
            
            logging.info('Saving the data into training and test sets.')
            TestDataFilePath=os.path.join(directory, 'TestData.csv')
            TrainDataFilePath=os.path.join(directory, 'TrainData.csv')
            
            logging.info('Converting the train df and test df into csv file.')
            test_df.to_csv(TestDataFilePath, sep=',', index=False)
            train_df.to_csv(TrainDataFilePath, sep=',', index=False)
            
            logging.info('Returning the file path of Train and Test datasets.')
            return (TrainDataFilePath, TestDataFilePath)
        else:
            logging.info('File must be .csv')
            return 
    
    
class DataCleaning(DataIntake):
    def __init__(self) -> None:
        super().__init__()
      
    def clean_data(self, row_data_path):
        #directory='artifacts/Data'
        #os.makedirs(directory, exist_ok=True)
        
        logging.info('Checking the file type in DataIntake Class.')
        if row_data_path.endswith('.csv'):
            row_df=pd.read_csv(row_data_path)
            
            if not pd.api.types.is_numeric_dtype(row_df['seedType']):
                seed_type_mapping = {
                                   'Kama': 1,
                                   'Rosa': 2,
                                   'Canadian': 3
                               }
                row_df['seedType']=row_df['seedType'].map(seed_type_mapping)
                
            pipeline=Pipeline([
                ('imputer', SimpleImputer(strategy='median'))
            ])
            
            cleaned_df=pd.DataFrame(pipeline.fit_transform(row_df), columns=row_df.columns)
            res =insert_data(clean_df=cleaned_df)
            return res
           
         
print(DataCleaning().clean_data('artifacts\Data\seed_dataset.csv'))    

        
    
    
     