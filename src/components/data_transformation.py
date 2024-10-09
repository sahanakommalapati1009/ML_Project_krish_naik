# The main purpose of data transformation is basically to do feature engineering, data cleaning.
# if we really want to change some of my dataset
# Convert my categorical features into numerical features we can do it from data transformation

import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
# column transformer is used to create pipeline using onehot encoder, stanadard scaler etc
from sklearn.impute import SimpleImputer # This is used for missing vales
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# Similar to data ingestion we are creating inputs for data transformation using this class
@dataclass
class DataTransfromationConfig:
    # Lets say we want to create any models and want to save that into a pickle file for that we require any one kind of path
    # Pickling is the process of converting a Python object into a byte stream, which can then be saved to a file. 
    # Unpickling is the reverse process: converting the byte stream back into a Python object.
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransfromationConfig()
    
    # We are creating this function this is just to create all my pickle files which are responsible for converting 
    # categorical features into numerical and standardscaler etc

    def get_data_transformer_object(self):

        '''
        This function is responsible for data transformation based on different types of data
        '''
        try:
            numerical_columns=["writing_score","reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Creating numerical pipeline
            # We have 2 steps here by creating a pipeline 1st we have handled a missing values using a particular stratergy called median
            # Then we are dooing the standard scaling
            # This pipeline needs to run on the training dataset like fit_transform on training dataset and just do transform on the test dataset
            num_pipeline= Pipeline(
                steps=[
                    # stratergy we are using it as median because we saw in numerical features that we have some outliers in EDA
                    ("imputer",SimpleImputer(strategy="median")),# handling missing values
                    # Tring to handle standard scaler
                    ("scaler", StandardScaler())
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),# Here we are using mode as the strategy
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("numerical columns standard scaling completed")
            logging.info("categorical columns encoding completed")

            # Combining this numerical pipeline and cat_pipeline using column transformer
            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor
            
            
        except Exception as e:
            raise CustomException(e,sys)
    
    # Starting our data transformation inside this function
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df=pd.read_csv(train_path) # reading training data
            test_df=pd.read_csv(test_path)

            logging.info("Reading train and test data completed")
            logging.info("Obtaining preprocessing object")
            preprocessing_obj=self.get_data_transformer_object()
            target_column_name="math_score"
            numerical_columns=["writing_score","reading_score"]

        
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]


            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            # Calling the pickle file and we are doing fit_transform
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e,sys)
            
            
