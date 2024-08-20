import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.WebTools
  
def GetStackPage(url: str): 
  try:     
    html = requests.get(url, headers = Tools.WebTools.headers).text
    soup = BeautifulSoup(html, features="html.parser")

    answers = soup.find_all("div", class_ = "answercell")
    answers = [answer.find("div", class_ = "s-prose") for answer in answers]
    results: ResultSet = [answer.find_all(string = True) for answer in answers]
    
    return results
  
  except Exception as e:
    return "Let the user know you can't access this specific webpage."