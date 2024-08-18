import asyncio
import os
from openai import OpenAI
from discord import File
from datetime import datetime
import Tools.ToolCall

def tts_speech(tool_call: Tools.ToolCall.ToolCall):
    text_input = tool_call.args["text"]
    
    # Use the existing client from tool_call
    client = tool_call.client
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
        input=text_input,
    )

    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"downloads/tts_{timestamp}.mp3"
    
    # Save the audio stream to a file
    response.stream_to_file(file_name)

    # Upload the file via dm_channel
    if os.path.exists(file_name):
        asyncio.create_task(tool_call.user.dm_channel.send("voice message", file=File(file_name)))
        return "Audio file created and sent! Ask the user if that was okay."
    else:
        return "Whoops, something went wrong! Couldn't save the audio file."