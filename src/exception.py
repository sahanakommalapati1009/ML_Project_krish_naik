# Any exception that is getting controlled, this sys library will automatically have that information
import sys 
from src.logger import logging

# Whenever an exception gets raised we want to push our own custom message
# we are giving 2 inputs, one is error and error_detail, this will be present on the sys
def error_message_detail(error, error_detail:sys):
    _,_,exc_tb=error_detail.exc_info() # This will give all the info like in which line the error occured, in which file etc
    file_name=exc_tb.tb_frame.f_code.co_filename
    # Write the error message which we want to display
    error_message="Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno,str(error)
    
    )
    return error_message


class CustomException(Exception):
    # A __init__ method is created within a class in Python to automatically initialize the attributes (variables) of an object 
    # whenever a new instance of that class is created, essentially acting as a constructor in other programming languages.
    def __init__(self, error_message,error_detail:sys):
        # super is commonly used in inheritance, allowing you to call methods from a parent class in a child class.
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    # The __str__ method is designed to return a human-readable, informal string representation of an object. 
    # This is useful for displaying information about the object in a way that makes sense to the end user, 
    # typically when using print() or str().
    def __str__(self):
        return self.error_message
    
# if __name__=="__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("Divide by zero")
#         raise CustomException(e,sys)
