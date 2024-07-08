from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from utils.logger import logging
import sqlite3 as sql
import pandas as pd 
import os


class DataIntake:
    
    def __init__(self) -> None:
        pass

    def split_data(self)-> str:
        
        directory='artifacts/Data'
        os.makedirs(directory, exist_ok=True)
        
        logging.info('Checking the file type in DataIntake Class.')
        try:
             ## Database Config
            Database_path=DataBase().get_dataBase_path()
            logging.info(Database_path)
            connection=sql.connect(Database_path)
            #cursor=connection.cursor()
            
            
            query = "SELECT * FROM Seed_Data_"
            df=pd.read_sql_query(query, connection)
            logging.info(f'{str(df.head())}')
            logging.info('Reading the file as Pandas dataframe.')
            X=df.iloc[:,:-1]
            y=df['seedType']

            # Split the data into training and test sets
            logging.info('Split the data into training and test sets.')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            test_df=pd.concat([X_test, y_test], axis=1)
            train_df=pd.concat([X_train, y_train], axis=1)
    
            logging.info('Returning the  Train and Test dataframe.')
            return (train_df, test_df)
        
        except Exception as e:
            return e
        
    
class DataCleaning():
    def __init__(self) -> None:
        pass
      
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
           
            return cleaned_df
    
class DataBase:
    def __init__(self) -> None:
                    ## Database Config
        self.__Database_path='DataBase\SeedDataBase.db'
        self.__connection=sql.connect(self.__Database_path)
        self.__cursor=self.__connection.cursor()
    
    def insert_data(self, row_data_path):
        try:
            Data=DataCleaning()
            
            clean_df=Data.clean_data(row_data_path)
            
            if not clean_df.empty:
            
                table='Seed_Data_'
                columns=', '.join(clean_df.columns)
                placeholders = ', '.join(['?'] * len(clean_df.columns))
                sql_insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
                for row in clean_df.itertuples(index=False, name=None):
                    self.__cursor.execute(sql_insert_query, row)
                
                self.__connection.commit()
                self.__connection.close()
                return 
            else:
                return 'Data insertion failed'
        except Exception as e:
            return f'Error occure {e}'     
    
    def get_dataBase_path(self):
        try:
            return self.__Database_path
        except Exception as e:
            return e 


        
    
    
     