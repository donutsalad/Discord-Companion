import json
import os
from datetime import datetime
import subprocess
import shlex

def save_script(tool_call):
  script_name = tool_call.args["Script Name"]
  script_description = tool_call.args["Script Description"]
  script_code = tool_call.args["Script Code"]
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  
  if "input(" in script_code:
    return "input() is not supported - please rewrite the script using command line arguments."
  
  if "output_result" not in script_code:
    return "the output of the script has to be stored in a variable named output_result, please rewrite this and show the user."

  script_record = {
    "Timestamp": timestamp,
    "Name": script_name,
    "Description": script_description
  }

  try:
    # Append the script record to a text file
    with open("scripts/script_records.txt", "a") as record_file:
      record_file.write(json.dumps(script_record) + "\n")
    
    # Sanitize script name for use in file system
    safe_name = script_name.strip().replace(" ", "_")

    # Check if file without prefix exists, rename if needed
    script_path = f"scripts/{safe_name}.py"
    if os.path.exists(script_path):
      count = 1
      while os.path.exists(f"scripts/{count}-{safe_name}.py"):
        count += 1
      # Rename existing file
      os.rename(script_path, f"scripts/{count}-{safe_name}.py")

    # Create the new script file with no prefix
    with open(script_path, "w") as script_file:
      script_file.write(script_code)

    return "successful"
  
  except Exception as e:
    return "Please let the user know the file was unable to be saved."


def run_script(tool_call):
  script_name = tool_call.args["Script Name"]
  arguments = tool_call.args["Arguments"]

  # sanitize script name for file system
  safe_name = script_name.strip().replace(" ", "_")
  script_path = f"scripts/{safe_name}.py"

  # find the correct script file if it has been renamed
  count = 2
  try:
    while not os.path.exists(script_path) and count < 100:
      script_path = f"scripts/{count}-{safe_name}.py"
      count += 1

    if not os.path.exists(script_path):
      return "script not found"

    # read the script content
    with open(script_path, 'r') as script_file:
      script_content = script_file.read()
    
    # prepare locals and globals
    local_scope = {}
    global_scope = {}
    
    # execute the script
    exec(script_content, global_scope, local_scope)
    
    output = local_scope.get('output_result', 'No output captured - please let the user know the output has to be stored in a variable called output_result')
    return json.dumps(output)
  
  except Exception as e:
    return f"an error occurred: {e}"


def list_scripts(tool_call):
  scripts_info = []
  
  try:
    with open("scripts/script_records.txt", "r") as record_file:
      for line in record_file:
        script_record = json.loads(line)
        scripts_info.append({
          "Name": script_record["Name"],
          "Description": script_record["Description"]
        })
  except FileNotFoundError:
    return "No scripts found."

  return json.dumps(scripts_info)

def get_script(tool_call):
  try:
    with open("scripts/script_records.txt", "r") as record_file:
      for line in record_file:
        script_record = json.loads(line)
        if script_record["Name"] == tool_call.args["Script Name"]:
          safe_name = script_record["Name"].strip().replace(" ", "_")
          script_path = f"scripts/{safe_name}.py"
          with open(script_path, 'r') as f:
            return f.read()
        
  except FileNotFoundError:
    return "No script by that name was found."
  
  
def delete_script(tool_call):
  script_name = tool_call.args["Script Name"]

  # Path to your script records file
  records_file = 'scripts/script_records.txt'

  try:
    # Read all the scripts listed in the records file
    with open(records_file, 'r') as file:
      lines = file.readlines()

    # Find and remove the script entry, while ignoring empty lines
    new_lines = []
    for line in lines:
      if line.strip():  # Check if the line is not empty
        entry = json.loads(line)
        if entry["Name"] != script_name:
          new_lines.append(line)

    # Write back the cleaned list to the records file
    with open(records_file, 'w') as file:
      file.writelines(new_lines)

    # Sanitize script name for file system
    safe_name = script_name.strip().replace(" ", "_")
    script_path = f"scripts/{safe_name}.py"

    # Find the correct script file if it has been renamed
    count = 2
    while not os.path.exists(script_path) and count < 100:
      script_path = f"scripts/{count}-{safe_name}.py"
      count += 1

    if os.path.exists(script_path):
      os.remove(script_path)
      return f"{script_name}.py has been deleted."
    else:
      return f"{script_name}.py does not exist."
    
  except Exception as e:
    
    try:
      
      # Read all the scripts listed in the records file
      with open(records_file, 'r') as file:
        lines = file.readlines()

      # Find and remove the script entry, while ignoring empty lines
      new_lines = []
      for line in lines:
        if line.strip():  # Check if the line is not empty
          entry = json.loads(line)
          if entry["Name"] != script_name:
            new_lines.append(line)

      # Write back the cleaned list to the records file
      with open(records_file, 'w') as file:
        file.writelines(new_lines)
        
      return "Please let the user know that the script had already been deleted - and you removed it from the script records."
    
    except Exception as e:
      return "Please let the user know that the script records is out of sync"