import json
from typing import List

import Tools.ToolCall  
import Tools.Embedding
    

def create_record(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  try:
    tool_call.recordbank.NewRecord(tool_call.client, tool_call.args["Abstract"], tool_call.args["Record"])
    
  except Exception as e:
    return "Tell the user the recordbank has failed to create the record"
    
  return "Tell the user the record has been stored successfully"
      

def forget_record(tool_call: Tools.ToolCall.ToolCall) -> str:
    
  try:
    record = tool_call.recordbank.GetRecord(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), 1)
    if record[0].score < 6:
      confirm = json.dumps({
          "Instruction": f"Ask the user if they meant to delete: {record[0].record.abstract}."
        })
      return confirm
    else:
      tool_call.recordbank.RemoveRecord(record[0].record)
      
  except Exception as e:  
    return "Let the user know there was a problem when trying to delete the record."
    
  return "Let the user know the record has been forgotten"
     

def recall_record(tool_call: Tools.ToolCall.ToolCall) -> str:
  
  if tool_call.args.get("Count") is None:
    count = 1
    
  else: count = int(tool_call.args["Count"])
  
  try:
    sorted = tool_call.recordbank.GetRecord(Tools.Embedding.EmbedString(tool_call.client, tool_call.args["Abstract"]), count)
  
  except Exception as e:
    print(e)
    return "Let the user know that the backend failed to open the record"
    
  results = []
  for record in sorted:
    results.append({
      "record_abstract": record.record.abstract,
      "record_content": record.record.record,
      "match_score": record.score,
      "match_confidence": record.strength
      })  
      
  if count == 1:
    final_result = json.dumps({
      "Instruction": "If it has a high confidence you can just let her know the content - otherwise also let her know you're not sure if they means this particular record.",
      "results": results[0]
    })
          
  else: final_result = json.dumps({
      "Instruction": "Show the user a list of the abstracts and their scores, and then when they specify one you can let her know the content of the record.",
      "results": results[:count]
    })
          
  return final_result