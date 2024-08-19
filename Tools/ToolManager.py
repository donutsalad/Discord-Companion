import json
import discord

import logmanager
import ticker
import restarting
import conlog

import Tools
import Tools.WebPage
import Tools.WebTools
import Tools.Youtube
import Tools.Embedding
import Tools.RecordBank
import Tools.ReminderBank
import Tools.Reminders
import Tools.Record
import Tools.Reminders
import Tools.ToolCall
import Tools.SearchGoogle
import Tools.Scripting
import Tools.VoiceMessage
import Tools.DallE

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
  
  {"tool_id": "search_youtube", "method": Tools.Youtube.GetYoutubeVideos},
  {"tool_id": "get_youtube_transcript", "method": Tools.Youtube.GetYoutubeTranscript},

  # Script Tools
  {"tool_id": "save_script", "method": Tools.Scripting.save_script},
  {"tool_id": "run_script", "method": Tools.Scripting.run_script},
  {"tool_id": "list_scripts", "method": Tools.Scripting.list_scripts},
  {"tool_id": "delete_script", "method": Tools.Scripting.delete_script},
  
  # Voice Message
  {"tool_id": "tts_speech", "method": Tools.VoiceMessage.tts_speech},

  # Image generation
  {"tool_id": "generate_image", "method": Tools.DallE.GenerateDallEImage}
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
        try:
          #Catch any exceptions thrown by the tool referenced.
          output = method["method"](Tools.ToolCall.ToolCall(tool.function.name, tool, args, client, self.discord, user, self.RecordBank, self.reminders))
          self.logger.LogToolResult(tool.function.name, output)
          return [{
            "tool_call_id": tool.id,
            "output": output
          }]
        except Exception as e:
          ("Error occured in the tool_call, please check your code.\nSpecific error:")
          conlog.log_tool_manager(e)
          restarting.restart_program()
      
    return [{
      "tool_call_id": tool.id,
      "output": "Please let the user know that this tool isn't implemented yet"
    }]