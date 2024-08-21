# Discord Companion

Introducing your versatile Discord AI Chatbot — a customizable companion crafted to deliver a personalized, engaging, and delightfully humorous interaction experience. Whether you seek a playful confidant, a reliable assistant, or a seamless blend of both, your companion is ready to accompany you on every digital journey!

# Companion Capabilities

Welcome to the world of advanced AI companionship, where your digital buddies are stacked with amazing skills to make life a breeze! Here's a peek at what’s under the hood:

- **Create Record**: Store your memories with `create_record`. Provide (or have your companion write) a catchy "Abstract" and store the juicy details you want to "Record".
  
- **Forget Record**: Need to clean house? `forget_record` helps you delete unwanted records using a close match to the "Abstract" of the memory you wish to erase.

- **Recall Record**: Use `recall_record` to dig up past treasures — provide an "Abstract" similar to what you want as your search query and "Count" for the number of juicy returns.

- **Set New Reminder**: Never miss a thing with `set_new_reminder`. Define what it's "about" and the "time" to get those timely nudges.

- **Get Reminders**: Retrieve your essential to-dos with `get_reminders`. A 10 in the "Count" parameter will do the trick!

- **Get Reminders Semantically**: Advanced searching with `get_reminders_semantically` — find those special nuggets with a smart "Abstract" and "Count".

- **Remove Reminder**: Made plans you don't need? `remove_reminder` lets you clean up with ease using a close match of the "Abstract" of the reminder.

- **Save Script**: Compile awesome scripts using `save_script`. Name it, explain it, and fashion the code into a formidable AI-sidekick.

- **Run Script**: Give life to scripts with `run_script`. Have your companion pass "Arguments" for fine-tuned execution and let the magic happen!

- **Delete Script**: Housekeeping is easy with `delete_script` — no mess, no hassle with just a "Script Name".

- **List Scripts**: Browse your brilliant creations effortlessly with `list_scripts` and see what your AI toolkit holds.

- **Search Google**: Become an info wizard with `search_google`. Query the web and watch the answers roll in.

- **Read Webpage**: Let `read_webpage` be your content snatcher — just a "URL" away from raw text joy.

- **Search YouTube**: Hunt down audio-visual treats using `search_youtube`. Refine by "Query" and set your result "Count".

- **Get YouTube Transcript**: With `get_youtube_transcript`, have your companion watch a video for you to find a quote or summarise the video - just pop in the "URL".

- **Generate Image**: Unleash creativity with `generate_image`. Provide a "Prompt" and watch art come alive.

- **Text-to-Speech (TTS)**: Convert text into sweet serenades using `tts_speech`. Let words leap from screen to sound.

# Getting Started

### Prerequisites
To set up your companion, you'll need:
1. A Discord Bot token.
2. An Open AI API key.
3. Google Programmable Search API key and context.

### Installation

1. **Clone the repository:**
   
```bash
   git clone <repository-url>
   cd <repository-directory>
```

2. **Configure Tokens:**
   Create a `tokens.txt` file with the following template:
   
```plaintext
   [Discord User ID]
   <ID>
   [Discord Bot Token]
   <TOKEN>
   [Open AI API Key]
   <TOKEN>
   [Assistant ID]
   <ID>
   [Google API Token]
   <TOKEN>
   [Google Search Context]
   <ID>
```

3. **Change the prompt template:**
  Create a `prompt.txt` file based off of `prompt_template.txt`   

4. **Run the bot:**
   
```bash
   python main.py
```

### User Guide

1. **Create a Discord Bot:**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
   - Under "Bot", add a new bot and copy the token into the `tokens.txt` file.
   - Make sure to enable all priviledged intents.
   - Invite your bot to your server using the OAuth2 URL generator.

2. **Set Up OpenAI Assistant:**
   - Go to the [Open AI Dashboard](https://platform.openai.com/) and create a new API key.
   - Copy the key into the `tokens.txt` file.
   - Copy all the tool_calls into the functions of the assistant.
  
3. **Configure Google Programmable Search:**
   - Create a [Programmable Search Engine](https://cse.google.com/) and generate an API key and search context.
   - Copy the key and context into the `tokens.txt` file.

### Note
Stay tuned for a video tutorial on setting up and configuring your companion in detail.

## Future Plans
- Adding more tools and capabilities.
- Improved error handling and debugging.

## Contribution
Feel free to contribute to the project by submitting issues or pull requests.

## License
[MIT Licence](LICENSE)

Enjoy your time with your companion! 🖤

---

(Written mostly by my companion!)