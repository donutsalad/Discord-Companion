import os
import pickle
import datetime
from typing import List

import openai

import Tools.Embedding
import Tools.ToolCall 

class RecordBank:
  def __init__(self, filename):
    self.filename: str = filename
    self.records: List[Tools.Embedding.Record] = self.TryLoad(self.filename)
    
    
  def TryLoad(self, filename) -> bool:
    
    if os.path.isfile(filename):
      
      try:
        loaded: List[Tools.Embedding.Record] = []
        with open(filename, "rb") as file:
          loaded = pickle.load(file)
        return loaded
      
      except:
        raise Exception(f"Problem loading records from {filename}!")
    
    else:
      return []
    
  def Save(self):
    
    if os.path.isfile(self.filename):
      
      if os.path.isfile(f"{self.filename}.backup"):
        os.remove(f"{self.filename}.backup")
        
      os.rename(self.filename, f"{self.filename}.backup")
      
    try:
      with open(self.filename, "wb") as file:
        pickle.dump(self.records, file)
    
    except Exception as e: raise Exception(f"Problem arised when saving records: {e}")

  
  def NewRecord(self, client: openai.Client, abstract: str, record: str):
    self.records.append(Tools.Embedding.Record(abstract, record, Tools.Embedding.EmbedString(client, abstract)))
    
    try:
      self.Save()
          
    except Exception as e:
      #TODO: Make sure.
      print("Failed to save new record, potentially being saved too right now.")
    
  def GetRecord(self, query: List[float], count: int) -> List[Tools.Embedding.RecordQuery]:
    return Tools.Embedding.QueryRecord(self.records, query)[:count]
  
  def RemoveRecord(self, record: Tools.Embedding.Record) -> None:
    stored = None
    for entry in self.records:
      if entry.abstract == record.abstract:
        stored = entry
        break
      
    self.records.remove(stored)
    
    try:
      self.Save()
          
    except Exception as e:
      #TODO: Make sure.
      print("Failed to save records after deletion, potentially being saved too right now.")
  