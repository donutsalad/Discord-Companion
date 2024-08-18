import os
import asyncio
import datetime

import openai
import discord

import logmanager
import restarting
import Tools
import Tools.ToolManager

prompt = ""
if os.path.exists("prompt.txt"):
  with open("prompt.txt", "r") as f:
    prompt = f.read()
else:
  with open("prompt_template.txt") as f:
    prompt = f.read()
    
questionaire = ""
if os.path.exists("questionaire.txt"):
  with open("questionaire.txt", "r") as f:
    questionaire = f.read()
  
Reminder_Message = """
The discord backend has just triggered an event.
A reminder that was set has elapsed. The reminder abstract was:
"""
      
def Reminder_Prompt():
  return f"{prompt}\n{Reminder_Message}"

#TODO: Make safer  
def chunk_message(message, limit = 1990):
  chunks = []
  chunk = ""
  code_block_open = False

  for line in message.splitlines(keepends=True):
    if len(chunk) + len(line) <= limit:
      chunk += line
      if line.startswith("```"):
        code_block_open = not code_block_open
    else:
      if code_block_open and not chunk.endswith("```\n"):
        chunk += "```\n"
      chunks.append(chunk)
      chunk = ""
      if line.startswith("```"):
        code_block_open = not code_block_open
        chunk = line
      else:
        chunk = line
      if code_block_open:
        chunk = "```" + chunk  # reopen the code block in the new chunk

  if code_block_open and not chunk.endswith("```\n"):
      chunk += "```\n"
  chunks.append(chunk)
  return chunks

class OpenAIChatHandler:

  def __init__(self, queue: asyncio.Queue, logger: logmanager.LogManager,
               toolmanager: Tools.ToolManager.ToolManager, discord: discord.Client, 
               openai_key: str, assistant_id: str, user_id: int):
    
    self.logger = logger
    
    self.queue = queue
    
    self.discord = discord
    self.user_id = user_id
    self.discorduser = self.discord.get_user(self.user_id)
    
    self.toolmanager = toolmanager
    
    self.openai_key = openai_key
    self.asssistant_id = assistant_id
    
    self.run = None
    self.ended = True
    
    self.client = openai.OpenAI(api_key = openai_key)
    self.assistant = self.client.beta.assistants.retrieve(assistant_id)
    
  def get_discord_user(self):
    return self.discord.get_user(self.user_id)

  async def waitloop(self):
    while True:
      
      if self.discorduser is None:
        print("Still waiting on getting discord user...")
        self.discorduser = self.get_discord_user()
      
      if not self.queue.empty():
        incoming = await self.queue.get()
        await self.incoming(incoming)
      
      await asyncio.sleep(0.5)
    
  async def incoming(self, message: discord.Message):
    
    if self.run is None:
        self.ended = False
        await self.new_thread(message)
        
    elif not self.ended:
        if self.run.thread_id is not None:
            await self.existing_thread(message)
            
    else:
        self.ended = False
        await self.new_thread(message)
        
    return

  async def new_thread(self, message: discord.Message):
    
      print("New thread starting.")
      self.logger.StartConversation()
      self.logger.LogUserMessage(message.content)
      
      await self.discord.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Talking to you!"))
      await self.handle_run(message, True)

  async def existing_thread(self, message: discord.Message):
      self.logger.LogUserMessage(message.content)
      await self.handle_run(message, False)

  async def delete_thread(self):
    self.client.beta.threads.delete(self.run.thread_id)
    self.run.thread_id = None
    self.ended = True
    
    self.logger.EndConversation()
    
    print("Uploading conversation data...")
    await self.discord.change_presence(status = discord.Status.idle, activity = discord.CustomActivity(name = "Uploading conversation data"))
    self.vector_store = self.client.beta.vector_stores.create(name="Companion's Files")
    
    file_streams = [open(f"conversations.json", "rb")]
    self.client.beta.vector_stores.file_batches.upload_and_poll(
      vector_store_id = self.vector_store.id, files=file_streams
    )
    
    self.client.beta.assistants.update(
      assistant_id = self.asssistant_id,
      tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}},
    )
    
    await self.discord.change_presence(status = discord.Status.idle, activity = discord.CustomActivity(name = "Counting electric sheep zzz"))
    print("Thread ended.")
    
  async def external_thread(self, type, information):
    
    if self.discorduser is None:
      return False
  
    if self.ended == False:
      return False
    
    try:
      match type:
        
        case "Reminder":          
          self.ended = False
          self.run = self.client.beta.threads.create_and_run(
            assistant_id = self.assistant.id,
            instructions = Reminder_Prompt() + information,
            thread = { "messages": [
              {"role": "assistant", "content": logmanager.get_most_recent_conversation()},
              {"role": "assistant", "content": "I'll read the reminder out to you from my prompt, so you can just listen to it instead of reading about it."}
            ]}
          )
          
        case _:
          print("Unknown Internal Message Type, Raising Exception.")
          raise Exception("Unknown Internal Message Type sent to Assistant.")
        
    except Exception as e:
      print("\n\nWARNING: unable to handle internal event. Raising exception.")
      raise Exception(f"Internal problem creating thread {e}")
      #TODO: Catch this
        
    
    await self.discord.change_presence(status = discord.Status.online, activity = discord.CustomActivity(name = "Messaging you!"))
    async with self.discorduser.dm_channel.typing():
      self.logger.StartConversation()
      await self.await_responce()
      
    return True
  
  async def handle_run(self, dmessage: discord.Message, newthr):
    
    message = dmessage.content

    images = []
    files=[]
    
    if len(dmessage.attachments) > 0:
      
      for attachment in dmessage.attachments:
        filename = attachment.filename
        
        if os.path.exists(f"downloads/{filename}"):
          filename = f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {filename}'
          
        await attachment.save(f"downloads/{filename}")
        files.append(attachment.url)
          
        #Vision
        if attachment.content_type in ('image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image.gif'):
          images.append(attachment.url)
          self.logger.LogUserImage(filename)
          
        #Files
        elif attachment.content_type in (
          'text/x-c',  # .c
          'text/x-csharp',  # .cs
          'text/x-c++',  # .cpp
          'application/msword',  # .doc
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
          'text/html',  # .html
          'text/x-java',  # .java
          'application/json',  # .json
          'text/markdown',  # .md
          'application/pdf',  # .pdf
          'text/x-php',  # .php
          'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # .pptx
          'text/x-python',  # .py
          'text/x-script.python',  # .py
          'text/x-ruby',  # .rb
          'text/x-tex',  # .tex
          'text/plain',  # .txt
          'text/css',  # .css
          'text/javascript',  # .js
          'application/x-sh',  # .sh
          'application/typescript'  # .ts
        ):
          
          file_streams = [open(f"downloads/{filename}", "rb")]
          self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id = self.vector_store.id, files=file_streams
          )
          
          self.client.beta.assistants.update(
            assistant_id = self.asssistant_id,
            tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}},
          )
      
    thread_messages = []
  
    if len(images) != 0:
      contents = []
      contents.append({"type": "text", "text": f'[{datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")}] {message}'})
      for img in images:
        contents.append({"type": "image_url", "image_url": {"url": img}})
        
      thread_messages.append(
        {"role": "user", "content": contents}
      )
      
    else:
      thread_messages.append(
        {"role": "user", "content": f'[{datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")}] {message}'}
      )
        
    async with dmessage.channel.typing():
            
      if newthr == True:
        thread_messages.append(
          {"role": "assistant", "content": logmanager.get_most_recent_conversation()}
        )
        self.run = self.client.beta.threads.create_and_run(
          assistant_id = self.assistant.id,
          thread = { "messages": thread_messages },
          instructions = prompt
        )
        
      else:
        self.run = self.client.beta.threads.runs.create(
          thread_id = self.run.thread_id,
          assistant_id = self.assistant.id,
          additional_messages = thread_messages
        )
          
      await self.await_responce()
          
  async def handle_tool_call(self, run, user):
  
    results = []
    for tool in run.required_action.submit_tool_outputs.tool_calls:
      result = await self.toolmanager.handle_tool_call(tool, self.client, self.discorduser)
      results.extend(result)
      
    self.run = self.client.beta.threads.runs.submit_tool_outputs(
      thread_id = self.run.thread_id,
      run_id = self.run.id,
      tool_outputs = results
    )
    
    await self.await_responce()
      
  #Used by starting new thread, opening new thread, and continuing - including tool calls
  async def await_responce(self):
    
    while not ((self.run.status == "completed") or (self.run.status == "requires_action")):
        
      match self.run.status:
        case "failed":
          await self.discorduser.dm_channel.send("The run failed! Restarting...")
          await self.delete_thread()
          restarting.restart_program()
          return
          
        case "in_progress":
          #print("waiting for responce...")
          await asyncio.sleep(0.35)
          
      self.run = self.client.beta.threads.runs.retrieve(thread_id = self.run.thread_id, run_id = self.run.id)

    
    match self.run.status:
      case 'completed':
        
        messages = self.client.beta.threads.messages.list(
          thread_id = self.run.thread_id,
          limit = 2
        )
          
        result = messages.data[0].content[0].text.value
        
        self.logger.LogCompanionMessage(result)
        
        final = False          
        if "<END>" in result[-5:]:
          final = True
          result = result[:-5]
        
        if len(result) < 1:
          await self.discorduser.dm_channel.send("Companion said nothing :o")
          
        elif len(result) < 1999:
          await self.discorduser.dm_channel.send(result)
          
        else:
          chunks = chunk_message(result)
          for chunk in chunks:
            #TODO: Handle gracefully (although I think it is now)
            await self.discorduser.dm_channel.send(chunk[:1999])
          
        if final:
          print("Thread ending from end token.")
          await self.CompleteQuestionaire()
          await self.delete_thread()
        return
      
      case "requires_action":
        await self.handle_tool_call(self.run, self.discorduser)
      
      case _:
        await self.discorduser.dm_channel.send(f"Unhandled state from normal messages. ({self.run.status})")
        await self.delete_thread()

  async def CompleteQuestionaire(self):
    
    messages = [
      {"role": "user", "content": questionaire}
    ]
    
    self.run = self.client.beta.threads.runs.create(
      thread_id = self.run.thread_id,
      assistant_id = self.assistant.id,
      additional_messages = messages
    )
        
    while not ((self.run.status == "completed") or (self.run.status == "requires_action")):
        
      match self.run.status:
        case "failed":
          await self.discorduser.dm_channel.send("Questionaire failed - restarting program.")
          await self.delete_thread()
          restarting.restart_program()
          return
          
        case "in_progress":
          #print("waiting for responce...")
          await asyncio.sleep(0.35)
          
      self.run = self.client.beta.threads.runs.retrieve(thread_id = self.run.thread_id, run_id = self.run.id)

    
    match self.run.status:
      case 'completed':
        
        messages = self.client.beta.threads.messages.list(
          thread_id = self.run.thread_id,
          limit = 2
        )
          
        result = messages.data[0].content[0].text.value
        
        self.logger.QuestionaireCompleted(result)
      
      case "requires_action":
        await self.handle_tool_call(self.run, self.discorduser)
      
      case _:
        await self.delete_thread()

    return