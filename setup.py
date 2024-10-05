# find_pacages will automatically find all the packages present in our application
from setuptools import find_packages,setup
# importing the List
from typing import List
# creating a function and giving input variables as file_path which is a string which gives the output as the list.
# In short this function will return a list of libraries 


HYPEN_E_DOT='-e .'


def get_requirements(file_path:str)->List[str]:
    '''
    This function will return the list of requirements
    '''
    requirements=[] #creating an empty list
    with open(file_path) as file_obj: #opening the file
        requirements=file_obj.readlines() #reading the file from line by line
        # we will have a new line in the requirements.txt file, so replacing that with an empty string
        requirements=[req.replace("\n","") for req in requirements]

        # while reading this requirement file as a list that -e . will also come that should not come so we write a condition for that
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

    

# setup contains the metadata information
setup(
name='ML_Project',
version='0.0.1',
author='Sahana Kommalapati',
author_email='sahanakommalapati1009@gmail.com',
packages= find_packages(),
#install_requires=['pandas','numpy','seaborn'], we cant write all the packages like this since we require a thousands of 
# libraries so we create a function get_requirements under requirements.txt
install_requires=get_requirements('requirements.txt')
)
