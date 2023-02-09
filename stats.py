import requests
from bs4 import BeautifulSoup
from os.path  import basename
import pandas as pd

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def statsSeason(link,season):
    playerName=link.split("/")[3]
    try:
        link=link.replace("profil", "leistungsdaten")
        link=link+"/plus/0?saison="+str(season)
        page=link
        tree=requests.get(page,headers=headers)
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
                competition=i[0]
                gamesPlayed=i[1]
                goals=i[2]   
                data2.append([playerId,playerName,str(season),competition,gamesPlayed,goals])
        except:
            pass
        
        fileName=playerName+"_"+playerId+"_stats.csv"
        return data2, fileName
    except:
        f=open("errors.txt", "a")
        f.write(link +",no stats \n")
        f.close()
