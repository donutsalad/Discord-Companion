# Discord Companion

This project aims to create the beginnings of a long term companion. I use discord for almost all communications with friends, so having an AI copmanion there feels natural! Everything is meticulously logged, and at the end of every conversation the companion will fill out a questionaire. The conversations.json will be an extremely useful datamine to fine-tune future models, and build many other projects with. I also plan on making all my future AI LLM projects backwards compatible. The goal is to bring cutting edge AI right into your DM's next to everyone else!

A key thing to note is say goodbye to your companion at the end of every conversation as they are told to put an \<END\> token when the conversation is over - this triggers the questionaire and deletes the thread resetting the context. The assistant has access to the conversations.json, and is also aware about the previous conversation which makes it feel more natural. If you don't see their status change to "Counting electric sheep zzz" be sure to remind them to end the thread!

# Companion Core Functions

You can chose which of these you want to use by only uploading the tool_calls of the functions that you would find useful, The next major update will include an addon's feature where you can drag and drop scripts into an addon folder and they'll be automatically loaded into the tool chain - so in case you create tons of addons and don't use certain core features ommit as you see fit.

## Records

Fuzzy search storage - useful for indexing things if your notes app is as full as mine!

- Create record
  - Abstract; short description of the record to be embedded
  - Record; the text/URL/code etc. to store.
- Recall record
  - Abstract; something similar to the original abstract - for a cosine search
- Forget record
  - Abstract; same as recall record, deletes the closest match, unless it's too dissimilar

## Reminders

A lot of people won't find this useful, but having ADHD - a conversational reminder where "snoozing" is met with teasing or guilt tripping definitely makes a difference!

- Set new reminder
  - Abstract; A description of what you want to be reminded about
  - Time; From a specific time to "tonight"
- Get reminders
  - Count; how many reminders to return
- Get reminders semantically
  - Abstract; same as in recalling records
- Remove reminder
  - Abstract; same as in forgetting records

## Scripts

Python scripts can be written by you or your companion, and they'll be executed. A local variable called `output_result` will be read and returned to the companion. Don't worry the companion is told not to use `input()` and `output_result` is checked for.

I personally don't use this as the addons feature is coming in the next update - but it's useful if you want some complicated maths function for example, you can have the companion write code to work out the answer and then get the results quickly.

I recommend deleting scripts you aren't going to use again to keep the list clear.

- Save script
  - Script Name; A save name for the script
  - Script Description; A description of it's function (useful for if you forget what you asked your companion to name it, they tend to list scripts when they can't find it)
  - Script Code; The python code to save
- Run script
  - Script Name; The exact match of the name - although the companion is encouraged to list the scripts and find the one you likely meant.
- List scripts (no parameters)
- Get script
  - Script Name; Exact match, but same thing goes as in run script.

## Web Functions

Access to the internet! Highly recommend keeping google search and webpage reading - if you can script please add to the Web folder! Some webpages have custom text extraction. Youtube is also useful if you're lazy and want a summary of a video without having to watch it, although definitely a candidate for freeing up slots for addons.

- Search Google
  - Query; The search string to use
- Read webpage
  - URL; The link to the page you want to scrape.
- Search Youtube
  - Query; The search string to use
- Get Youtube transcript
  - URL; The link to the video you want your companion to "watch"

## Auxiliary Functions

More OpenAI API functions just because!

- Generate image
  - Prompt; The prompt that's sent to dall-e
- Text to speech
  - Text; The text to be spoken outloud.

# Getting Started

## Prerequisites
To set up your companion, you'll need:
1. A Discord Bot token.
2. An Open AI API key & Assistant
3. Google Programmable Search API key and context.

## Tokens
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

## Change the prompt template:
Create a `prompt.txt` file based off of `prompt_template.txt`

## User Guide

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

---

### Note
Stay tuned for a video tutorial on setting up and configuring your companion in detail.

### Contribution
Feel free to contribute to the project by submitting issues or pull requests.

### License
[MIT Licence](LICENSE)

---

Contact me on isabellemunnee@gmail.com or donutsalad on discord if you want to help out!
