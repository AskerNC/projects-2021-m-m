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
unempl_pers = Dst.get_variables(table_id='AUF01')

#We find the possible IDs for the chosen variables within the table and prints them with
#their associated text to describe the IDs
for id in ['YDELSESTYPE','ALDER','KØN']:
    
    print(id)
    values = unempl_pers.loc[unempl_pers.id == id,['values']].values[0,0]
    for value in values:      
        print(f' id = {value["id"]}, text = {value["text"]}')

variables = {'OMRÅDE':['*'],'YDELSESTYPE':['TOT'],'ALDER':['TOT'],'KØN':['M','K'],'TID':['*']}
unempl_AUF1 = Dst.get_data(table_id= 'AUF01', variables=variables)
unempl_AUF2 = Dst.get_data(table_id= 'AUF02', variables=variables)

#Rewrite the TID parameter to be in datetime
unempl_AUF1.loc[:,'TID']= pd.to_datetime(unempl_AUF1.loc[:,'TID'].str.replace('M',''),format='%Y%m')
unempl_AUF2.loc[:,'TID']= pd.to_datetime(unempl_AUF2.loc[:,'TID'].str.replace('M',''),format='%Y%m')
unempl_AUF2.head(-1)
#Since AUF2 has the actual unemployment numbers, but AUF1 have more recent data, we choose to merge these.
I = (unempl_AUF1["TID"] > "2019-06-01") #Choose to stack only rows in AUF1, where there are newer data than in AUF2
unempl_AUF1 = unempl_AUF1.loc[I == True]
unempl_AUF1
#concat = pd.concat([unempl_AUF2, unempl_AUF1])
outer = pd.merge(unempl_AUF1, unempl_AUF2, how='outer') 
outer.head()

#Beginning of data cleaning
unempl = outer.copy()
unempl.rename(columns = {"OMRÅDE": "municipality", "ALDER":"age", "KØN":"gender","TID":"time","INDHOLD":"unemployed"}, inplace=True)
drop_columns = ["YDELSESTYPE", "AKASSE"] #Drops the data from YDELSESTYPE and AKASSE
unempl.drop(drop_columns, axis=1, inplace=True)

#Deletes any row, where it isn't a municipality
I = unempl.municipality.str.contains('Region')
I |= unempl.municipality.str.contains('Province')
I |= unempl.municipality.str.contains('All Denmark')
unempl = unempl.loc[I == False] #Keep everything that isn't "I"

#Making graphs
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

unempl.loc[unempl['municipality'] == 'Samsø', :][unempl['gender'] == 'Men'].plot(ax=ax, x="time", y = "unemployed",legend=True)
plt.show()


#Widget for all municipalities and for each gender
import ipywidgets as widgets
def plot_interact(df, municipality):
    I = df['municipality'] == municipality
    I |= df['gender'] == gender
    ax = df.loc[I,:].plot(x='time', y = 'unemployed', style='-o', legend=False)
widgets.interact(plot_interact, 
    df = widgets.fixed(unempl),
    municipality = widgets.Dropdown(description='Municipality', 
    options=unempl.municipality.unique(), 
    value='Roskilde'),
    gender = widgets.Dropdown(description='Gender',
    options=unempl.gender.unique(),
    value='Men')
);