import os
import pandas as pd
from transfers import transferHistory
from stats import statsSeason
from bio import biography
from value import playerValue

f=pd.read_csv(r'errors.txt')
f2=open("errors2.txt","a")
f3=open("merged.csv","a")
for index,row in f.iterrows():
    print(row[0])
    print(row[1])
    print(row[1].split("/")[4])
    os.chdir(row[0])
    if row[1].split("/")[4] == "transfers":
        transferHistory(row[1],f2)
    elif row[1].split("/")[4] == "nationalmannschaft":
        biography(row[1],f2,f3)
    elif row[1].split("/")[4] == "marktwertverlauf":
        pass
    elif row[1].split("/")[4] == "leistungsdatendetails":
        statsSeason(row[1],f2)
f2.close()
