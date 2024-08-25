import asyncio
import os
import importlib.util
import sys
import threading
import Tools
import discord
import logmanager


class RegistrarVariables:
  def __init__(self, value):
    self.value = value
    
class RegistrarGlobals:
  def __init__(self, queue: asyncio.Queue, logger: logmanager.LogManager, discord: discord.Client):
    
    self.queue = queue
    self.logger = logger
    self.discord = discord 

class Registrar:
  def __init__(self, queue: asyncio.Queue, logger: logmanager.LogManager, discord: discord.Client, 
               addons_folder='addons'):
    
    self.globals: RegistrarGlobals = RegistrarGlobals(queue, logger, discord) 
    
    self.function_list = []
    self.ticker_functions = []
    self.queue_functions = []
    
    self.states = []
    
    self.queue = queue
    
    self.load_addons(addons_folder)
    
    # Non-async implementation
    queue_thread = threading.Thread(target=self.process_queue)
    queue_thread.start()

  def load_addons(self, folder):
    
    for filename in os.listdir(folder):
      if filename.endswith('.py'):
        
        print(f'File name: {filename}')
        
        filepath = os.path.join(folder, filename)
        module_name = filename[:-3]
        
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)
        
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        if hasattr(module, 'exposed_functions'):
          for method in module.exposed_functions:
            self.function_list.append({"name": method["name"], "func": method["func"]})
            self.states.append({"name": method ["name"], "state": {}})

        if hasattr(module, 'ticker_functions'):
          for method in module.ticker_functions:
            self.ticker_functions[method ["name"]] = method ["func"]
            self.states.append({"name": method ["name"], "state": {}})
        
        if hasattr(module, 'queue_functions'):
          for method in module.queue_functions:
            self.queue_functions[method ["name"]] = method ["func"]
            self.states.append({"name": method ["name"], "state": {}})

  async def ticker(self):
    while True:
      for name, method in self.ticker_functions.items():
        method (self.globals, next((x for x in self.states if x["name"] == name), None))
      await asyncio.sleep(1)  # Ticking every second

  def process_queue(self):
    while True:
      if not self.queue.empty():
        item = self.queue.get()
        for name, method in self.queue_functions.items():
          method (self.globals, item, next((x for x in self.states if x["name"] == name), None))    

  def call_function(self, tool_call, name):
    for func in self.function_list:
      if func["name"] == name:
        return func["func"](self.globals, tool_call, next((x for x in self.states if x["name"] == name), None))
      
    return "Not Found in addons"