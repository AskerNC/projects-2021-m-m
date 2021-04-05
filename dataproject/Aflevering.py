import numpy as np
import pandas as pd
import datetime

import pandas_datareader 
import pydst 
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

Dst = pydst.Dst(lang='en')
Dst.get_subjects()
tables = Dst.get_tables(subjects=['04'])
tables[tables.id == 'AUF01']
unemp_pers = Dst.get_variables(table_id='AUF01')

for id in ['YDELSESTYPE','ALDER','KØN']:
    print(id)
    values = unemp_pers.loc[unemp_pers.id == id,['values']].values[0,0]
    for value in values:      
        print(f' id = {value["id"]}, text = {value["text"]}')

