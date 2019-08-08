# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to 
import pandas as pd
import datetime
import numpy as np
from string import digits

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None, dataframe2 = None):

    # Execution logic goes here
    print('Input pandas.DataFrame #1:\r\n\r\n{0}'.format(dataframe1))
    singaporeHousing = dataframe1
    singaporeHousing["AgeOfBuilding"]=[(2019-year) for year in singaporeHousing["LEASE_COMMENCE_DATE"]]
    singaporeHousing["DaysElapsedSinceLastResale"] = [(datetime.datetime.strptime('2019-01-01', "%Y-%m-%d")-datetime.datetime.strptime(str(d)[0:10],"%Y-%m-%d")).days for d in singaporeHousing["RESALE_REGISTRATION_DATE"]]
    remove_digits = str.maketrans('', '', digits)
    singaporeHousing["StreetType"] =[street.translate(remove_digits).strip().split()[len(street.translate(remove_digits).strip().split())-1] for street in singaporeHousing['STREET_NAME']]

    dataframe1 = singaporeHousing
    # If a zip file is connected to the third input port is connected,
    # it is unzipped under ".\Script Bundle". This directory is added
    # to sys.path. Therefore, if your zip file contains a Python file
    # mymodule.py you can import it using:
    # import mymodule
    
    # Return value must be of a sequence of pandas.DataFrame
    return dataframe1,
