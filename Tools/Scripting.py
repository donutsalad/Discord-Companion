import json
import os
from datetime import datetime
import subprocess

def save_script(tool_call):
    script_name = tool_call.args["Script Name"]
    script_description = tool_call.args["Script Description"]
    script_code = tool_call.args["Script Code"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    script_record = {
        "Timestamp": timestamp,
        "Name": script_name,
        "Description": script_description
    }

    # Append the script record to a text file
    with open("scripts/script_records.txt", "a") as record_file:
        record_file.write(json.dumps(script_record) + "\n")
    
    # Sanitize script name for use in file system
    safe_name = script_name.strip().replace(" ", "_")

    # Check for existing files and rename if needed
    script_path = f"scripts/{safe_name}.py"
    count = 2
    while os.path.exists(script_path):
        script_path = f"scripts/{count}-{safe_name}.py"
        count += 1
    
    # Create the script file
    with open(script_path, "w") as script_file:
        script_file.write(script_code)

    return "successful"


def run_script(tool_call):
    script_name = tool_call.args["Script Name"]
    arguments = tool_call.args["Arguments"]

    # Sanitize script name for file system
    safe_name = script_name.strip().replace(" ", "_")
    script_path = f"scripts/{safe_name}.py"

    # Find the correct script file if it has been renamed
    count = 2
    while not os.path.exists(script_path) and count < 100:
        script_path = f"scripts/{count}-{safe_name}.py"
        count += 1

    if not os.path.exists(script_path):
        return "script not found"

    # Run the script with the given arguments
    command = f"python {script_path} {arguments}"
    try:
        #TODO: enable inputs.
        output = subprocess.check_output(command, shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Ran the code, an error occured, please let the user know about the error: {e.output}"
      

def list_scripts():
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