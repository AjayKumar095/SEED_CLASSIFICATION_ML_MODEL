from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from utils.Helper import save_model, load_model
from ModelComponents import DataIntake
from utils.logger import logging
from sklearn.svm import SVC
import pandas as pd
import warnings
import os

warnings.filterwarnings('ignore')
class ModelTrainer:
    
    def __init__(self) -> None:
        pass
    logging.info('Model Trainer Class.')
    def TrainModel(self):
        
        logging.info('Getting the data.')
        Data=DataIntake()
        row_data_file_path='artifacts\Data\seed_dataset.csv'
        train_df_filepath, test_df_filepath=Data.split_data(row_data_path=row_data_file_path)
        logging.info('Getting the train and test data file path.')
        
        logging.info('Reading the data into csv file in pandas dataframe.')
        train_df=pd.read_csv(train_df_filepath)
        test_df=pd.read_csv(test_df_filepath)
        
        logging.info('Split the data into training and test sets.')
        X_train=train_df.iloc[:,:-1]
        y_train=train_df['seedType']
        
        X_test=test_df.iloc[:,:-1]
        y_test=test_df['seedType']
        
        logging.info('Creating the SVC model.')
        SVC_Model=SVC(C=100, kernel='linear', probability=True)
        SVC_Model.fit(X_train, y_train)
        
        logging.info('Predicting the test data.')
        y_pred=SVC_Model.predict(X_test)
        
        logging.info('Checking various matrix for model performance.')
        accuracy=accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        
        Model_matrix={
            'Accuracy': accuracy,
            'Presision': precision,
            'Recall': recall,
            'f1_score': f1,
            'Confusion Matrix': conf_matrix
        }
        logging.info(f'Model Performace Details:\n {str(Model_matrix)}')
        
        ModelFilePath=save_model('SVC_model.pkl', model_obj=SVC_Model)
        logging.info('Returning the model file path after saving the model.')
        return ModelFilePath
        
class PredictionPipeline():
    def __init__(self) -> None:
        pass
    
    logging.info('Prediction Pipeline Class.')
    def Prediction(self, newdata):
        logging.info('Getting the model object and loading for predicting new datapoints.')
        Trainer=ModelTrainer()
        modelfilepath=Trainer.TrainModel()
        model=load_model(modelfilepath)
        
        logging.info('Predicting the new data points.')
        pred=model.predict(newdata)
        logging.info(f'Model classification for new data point {pred}.')
        return pred
        
            