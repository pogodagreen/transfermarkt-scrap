import requests
from bs4 import BeautifulSoup
import os.path
from os.path  import basename
import pandas as pd
import os

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def statsSeason(link,file):
    playerName=link.split("/")[3]
    try:
        link=link.replace("profil", "leistungsdatendetails")
        tree=requests.get(link,headers=headers)
        soup = BeautifulSoup(tree.content, 'html.parser')

        playerId=link.split("/")[6]
        data = []
        data2=[]

        try:
            tables=soup.find_all('table')
            table = tables[1].find('tbody')    
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            for i in data:
                if i[2]=='-':
                    i[2]=0
                if i[3]=='-':
                    i[3]=0
                if i[6]=='-':
                    i[6 ]=0
                season=str(i[0])
                competition=str(i[1])
                gamesPlayed=str(i[2])
                goals=str(i[3])
                minutes=str(i[6]).replace(".","").replace("'","")
                data2.append([playerId,playerName,str(season),competition,gamesPlayed,goals,minutes])
        except:
            pass
        df=pd.DataFrame(data2,columns=['id','name','season','competition','gamesPlayed','goals','minutes'])
        fileName=playerName+"_"+playerId+"_stats.csv"
        df.to_csv(fileName, index=False)

    except:
        string=os.getcwd()+","+link+"\n"
        file.write(string)