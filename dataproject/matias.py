import numpy as np
import pandas as pd
import datetime
import copy
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
#Since AUF2 has the actual unemployment numbers, but AUF1 have more recent data, we choose to stack these on top of eachother.
I = (unempl_AUF1["TID"] > "2019-06-01") #Choose to stack only rows in AUF1, where there are newer data than in AUF2
unempl_AUF1 = unempl_AUF1.loc[I == True]
unempl_AUF1
#concat = pd.concat([unempl_AUF2, unempl_AUF1])
outer = pd.merge(unempl_AUF1, unempl_AUF2, how='outer') 

#Create seperate total unemployment df for men and women and sum them
I = (outer['OMRÅDE'] == 'All Denmark') & (outer['KØN'] == 'Women')
unem_tot_wom = outer.loc[I, :]

unem_tot_wom.head()

I = (outer['OMRÅDE'] == 'All Denmark') & (outer['KØN'] == 'Men')
unem_tot_men = outer.loc[I, :]

unem_tot = copy.copy(unem_tot_wom)
unem_tot.head(100)

unem_tot['INDHOLD'] = unem_tot_men['INDHOLD'] + unem_tot_wom['INDHOLD']
unem_tot.head(100)


drop_columns = ["YDELSESTYPE", "AKASSE", "KØN", "ALDER"] 

unem_tot = outer['All Denmark']

#Graf med faktiske bruttoledige, væksten i % og den gennemsnitslige vækst i %