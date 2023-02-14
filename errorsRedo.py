import os
import pandas as pd
from transfers import transferHistory
from stats import statsSeason
from bio import biography
from value import playerValue

f=pd.read_csv(r'errors2.txt')
f2=open("errors3.txt","a")
for index,row in f.iterrows():
    print(row[0])
    print(row[1])
    print(row[1].split("/")[4])
    os.chdir(row[0])
    if row[1].split("/")[4] == "transfers":
        transferHistory(row[1],f2)
    elif row[1].split("/")[4] == "nationalmannschaft":
        biography(row[1],f2)
    elif row[1].split("/")[4] == "marktwertverlauf":
        playerValue(row[1],f2)
    elif row[1].split("/")[4] == "leistungsdatendetails":
        statsSeason(row[1],f2)
f2.close()
