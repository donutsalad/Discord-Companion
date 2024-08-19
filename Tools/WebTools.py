import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.ToolCall
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
  
#Not sure if this is the best technique
def ReadGenericPage(url):
  try:
    html = requests.get(url, headers = headers).text
    soup = BeautifulSoup(html, features="html.parser")

    results: ResultSet = soup.find_all(string = True)
  
    return [
      entry.text
      for entry in results
    ]
    
  except Exception as e:
    return "Let the user know you can't access this website."