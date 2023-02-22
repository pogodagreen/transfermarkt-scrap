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
import sys

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
colList=['id','name','season','competition','gamesPlayed','goals']

f=open("errors.txt", "a")
f2=open("merged.csv","a")

def dir(path):
    print(path)
    try:
        os.mkdir(path)
    except:
        pass
    os.chdir(path)
    print(os.getcwd())


def player(playerName,playerLink):
    path3=os.path.join(playerName,"")
    dir(path3)

    playerValue(playerLink,f)
    biography(playerLink,f,f2)
    transferHistory(playerLink,f)
    statsSeason(playerLink,f)

    os.chdir("../")
        

def team(teamName,teamLink):
    path2=os.path.join(teamName,"")
    dir(path2)

    tree = requests.get(teamLink, headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    links=[]
    for a in soup.find_all('a', href=True):
        links.append(a['href'])

    r = re.compile(".*/profil/spieler/[0-9]+")
    newlist = list(filter(r.match, links))
    links=list(dict.fromkeys(newlist))

    for j in range(len(links)):
        player(links[j].split("/")[1],"https://www.transfermarkt.pl"+links[j])
    os.chdir("../")  

def league(leagueLink):
    leagueName= leagueLink.split("/")[3]+leagueLink.split("/")[-3]
    path1=os.path.join(leagueName,"")
    dir(path1)
    
    tree = requests.get(leagueLink, headers = headers)
    soup = BeautifulSoup(tree.content, 'html.parser')

    links=[]

    for a in soup.find_all('a', href=True):
        links.append(a['href'])

    r = re.compile(".*/startseite/verein/[0-9]+/.*")
    newlist = list(filter(r.match, links))
    links=list(dict.fromkeys(newlist))

    for i in range(len(links)):
        team(links[i].split("/")[1],"https://www.transfermarkt.pl"+links[i])
    os.chdir("../")



def leagues(n):
    page = "https://www.transfermarkt.pl/wettbewerbe/europa"
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    links = pageSoup.find_all("tr")

    site = 'https://www.transfermarkt.pl'
    s22_string = "/plus/?saison_id=2022"
    leagues = []
    for a in list(range(2,((n*2)+1),2)):
        leagues.append((site+(str(links[a]).split('href="',5)[2].split('"')[0])+s22_string))
    return leagues

# n=int(sys.argv[1])
# listOfLeagues=leagues(n)
# for i in listOfLeagues:
#     league(i)

league("https://www.transfermarkt.pl/pko-ekstraklasa/startseite/wettbewerb/PL1/plus/?saison_id=2022")

f.close()
f2.close()
os.system("find . -name geckodriver.log -type f -delete")