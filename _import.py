import os
import glob
import pandas as pd
import numpy as np
import csv


#d={} why here and not in read_data


class Measurement: #i'm trying to do everything with a class but wouldn't it be easier if i put everything about a measurement into a list and i write functions to get the values?
    "this class serves to store an experiment with its date and results"

    # which values do we need for analysis?
    #which datapiont is for what? i mean for example teh a_A is only for light adapted measurements and the mean of the mesurementd of 2 different frequencies?
    def __init__(self,records, adaptation):
        self.date=records[2][0].split(' ')[0]
        self.eye=records[3][0]
        self.e_type=records[4][0]. split('_')[1]
        self.flash = records[6][0]
        self.a_t, self.a_A, self.b_t, self.b_A=[records[i][0] for i in range(12, 16)]
        self.fund_t=records[17][2]
        self.waveform_t =records[18][2]
        self.fund_A= records[19][2]
        self.waveform_A = records[20][2]
        self.recorded_waveform=pd.DataFrame(records[27:456,0:2], columns = ['ms','uV'])
        self.raw_waveform = pd.DataFrame(records[458:98202,0:2], columns = ['ms','uV'])
        self.pupil_waveform = pd.DataFrame(records[98204:,0], columns = ['ms']) #hopefully Edina's part drops NaN
        self.status = 'WAITING FOT VALIDATION'
        self.adaptation=adaptation


    #order by date (ascending)

    #function to get data easily


# DATA READING
#def index_2d(myList, v):
    #for i, x in enumerate(myList):
        #if v in x:
            #return i, x.index(v)

def read_data(path):
    d = {}
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    for f in csv_files[:4]: # loop over the list of csv files
        df = pd.read_csv(f, encoding = "ISO-8859-1", low_memory=False, header=None) # read the csv file
        df=df.values
        #df=df.tolist() #easier to use the table as a list of lists(rows) but I use the np.array because of the indexing
        #print(type(df[9][2]))
        if df[9][2]=='30':
            light_right1=Measurement(df[:, 2:5], 'light')
            light_right2 = Measurement(df[:, 6:9], 'light')
            light_left1 = Measurement(df[:, 10:13], 'light')
            light_left2 = Measurement(df[:, 14:17], 'light')
            dark_right1 = Measurement(df[:, 20:23], 'dark')
            dark_right2 = Measurement(df[:, 24:27], 'dark')
            dark_left1 = Measurement(df[:, 28:31], 'dark')
            dark_left2 = Measurement(df[:, 32:35], 'dark')
        else: #would be better in a for cycle
            dark_right1 = Measurement(df[:, 4:7], 'dark')
            dark_right2 = Measurement(df[:, 8:11], 'dark')
            dark_left1 = Measurement(df[:, 12:15], 'dark')
            dark_left2 = Measurement(df[:, 16:19], 'dark')
            light_right1 = Measurement(df[:, 22:25], 'light')
            light_right2 = Measurement(df[:, 26:29], 'light')
            light_left1 = Measurement(df[:, 32:35], 'light')
            light_left2 = Measurement(df[:, 36:39], 'light')
        s=df[0][2]  #I tried to get the real value (for example the patient ID)
        if s in d:
            s_list=d[s]
            s_list.extend([light_right1, light_right2, light_left1, light_left2, dark_right1, dark_right2, dark_left1, dark_left2])
            d[s]=s_list
        else:
            d[s]=[df[1][2], light_right1, light_right2, light_left1, light_left2, dark_right1, dark_right2, dark_left1, dark_left2]

        #df = df.tolist()
        # print(index_2d(df, 'Reported Waveform'), index_2d(df, 'Raw Waveform'), index_2d(df, 'Pupil Waveform'))
    return d  #Now I use d as a global variable in the code but I'm not sure yet how it will be more prctical -> global variable or value that can be passed by the function returning with that dictionary


#path = r'C:\Users\veres\PycharmProjects\braintherpy\data'
#read_data(path)






