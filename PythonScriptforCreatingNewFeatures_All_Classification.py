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


    # Ticket Analysis

    aggTicketDS=trainTitanicDS_Merged[['PassengerId','Ticket']].groupby(['Ticket']).count().reset_index()
    aggTicketDS.columns = ['Ticket','Ticket_Count']
    trainTitanicDS_Merged = pd.merge(trainTitanicDS_Merged,aggTicketDS,on="Ticket")
    trainTitanicDS_Merged["Ticket_Freq"] = [(1 if i>1 else 0)  for i in trainTitanicDS_Merged["Ticket_Count"]]
    
    # Family Size
    
    trainTitanicDS_Merged["FamilySize"]=1+trainTitanicDS_Merged["SibSp"]+trainTitanicDS_Merged["Parch"]
    trainTitanicDS_Merged["FamilySize_Count"] = [(1 if i>1 else 0)  for i in trainTitanicDS_Merged["FamilySize"]]
    
    # Surname Analysis, Identifying people who travelled with similar surnames
    
    trainTitanicDS_Merged["Surname"]=[nameStr[0].strip() for nameStr in trainTitanicDS_Merged['Name'].str.split(',')]
    aggBySurnameDS=trainTitanicDS_Merged[['Surname','Ticket']].groupby(['Surname']).count().reset_index()
    aggBySurnameDS.columns = ['Surname','Surname_Count']
    trainTitanicDS_Merged = pd.merge(trainTitanicDS_Merged,aggBySurnameDS,on="Surname")
    trainTitanicDS_Merged["Surname_Count_Freq"] = [(1 if i>1 else 0)  for i in trainTitanicDS_Merged["Surname_Count"]]

    # Cabin Analysis
    aggByCabinDS=trainTitanicDS_Merged[['Cabin','Ticket']].groupby(['Cabin']).count().reset_index()
    aggByCabinDS.columns = ['Cabin','Cabin_Count']
    trainTitanicDS_Merged = pd.merge(trainTitanicDS_Merged,aggByCabinDS,on="Cabin",how="left")
    trainTitanicDS_Merged.loc[trainTitanicDS_Merged["Cabin_Count"].isnull(),"Cabin_Count"]= 0

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
