import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from import_1 import read_data


#data1 = pd.read_csv("Example Reteval.csv", sep=',', usecols=[6,7], skiprows=28, names=columns )
#data1 = data1.dropna(how='any')
data1 = pd.read_csv("CB07_970322_220216105506_Small.csv", sep=',', encoding='latin1')


i = data1.loc[data1['PatientID'] == 'Reported Waveform'].index.values
j = data1.loc[data1['PatientID'] == 'Raw Waveform'].index.values
k = data1.loc[data1['PatientID'] == 'Pupil Waveform'].index.values

data2 = data1.iloc[i[0]+1:j[0],:] #splitting the datasets
data3 = data1.iloc[j[0]+1:k[0],:]
data4 = data1.iloc[k[0]+1:,:]

#dropping the columns that does not have values
data2 = data2.dropna(axis = 1, how='all')
data3 = data3.dropna(axis = 1, how='all')
data4 = data4.dropna(axis = 1, how='all')
#converting the column values to numeric data
data2 = data2.apply(pd.to_numeric)
data3 = data3.apply(pd.to_numeric)
data4 = data4.apply(pd.to_numeric)

print(data4.columns)
print(data4)
#  plotting

data2.plot(x='CB07',y= 'Unnamed: 3')
data2.plot(x='CB07.2',y= 'Unnamed: 7')
data2.plot(x='CB07.4',y= 'Unnamed: 11')
plt.show()

data3.plot(x='CB07',y= 'Unnamed: 3')
data3.plot(x='CB07.2',y= 'Unnamed: 7')
data3.plot(x='CB07.4',y= 'Unnamed: 11')
plt.show()

data4.plot(x='CB07.13',y= 'CB07.15')
plt.show()





