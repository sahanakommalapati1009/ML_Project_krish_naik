# Utils will have all the common functionalities which the entire project can use
import os
import sys
import numpy as np
import pandas as pd
import pickle
import dill
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))): # Looping through each and every model

            model = list(models.values())[i]

            para=param[list(models.keys())[i]] # Listed down all the parameters how we did did for models , this is for hyoer parameter tuning

            gs = GridSearchCV(model,para,cv=3) # is creating an instance of the GridSearchCV class, which is used for performing hyperparameter tuning by exhaustively searching over a specified parameter grid for the best model
            
            gs.fit(X_train,y_train)# training the model

            model.set_params(**gs.best_params_) # setting the parameter
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train) #doing the prediction on X_train

            y_test_pred = model.predict(X_test) #doing the prediction on X_test

            train_model_score = r2_score(y_train, y_train_pred) #computinh r2_score

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)