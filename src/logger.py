# Logger is for the purpose that any exception happens, we should log all those information, 
# execution everything in files so that we are able to track if there are some errors
import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE)
os.makedirs(logs_path,exist_ok=True)# THis says that even though there are files, just keep on appending the files
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO, #This means that wherever we are using logging.INFO this will use this kind of basic config 


)

if __name__=="__main__":
    logging.info("logging has started")