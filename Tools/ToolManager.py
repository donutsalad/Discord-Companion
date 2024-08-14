import json
import discord

import logmanager
import ticker

import Tools
import Tools.WebPage
import Tools.WebTools
import Tools.Embedding
import Tools.RecordBank
import Tools.ReminderBank
import Tools.Reminders
import Tools.Record
import Tools.Reminders
import Tools.ToolCall
import Tools.SearchGoogle

tool_list = [
  {"tool_id": "set_new_reminder", "method": Tools.Reminders.set_new_reminder},
  {"tool_id": "get_reminders", "method": Tools.Reminders.get_reminders},
  {"tool_id": "get_reminders_semantically", "method": Tools.Reminders.get_reminders_semantically},
  {"tool_id": "remove_reminder", "method": Tools.Reminders.remove_reminder},
  {"tool_id": "create_record", "method": Tools.Record.create_record},
  {"tool_id": "forget_record", "method": Tools.Record.forget_record},
  {"tool_id": "recall_record", "method": Tools.Record.recall_record},
  
  #Core Web Functions
  {"tool_id": "read_webpage", "method": Tools.WebPage.ReadSite},
  {"tool_id": "search_google", "method": Tools.SearchGoogle.SearchGoogle},
]

class ToolManager:
  
  def __init__(self, discord: discord.Client, ticking: ticker.Ticker, record: Tools.RecordBank.RecordBank, reminders: Tools.ReminderBank.ReminderBank, logger: logmanager.LogManager):
    self.ticking = ticking
    self.RecordBank = record
    self.reminders = reminders
    
    self.discord = discord
    self.logger = logger

  async def handle_tool_call(self, tool, client, user):
  
    args = json.loads(tool.function.arguments)
    
    self.logger.LogToolCall(tool.function.name, args)
    
    for method in tool_list:
      if method["tool_id"] == tool.function.name:
        return [{
          "tool_call_id": tool.id,
          "output": method["method"](Tools.ToolCall.ToolCall(tool.function.name, tool, args, client, self.discord, user, self.RecordBank, self.reminders))
        }]
      
    return [{
      "tool_call_id": tool.id,
      "output": "Please let the user know that this tool isn't implemented yet"
    }]