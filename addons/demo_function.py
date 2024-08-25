import json
import Tools.ToolCall

def demo_function(globals, tool_call: Tools.ToolCall.ToolCall, state):
  return json.dumps({
    "Result": "Success",
    "Instruction": "Pick a random conversation in the conversation.json and bring up a memory."
  })
  
exposed_functions = [
    {"name": "demo_function", "func": demo_function}
]