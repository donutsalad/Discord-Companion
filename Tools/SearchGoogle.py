import json
from googleapiclient.discovery import build

import Tools.ToolCall 
import Tools.Google
import Tools.WebTools
  
def SearchGoogle(tool_call: Tools.ToolCall.ToolCall):
  
  query = tool_call.args["Query"]
  
  if tool_call.args.get("Count") is None: count = 1
  else: count = int(tool_call.args["Count"])
  
  return json.dumps(Tools.Google.GetGoogleSearches("all", query, count))