import requests
from bs4 import BeautifulSoup, ResultSet
from googleapiclient.discovery import build

import Tools.WebTools
import json

def ReadPhysOrgArticle(url: str):
  try:
    html = requests.get(url, headers = Tools.WebTools.headers).text
    soup = BeautifulSoup(html, features="html.parser")

    article = soup.find("article")
    results: ResultSet = article.find_all("p")
    
    return [
      result.text
      for result in results
    ]
    
  except Exception as e:
    return "Let the user know you can't access this specific webpage."

