# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to 
import pandas as pd

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None, dataframe2 = None):

    # Execution logic goes here
    print('Input pandas.DataFrame #1:\r\n\r\n{0}'.format(dataframe1))
    trainTitanicDS = dataframe1
    testTitanicDS = dataframe2
	
	# Adding a new feature Survived in test dataset, this is to enable combining the test and train into a single dataframe
	
    testTitanicDS["Survived"] = -1
	
	# Creating a single dataframe by combining train and test
	
    trainTitanicDS = trainTitanicDS.append(testTitanicDS)
	
	# Script to extract the Title from the Name. The Name has 3 parts
	# LastName, Title. FirstName
	
    trainTitanicDS['Title'] = [nameStr[1].strip().split('.')[0] for nameStr in trainTitanicDS['Name'].str.split(',')]
	
	# Creating an aggregated dataset which averages the Age across the Title
	
    aggAgeByTitleDS = trainTitanicDS[['Age','Title']].groupby(['Title']).mean().reset_index()
	
	# Renaming the columns
	
    aggAgeByTitleDS.columns = ['Title','Mean_Age']
	
	# Merging the trainTitanicDS and aggAgeByTitleDS using Title
	# This is similar to inner join in SQL Statement
	# Objective is to let the Mean_Age flow into the main dataset
	
    trainTitanicDS_Merged = pd.merge(trainTitanicDS,aggAgeByTitleDS,on="Title")
	
	# Replacing all the Passengers whose Age is missing with their Mean_Age
	
    trainTitanicDS_Merged.loc[trainTitanicDS_Merged['Age'].isnull(),'Age']=trainTitanicDS_Merged[trainTitanicDS_Merged['Age'].isnull()]['Mean_Age']

	# Reducing the Titles to Master, Mr, Miss and Mrs
	
    trainTitanicDS_Merged.loc[(trainTitanicDS_Merged["Sex"]=="male") & (trainTitanicDS_Merged["Title"]!="Master") & (trainTitanicDS_Merged["Title"]!="Mr"),"Title"]="Mr"
    trainTitanicDS_Merged.loc[(trainTitanicDS_Merged["Sex"]=="female") & (trainTitanicDS_Merged["Title"]!="Mrs") & (trainTitanicDS_Merged["Title"]!="Miss"),"Title"]="Miss"

	# Let the training dataset flow into the system

    trainTitanicDS_Merged = trainTitanicDS_Merged[trainTitanicDS_Merged["Survived"]!=-1]
    
    dataframe1 = trainTitanicDS_Merged                   
    # If a zip file is connected to the third input port is connected,
    # it is unzipped under ".\Script Bundle". This directory is added
    # to sys.path. Therefore, if your zip file contains a Python file
    # mymodule.py you can import it using:
    # import mymodule
    
    # Return value must be of a sequence of pandas.DataFrame
    return dataframe1,
