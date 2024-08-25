import asyncio
import datetime
import conlog

import tokens
import discordbot
import assistant
import ticker
import logmanager
import addons.addons as addons

import Tools.Embedding
import Tools.Record
import Tools.RecordBank
import Tools.ReminderBank
import Tools.Reminders
import Tools.ToolManager

async def main():
  
  conlog.log_system("Starting up")
  
  masterqueue = asyncio.Queue()
  assistantqueue = asyncio.Queue()
  
  conlog.log_system("Created queues")
  
  logger = logmanager.LogManager()
  
  conlog.log_system("Created conversations.json logger")
  
  records = Tools.RecordBank.RecordBank("data/records")
  reminders = Tools.ReminderBank.ReminderBank("data/reminders")
  
  conlog.log_system("RecordBank and ReminderBank loaded.")
  
  client = discordbot.SetupDiscordClient(assistantqueue, tokens.user_id)
  conlog.log_system("Setup discord client.")
  
  ticking = ticker.Ticker(reminders, records, masterqueue)
  conlog.log_system("Ticker created")
  
  addons_handler = addons.Registrar(masterqueue, logger, client)
  conlog.log_assistant("Addons registered")
  
  toolmanager = Tools.ToolManager.ToolManager(addons_handler, client, ticking, records, reminders, logger)
  conlog.log_system("Tool manager created.")
  
  assistant_handler = assistant.OpenAIChatHandler(assistantqueue, logger, toolmanager, client, tokens.openai_key, tokens.assistant_id, tokens.user_id)
  conlog.log_system("OpenAI Assistant Handler instantiated.")
  
  
  conlog.log_system("Starting Tasks...")
  asyncio.create_task(client.start(tokens.discord_token))
  asyncio.create_task(ticking.TickerLoop())
  asyncio.create_task(assistant_handler.waitloop())
  
  conlog.log_system("Exiting setup and starting main loop.")
  await main_loop(masterqueue, reminders, assistant_handler)
  
async def main_loop(masterqueue: asyncio.Queue, reminders: Tools.ReminderBank.ReminderBank, assistant_handler: assistant.OpenAIChatHandler):
  
  while True:
    
    while not masterqueue.empty():
      item = await masterqueue.get()
      
      if isinstance(item, Tools.Embedding.Reminder):
        try:
          new_thread = await assistant_handler.external_thread("Reminder", item.abstract)
          
          if not new_thread:
            conlog.log_system("Companion is busy, appending back to list with a half minute delay...")
            delayed: Tools.Embedding.Reminder = item
            delayed.time = item.time + datetime.timedelta(seconds = 30)
            reminders.reminders.append(delayed)
            
          else:
            conlog.log_system("Companion has been alerted of an internal ticker elapse.")
        
        except Exception as e:
          conlog.log_system(f"Internal Exception from creating new thread: \n{e}\n\n")
            
      else:
        conlog.log_system("Unhandled ticker type... Ignoring.")

    await asyncio.sleep(0.5)
  
if __name__ == "__main__":
  asyncio.run(main())