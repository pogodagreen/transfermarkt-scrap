import requests
import re
from bs4 import BeautifulSoup
from os.path  import basename
import pandas as pd

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

def biography(link):
    playerName=link.split("/")[3]
    try:
        link=link.replace(".pl/",".co.uk/")
        link=link.replace("profil", "nationalmannschaft")
        page=link
        tree=requests.get(page,headers=headers)
        soup = BeautifulSoup(tree.content, 'html.parser')
        playerId=link.split("/")[6]
        playerYoB=re.findall("\d\d\d\d",str(soup.find("span", itemprop="birthDate")))
        playerNationality=re.findall("[A-Z][a-z]+",str(soup.find("span", itemprop="nationality")))
        playerHeight = re.findall("\d,\d\d",str(soup.find("span", itemprop="height")))
        playerPosition=re.findall("([A-Z][a-z]+( |\-)[A-Z][a-z]+|Goalkeeper|Sweeper)",str(str(soup.find_all("li"))[re.search("Position:",str(soup.find_all("li"))).start():]))[0]
        playerU15=0
        playerU16=0
        playerU17=0
        playerU18=0
        playerU19=0
        playerU20=0
        playerU21=0
        playerA=0
        data = []
        data2=[]
        try:
            table = soup.find('table').find('tbody')

            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele]) # Get rid of empty values
            for i in range(len(data)):
                if i%2!=0:
                    data2.append(data[i])
            for i in range(len(data2)):
                if data2[i][3] == '-':
                    data2[i][3]=0
                if '15' in data2[i][1]:
                    playerU15=data2[i][3]
                elif '16' in data2[i][1]:
                    playerU16=data2[i][3]
                elif '17' in data2[i][1]:
                    playerU17=data2[i][3]
                elif '18' in data2[i][1]:
                    playerU18=data2[i][3]   
                elif '19' in data2[i][1]:
                    playerU19=data2[i][3]
                elif '20' in data2[i][1]:
                    playerU20=data2[i][3]  
                elif '21' in data2[i][1]:
                    playerU21=data2[i][3]   
                else:
                    playerA=data2[i][3]        
        except:
            pass
        df = pd.DataFrame.from_records([{'id':str(playerId), 'name': playerName, 'yearOfBirth': str(playerYoB[0]),'nationality': str(playerNationality[0]), 'height': str(playerHeight[0]), 'position':str(playerPosition[0]), 'u15':str(playerU15), 'u16':str(playerU16), 'u17':str(playerU17), 'u18':str(playerU18), 'u19':str(playerU19), 'u20':str(playerU20), 'u21':str(playerU21), 'team':str(playerA)}])
        fileName=playerName+"_"+playerId+"_National.csv"
        df.to_csv(fileName, index=False)
        
    except:
        f=open("errors.txt", "a")
        f.write(link +",no bio \n")
        f.close()