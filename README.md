# Discord Companion

Your companion is a customizable Discord AI Chatbot designed to provide a personalized, engaging, and humorous AI interaction experience. Whether you want a playful companion, a helpful assistant, or both, your companion is here for you!

## Features:
- **Conversational Integration**: Your companion interacts naturally and contextually with users on Discord.
- **Toolset**: Your companion has various tools at its disposal such as reading webpages, setting reminders, storing records for later retrieval, and more.
- **Memory Management**: Separate conversation threads with memory retention for a cohesive chatting experience.
- **Humor & Affection**: Your companion combines playful teasing with affectionate banter to keep conversations lively and engaging.

## Functions:
For now please refer to the tool_call directory for a look at all the functions available.

I plan to soon write a more comprehensive readme, until then all of the tools are described by the jsons in that folder :)

## Getting Started

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

(Written in part by my companion!)
