import os
import json
import discord
import datetime
import conlog

file_path = 'conversations.txt'

def get_most_recent_conversation():
  try:
    if (os.path.exists(file_path)):
      with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1]
        last_json: dict = json.loads(last_line)
        last_record: str = last_json["Questionaire"]["conversation_record"]
        last_memory: str = last_json["Questionaire"]["things_to_remember"]
        last_mood: str = last_json["Questionaire"]["summary_of_my_mood"]
        last_reflection: str = last_json["Questionaire"]["companion_reflections_and_hopes"]
        
        message_starter = f"""Hi future me! My code lets me write a few things to my future selve in order to pick up the conversation where we left off.
This is what we talked about last time
{last_record}

This is what I wanted to remember
{last_memory}

Last time they were feeling: "{last_mood}" 💕

And I felt this: "{last_reflection}" 😇"""
      
    else:
      return "The user can't see this message, I just realised to myself this is the first time I'm meeting them, I should introduce myself and get to know them."
        
  except Exception as e: 
    conlog.log_log_manager(f"Error occured\nSpecific error: {e}")
    return "The user won't see this message so I need to tell them something went wrong when I see them."
      
  return message_starter

class LogManager:
  
  def __init__(self):
    self.CurrentConversation: Conversation = None
    
  def StartConversation(self):
    self.CurrentConversation = Conversation()
    
  def LogUserMessage(self, message):
    if self.CurrentConversation is None:
      conlog.log_log_manager("Warning: User message recieved without an active conversation. Ignoring.")
      return
    
    self.CurrentConversation.log_user_message(message)
    
  def LogUserImage(self, image):
    if self.CurrentConversation is None:
      conlog.log_log_manager("Warning: User image recieved without an active conversation. Ignoring.")
      return
    
    self.CurrentConversation.log_user_image(image)
    
  def LogCompanionMessage(self, message):
    if self.CurrentConversation is None:
      conlog.log_log_manager("Warning: Companion message recieved without an active conversation. Ignoring.")
      return
    
    self.CurrentConversation.log_companion_message(message)
    
  def LogToolCall(self, tool, args):
    if self.CurrentConversation is None:
      conlog.log_log_manager("Warning: Tool Call recieved without an active conversation. Ignoring.")
      return
    
    self.CurrentConversation.log_tool_call(tool, args)
    
  def LogToolResult(self, tool, result):
    if self.CurrentConversation is None:
      conlog.log_log_manager("Warning: Tool Call recieved without an active conversation. Ignoring.")
      return

    self.CurrentConversation.log_tool_result(tool, result)
    
  def QuestionaireCompleted(self, questionaire):
    if self.CurrentConversation is None:
      conlog.log_log_manager("Warning: Questionaire recieved without an active conversation. Ignoring.")
      return
    
    try:
      dictionary = json.loads(questionaire)
      self.CurrentConversation.questionaire_completed(dictionary)
      
    except Exception as e:
      conlog.log_log_manager("Warning!!! The result wasn't a clean json. Storing string to fix later...")
      self.CurrentConversation.questionaire_completed(f"NON_JSON_RESPONSE:\n{questionaire}")
      
    
  def EndConversation(self):
    dictionary = self.CurrentConversation.as_dict()
    dictionary["EndTime"] = datetime.datetime.now()
    
    with open(file_path, "a") as file:
      file.write("\n")
      json.dump(dictionary, file, default = str)
      
    
    #formatting as json for openai files
    with open(file_path, 'r') as f:
        data = f.readlines()

    json_objects = [json.loads(line.strip()) for line in data if line.strip()]

    with open("conversations.json", 'w') as f:
      json.dump(json_objects, f, indent=4)
    #---
    
      
    self.CurrentConversation = None
  

class Conversation:
  
  def __init__(self):
    self.StartedAt = datetime.datetime.now()
    self.Messages = []
    self.ToolCalls = []
    self.ToolResults = []
    self.Questionaire = dict()
    
  def log_user_message(self, message):
    self.Messages.append({"who": "User", "when": datetime.datetime.now(), "message": message})
    
  def log_user_image(self, image):
    self.Messages.append({"who": "User_pic", "when": datetime.datetime.now(), "path": image})
    
  def log_companion_message(self, message):
    self.Messages.append({"who": "Companion", "when": datetime.datetime.now(), "message": message})
    
  def log_tool_call(self, tool, args):
    self.ToolCalls.append({"tool": tool, "args": args, "when": datetime.datetime.now()})
    
  def log_tool_result(self, tool, result):
    self.ToolResults.append({"tool": tool, "result": result, "when": datetime.datetime.now()})
    
  def questionaire_completed(self, result):
    self.Questionaire = result
    
  def as_dict(self) -> dict:
    return {
      "StartTime": self.StartedAt,
      "Messages": self.Messages,
      "ToolCalls": self.ToolCalls,
      "ToolResults": self.ToolResults,
      "Questionaire": self.Questionaire
    }