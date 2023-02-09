import requests
from bs4 import BeautifulSoup
from os.path  import basename
import re
import os
from value import playerValue
from bio import biography
from stats import statsSeason
from transfers import transferHistory
import pandas as pd
import glob

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
colList=['id','name','season','competition','gamesPlayed','goals']

def top_league(n):
    page = "https://www.transfermarkt.pl/pko-ekstraklasa/startseite/wettbewerb/PL1"
    leagueName= page.split("/")[3]+page.split("/")[-1]
    path1=os.path.join(leagueName,"")
    try:
        os.mkdir(path1)
    except:
        pass
    os.chdir(path1)
    print(leagueName)
    tree = requests.get(page, headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    links=[]
    clubsDict={}
    for a in soup.find_all('a', href=True):
        links.append(a['href'])

    r = re.compile(".*/startseite/verein/[0-9]+/.*")
    newlist = list(filter(r.match, links))
    links=list(dict.fromkeys(newlist))
    for i in range(len(links)):
        clubName=links[i].split("/")[1]
        clubsDict.update({clubName:"https://www.transfermarkt.pl"+links[i]})

    for key, value in clubsDict.items():
        path2=os.path.join(key,"")
        print(path2)
        try:
            os.mkdir(path2)
        except:
            pass
        print(os.getcwd())
        os.chdir(path2)
        page = value
        tree = requests.get(page, headers = headers)
        soup = BeautifulSoup(tree.content, 'html.parser')
        
        links=[]
        for a in soup.find_all('a', href=True):
            links.append(a['href'])

        r = re.compile(".*/profil/spieler/[0-9]+")
        newlist = list(filter(r.match, links))
        links=list(dict.fromkeys(newlist))

        for j in range(len(links)):
            link="https://www.transfermarkt.pl"+links[j]
            playerName=links[j].split("/")[1]
            path3=os.path.join(playerName,"")
            try:
                print(path3)
                os.mkdir(path3)
                os.chdir(path3)
            except:
                pass
            try:
                playerValue(link)
                biography(link)
                transferHistory(link)
                data,fileName=statsSeason(link,2022)
                if data == []:
                    break
                df = pd.DataFrame(data,columns=colList)
                df.to_csv(fileName, index=False)
                for i in range(2021,1990,-1):
                    data,fileName=statsSeason(link,i)
                    if data == []:
                        break
                    df = pd.DataFrame(data,columns=colList)
                    df.to_csv(fileName, mode='a',index=False, header=False)
            except:
                pass
            os.chdir("../")
        os.chdir("../")
    
top_league(1)