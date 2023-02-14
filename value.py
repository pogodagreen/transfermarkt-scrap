import pandas as pd
from selenium import webdriver
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def get_local_safe_setup():
  options = FirefoxOptions() 
  options.add_argument("--disable-blink-features")
  options.add_argument("--disable-blink-features=AutomationControlled")
  options.add_argument("--disable-infobars")
  options.add_argument("--disable-popup-blocking")
  options.add_argument("--disable-notifications")
  driver = Firefox(desired_capabilities = options.to_capabilities())
  return driver

def playerValue(link,file):
    playerName=link.split("/")[3]
    playerId=link.split("/")[6]
    link=link.replace("profil", "marktwertverlauf")


    try:
      driver = get_local_safe_setup() 
      driver.get(link)

      WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.ID, "highcharts-0"))
      )

      date = driver.execute_script('return Highcharts.charts[0].series[0].data.map(x => x.series).map(x => x.xData)[0].map(x => new Date(x).toISOString())')
      value = driver.execute_script('return Highcharts.charts[0].series[0].data.map(x => x.series).map(x => x.yData)[0]')

      for i in range(len(date)):
        date[i]=date[i][:10]
      df = pd.DataFrame({'id':playerId, 'name': playerName,'dates': date, 'marketValue': value})

      fileName=playerName+"_"+playerId+"_Value.csv"
      df.to_csv(fileName, index=False)
      
      driver.quit()

    except:
      driver.quit()
      string=os.getcwd()+","+link+"\n"
      file.write(string)
