import numpy as np
import pandas as pd
import datetime

import pandas_datareader 
import pydst 
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')


#Begin to download data using pydst: Danish Statistical Banks Python integration
Dst = pydst.Dst(lang='en')
Dst.get_subjects()
tables = Dst.get_tables(subjects=['04'])
tables[tables.id == 'AUF01']
unemp_pers = Dst.get_variables(table_id='AUF01')

for id in ['YDELSESTYPE','ALDER','KØN']:
    " Finds the possible IDs for the chosen variables within the table and prints them with"
    " their associated text to describe the IDs"
    print(id)
    values = unemp_pers.loc[unemp_pers.id == id,['values']].values[0,0]
    for value in values:      
        print(f' id = {value["id"]}, text = {value["text"]}')

variables = {'OMRÅDE':['*'],'YDELSESTYPE':['TOT'],'ALDER':['TOT'],'KØN':['M','K'],'TID':['*']}
unemp_api = Dst.get_data(table_id= 'AUF01', variables=variables)
unemp_api.head(5)

#Beginning of data cleaning
unempl = unemp_api.copy()
unempl.rename(columns = {"OMRÅDE": "municipality", "ALDER":"age", "KØN":"gender","TID":"time","INDHOLD":"unemployed"}, inplace=True)
drop_columns = ["YDELSESTYPE", "AKASSE"] #Drops the data from YDELSESTYPE and AKASSE
unempl.drop(drop_columns, axis=1, inplace=True)
    #Deletes any row, where it isn't a municipality
I = unempl.municipality.str.contains('Region')
I |= unempl.municipality.str.contains('Province')
I |= unempl.municipality.str.contains('All Denmark')
unempl = unempl.loc[I == False] #Keep everything that isn't "I"
unempl.head(10)
unempl.loc[unempl.municipality == 'Samsø'][unempl.gender == 'Men']

#Making graphs
unempl.info()

unempl.loc[:,'time']= pd.to_datetime(unempl.loc[:,'time'].str.replace('M',''),format='%Y%m')


fig = plt.figure()
ax = fig.add_subplot(1,1,1)

unempl.loc[unempl['municipality'] == 'Samsø',:].plot(x="time", y = "unemployed",legend=True,ax=ax)
plt.show()



