# Most of the time when we are working as a data scientist, for any probblem statement that we really want to solve we require data.
# In we are working in a bigger team. We will be having a separate big data team.
# They will be maaking sure that they will collect data from different sources and probably storing it in some databases, in hadoop, in mongodb or it can be stored in any kind of data sources.
# We as a data scientist we should particularly read the dataset from the data source.


import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransfromationConfig

# In data ingestion whenever we are performing the data ingestion component  there should be some inputs that may be probably required by the data ingestion component.
# The input can be like where  have to save the train data, test data, raw data. 
# So those kind of input will be basically be creating in another class called DataIngestionConifg

@dataclass # if we try to use this dataclass we will be directly able to define our class variable
class DataIngestionConfig:
    # Any input required will be given through this class
    # creating a train_data_path class varaible of string type and creating some path to store the artifact folder and all the output will be stored in artifact folder and train.csv file
    train_data_path: str=os.path.join('artifacts','train.csv')
    test_data_path: str=os.path.join('artifacts','test.csv')
    raw_data_path: str=os.path.join('artifacts','raw_data.csv')


# If you are using only data variables you can use dataclass
# If you are defining some functions its better to use __init__
class DataIngestion:
    def __init__(self):
        # This will consists of all the three inputs given
        self.ingestion_config=DataIngestionConfig() # AS soon as dataIngestionConfig is called these three paths will be saved inside this particular class variable.

    def initiate_data_ingestion(self):
        # This function is used to read the data from the partcular database, that code should be written here
        logging.info("Entered the data Ingestion method or component")
        try:
            df=pd.read_csv('notebook\data\student_performance_indicator.csv')
            logging.info('Read the dataset as dataframe')
            # I already know the path of training data like my path will be artifacts/traiin.csv
            # This artifacts is the folder so lets go ahead and create these folders with the help of training, testing and raw data path.
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False, header=True)
            logging.info("train Test split initiated")
            train_set, test_set=train_test_split(df, test_size=0.2,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False, header=True)
            logging.info("Ingestion of the data is completed")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e,sys)
        

if  __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)

