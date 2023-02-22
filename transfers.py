import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def transferHistory(link,file):
    playerName=link.split("/")[3]
    playerFirstName=playerName.split("-")[0]
    try:
      playerLastName=playerName.split("-")[1]
    except:
      playerLastName="-"

    try:
        link=link.replace(".pl/",".co.uk/")
        link=link.replace("profil", "transfers")
        tree=requests.get(link,headers=headers)
        soup = BeautifulSoup(tree.content, 'html.parser')

        playerId=link.split("/")[6]
        cols=["season","date","sourceTeam","destTeam","marketValue","price"]

        mydivs = soup.find_all("div", {"class": "row"})
        txt="".join(mydivs[1].getText().strip())
        txt2=txt.splitlines()
        txt3=[]
        row=[]

        for i in txt2:
            if i != '\n':
                if i!='':
                    txt3.append(i)

        df=pd.DataFrame()
        txt4=txt3[7:]

        for i in range(len(txt4)):
            txt4[i]=txt4[i].lstrip().rstrip()

        if txt4[0]=="Upcoming transfer":
            txt4.remove("Upcoming transfer")
        if txt4[6]=="Transfer history":   
            txt4.remove("Transfer history")

        for i in range(len(txt4)):
            if i%6==0:
                new_df=pd.DataFrame([row])
                df = pd.concat([df, new_df], axis=0, ignore_index=True)
                row=[]
            row.append(txt4[i])

        df.columns=cols
        df=df.drop([0])
        playerIdTable=[]
        playerLastNameTable=[]
        playerFirstNameTable=[]
        for index, row in df.iterrows():
            playerIdTable.append(playerId)
            playerLastNameTable.append(playerLastName)
            playerFirstNameTable.append(playerFirstName)
            if row['date'] == "0":
                df=df.drop(index)
            else:
                row['date']=str(datetime.strptime(str(row['date']),"%b %d, %Y"))[:10]
            if row['marketValue']=='-':
                row['marketValue']=str(0)
            if row['price']=='-':
                row['price']=str(0)
            if row['price']=='?':
                row['price']=str(0)
            if "fee" in row['price']:
                row['price']="Loan" 
            if row['marketValue'][-1:]=='k':
                row['marketValue']=str(int(row['marketValue'][1:-1])*1000)
            elif row['marketValue'][-1:]=='m':
                row['marketValue']=str(int(row['marketValue'][1:-1].replace('.',''))*10000)
            if row['price'][-1:]=='k':
                row['price']=str(int(row['price'][1:-1])*1000)
            elif row['price'][-1:]=='m':
                row['price']=str(int(row['price'][1:-1].replace('.',''))*10000)
        idx=0
        df.insert(loc=idx, column='lastName', value=playerLastNameTable)
        df.insert(loc=idx, column='firstName', value=playerFirstNameTable)
        df.insert(loc=idx, column='id', value=playerId)
        fileName=playerName+"_"+playerId+"_Transfers.csv"
        df.to_csv(fileName, index=False)

    except:
        string=os.getcwd()+","+link+"\n"
        file.write(string)