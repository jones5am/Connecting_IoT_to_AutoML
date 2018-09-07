# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 13:24:03 2018

@author: andrew.jones
"""

#import packages
import pandas as pd
from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

#%% read in data

Secom_Data = pd.read_csv('C:/Users/andrew.jones/Documents/Grad School/Applied Research/secom.data.txt', header = None, delim_whitespace = True)
Secom_Labels = pd.read_csv('C:/Users/andrew.jones/Documents/Grad School/Applied Research/secom_labels.data.txt', header = None, delim_whitespace = True)


#%% Relabelling Columns

Secom_Labels.columns = ['Pass_Fail', 'Time_Stamp']
Secom_Data = Secom_Data.add_prefix('Feature_')

#%% Droping columns with many NaN values and with all zeros

Secom_Data = Secom_Data.dropna(thresh = len(Secom_Data) - 25, axis = 1) #columns that have more than 25 NaN values



#%% bind data together so that nan rows can be droped without reindexing the targets
Secom_Labelled_Data = pd.concat([Secom_Labels, Secom_Data], axis = 1)
Secom_Labelled_Data = Secom_Labelled_Data.dropna(axis = 0) #at this point rows there were only ~130 NaN rows

#%% Dropping Columns that have only zeros and therefore don't contribute to the model
Secom_Labelled_Data = Secom_Labelled_Data.loc[:, (Secom_Labelled_Data != 0).any(axis = 0)]


#%% EDA for Unbalanced Dataset

Unbalanced = Secom_Labelled_Data['Pass_Fail'].value_counts() #class of data is clearly unbalanced
#Unbalanced = Unbalanced.reset_index().drop(['index'], axis = 1)
print(Unbalanced)
y_pos = ['-1','1']

num_bins = 3
plt.bar(y_pos, Unbalanced, facecolor = 'blue',alpha = 0.1)
plt.title('Unbalanced Classes')
plt.ylabel('Number of Records')
plt.xlabel('Normal Unit vs. Defect Unit')
plt.show()

#%% EDA for range of values within dataset; Scatterplot of Mean and Standard Deviation

Mean = Secom_Labelled_Data.mean(axis = 0)
SD = Secom_Labelled_Data.std(axis = 0)

plt.scatter(Mean, SD)
plt.title('Mean and Standard Deviation of Features')
plt.xlabel('Mean')
plt.ylabel('Standard Deviation')
plt.show()


#%% Resplit data back into features & targets
Secom_Labels_Final = Secom_Labelled_Data.iloc[:,0] #put targets in own dataframe
Secom_Data_Final = Secom_Labelled_Data.drop(['Pass_Fail','Time_Stamp'], axis = 1) #don't need timestamp either


#%% Train Test Split - put test size at 20%, because I don't have a massive number of records


X_train, X_test, y_train, y_test = train_test_split(Secom_Data_Final, Secom_Labels_Final, test_size=0.20, random_state=42) 


#%% Invoking the TPOT classifier class to run through thousands of models & hyperparameters for optimization
#Please note they market this tool as a Data Science "Assistant" not a replacement, and encourage further manual model validation steps

tpot = TPOTClassifier(generations=5, population_size=50, verbosity=2, scoring = 'roc_auc') #chose AUC because of imbalanced dataset
tpot.fit(X_train, y_train)
print(tpot.score(X_test, y_test))
tpot.export('tpot_secom_pipeline_v2.0.py')   

