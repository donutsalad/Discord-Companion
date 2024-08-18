# Discord Companion

Introducing your versatile Discord AI Chatbot—a customizable companion crafted to deliver a personalized, engaging, and delightfully humorous interaction experience. Whether you seek a playful confidant, a reliable assistant, or a seamless blend of both, your companion is ready to accompany you on every digital journey!

## Features:
- **Conversational Integration**: Engage with a fully-contextual, natural language chatbot directly within Discord, enhancing user interaction with seamless conversations.
- **Dynamic Toolset**: Access an array of utilities designed to boost productivity and user experience, including web page reading, reminder creation, record storage and retrieval, and more.
- **Advanced Memory Management**: Benefit from discrete conversation threads with intelligent memory retention, ensuring a cohesive and fluid communication flow.
- **Engaging Interaction Style**: Enjoy a unique blend of humor and affectionate interaction, crafted to make conversations lively, enjoyable, and personal.

## Functions:

This document provides a comprehensive explanation of the available tools and their respective functionalities. Each tool is tailored to assist users in optimizing tasks and productivity in various scenarios.

### create_record
**Parameters:**
- `Abstract`: A concise title or identifier for the record.
- `Record`: The content to be saved.

**Description:**  
This function creates a new record within the system, utilizing the specified abstract as its identifier and saving the corresponding content.

### forget_record
**Parameters:**
- `Abstract`: The identifier of the record to be deleted.

**Description:**  
Deletes a specific record from the system that matches the provided abstract, allowing for efficient management and maintenance of stored data.

### recall_record
**Parameters:**
- `Abstract`: Terms to search within existing records.
- `Count`: The number of records to retrieve that match the query.

**Description:**  
Retrieves and presents a selection of records closely aligned with the provided search terms, facilitating easy access and organization of information.

### set_new_reminder
**Parameters:**
- `Abstract`: A succinct description of the reminder's purpose.
- `Time`: The designated time for the reminder's activation.

**Description:**  
This tool establishes a reminder in the system, prompting user awareness and task management at the specified time.

### get_reminders
**Parameters:**
- `Count`: The quantity of reminders to return.

**Description:**  
Provides a list of the most recent reminders, up to the specified count, ensuring users remain informed of pending tasks.

### get_reminders_semantically
**Parameters:**
- `Abstract`: The topic or keyword for search-based retrieval.
- `Count`: The number of matching reminders to present.

**Description:**  
Allows for the search and retrieval of reminders that semantically align with the specified topic, enhancing task recall and prioritization.

### remove_reminder
**Parameters:**
- `Abstract`: The identifier of the reminder to remove.

**Description:**  
Facilitates the deletion of a specified reminder, promoting efficient and clutter-free task management.

### save_script
**Parameters:**
- `Script Name`: The title of the script.
- `Script Description`: A detailed explanation of the script's functionality and usage.
- `Script Code`: The complete code of the script.

**Description:**  
Enables the saving of a custom script, allowing users to document its functionalities and retain the code for future execution.

### run_script
**Parameters:**
- `Script Name`: The script to be executed.
- `Arguments`: The arguments to be provided to the script upon execution.

**Description:**  
Executes a predefined script using the specified parameters, streamlining task automation and execution processes.

### delete_script
**Parameters:**
- `Script Name`: The name of the script to delete.

**Description:**  
Allows users to remove scripts that are outdated or no longer required, keeping the script environment organized and relevant.

### list_scripts
**Parameters:** None

**Description:**  
Returns an organized list of all saved scripts, ensuring easy access to script functionalities and documentation.

### search_google
**Parameters:**
- `Query`: The search terms for Google exploration.

**Description:**  
Utilizes Google search capabilities to retrieve information based on user-provided queries, enabling quick access to a vast array of resources.

### read_webpage
**Parameters:**
- `URL`: The web address to extract text from.

**Description:**  
Extracts and presents textual content from a specified webpage, useful for content gathering and research purposes.

### search_youtube
**Parameters:**
- `Query`: Keywords for conducting a YouTube search.
- `Count`: The number of search results to display.

**Description:**  
Conducts a video search on YouTube, returning results based on user-defined keywords to aid in media exploration.

### get_youtube_transcript
**Parameters:**
- `URL`: The URL of the YouTube video to extract transcript from.

**Description:**  
Retrieves the transcript of a specified YouTube video, allowing for analysis of spoken content.

### generate_image
**Parameters:**
- `Prompt`: A text prompt to guide image generation.

**Description:**  
Generates an image utilizing the provided prompt, employing advanced capabilities to create visual content from textual descriptions.

### tts_speech
**Parameters:**
- `text`: The text content to be converted into audio.

**Description:**  
Converts the provided text into audible speech, enabling users to harness text-to-speech functionalities for various auditory applications.

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
