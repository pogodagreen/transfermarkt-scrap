import pandas as pd
import os.path
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_local_safe_setup():
  options = FirefoxOptions() 
  options.add_argument("--disable-blink-features")
  options.add_argument("--disable-blink-features=AutomationControlled")
  options.add_argument("--disable-infobars")
  options.add_argument("--disable-popup-blocking")
  options.add_argument("--disable-notifications")
  driver = Firefox(desired_capabilities = options.to_capabilities())
  return driver

def playerValue(link):
    playerName=link.split("/")[3]
    playerId=link.split("/")[6]
    link=link.replace("profil", "marktwertverlauf")
    # Create local setup like here: https://gist.github.com/theDestI/aa21a0e721b06a74bd58a0a391d96e8f
    driver = get_local_safe_setup() 
    
		# Call url through selenium driver
    driver.get(link)

		# Wait until element with highcharts graph appears
    try:
      WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.ID, "highcharts-0"))
      )

      # Parse dates and values in those dates
      date = driver.execute_script('return Highcharts.charts[0].series[0].data.map(x => x.series).map(x => x.xData)[0].map(x => new Date(x).toISOString())')
      value = driver.execute_script('return Highcharts.charts[0].series[0].data.map(x => x.series).map(x => x.yData)[0]')
      for i in range(len(date)):
        date[i]=date[i][:10]
      df = pd.DataFrame({'id':playerId, 'name': playerName,'dates': date, 'marketValue': value})
      # df=pd.DataFrame(club)

      # Store to dataframe and save it in current folder
      fileName=playerName+"_"+playerId+"_Value.csv"
      df.to_csv(fileName, index=False)
      
      # Don't forget ot quit!
      driver.quit()

    except:
      driver.quit()
      f=open(os.path.dirname(__file__)+"../errors.txt", "a")
      f.write(link +",no highcharts \n")
      f.close()
