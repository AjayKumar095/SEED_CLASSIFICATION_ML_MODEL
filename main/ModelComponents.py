from sklearn.model_selection import train_test_split
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
    
    
    
     
        
        
        
    
    
     