#from logger import logging
import pickle as pkl
import os


def save_model(filename:str, model_obj:object):
    
    directory='artifacts\Model'
    os.makedirs(directory, exist_ok=True)
    ModelFilePath=os.path.join(directory, filename)
    
    with open(ModelFilePath, 'wb') as file:
        pkl.dump(obj=model_obj, file=file)

    return ModelFilePath

def load_model(ModelFilePath:str):
    
    with open(ModelFilePath, 'rb') as file:
        model=pkl.load(file)
        return model