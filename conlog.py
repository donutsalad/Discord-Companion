import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

def format_message(source, color, message, max_source_length):
    # Adjusting the padding to add space outside the brackets
    formatted_lines = [f"{Style.RESET_ALL}{color}[{source}]{' ' * (max_source_length - len(source))} | " + message.split('\n')[0]]
    padding = ' ' * (max_source_length + 2)
    formatted_lines += [f"{padding} | " + line for line in message.split('\n')[1:]]
    return '\n'.join(formatted_lines)

def get_max_source_length():
    sources = ['ERROR', 'System', 'Discord', 'Ticker', 'Assistant', 'Tool Manager', 'Tool', 'Chat Message User', 'Chat Message Assistant', 'Conversations.json']
    return max(len(s) for s in sources)

MAX_SOURCE_LENGTH = get_max_source_length()

def log_system(message):
    print(format_message('System', Fore.BLUE + Style.BRIGHT, message, MAX_SOURCE_LENGTH))

def log_discord(message):
    print(format_message('Discord', Fore.LIGHTBLACK_EX, message, MAX_SOURCE_LENGTH))

def log_ticker(message):
    print(format_message('Ticker', Fore.MAGENTA, message, MAX_SOURCE_LENGTH))

def log_assistant(message):
    print(format_message('Assistant', Fore.CYAN, message, MAX_SOURCE_LENGTH))

def log_tool_manager(message):
    print(format_message('Tool Manager', Fore.YELLOW, message, MAX_SOURCE_LENGTH))  # Making orange using yellow since there's no direct orange in basic ansi

def log_tool(message):
    print(format_message('Tool', Fore.LIGHTYELLOW_EX, message, MAX_SOURCE_LENGTH))

def log_chat_message_user(message):
    print(format_message('Chat Message User', Fore.LIGHTGREEN_EX, message, MAX_SOURCE_LENGTH))

def log_chat_message_assistant(message):
    print(format_message('Chat Message Assistant', Fore.LIGHTCYAN_EX, message, MAX_SOURCE_LENGTH))
    
def log_log_manager(message):
    print(format_message('Conversations.json', Fore.YELLOW, message, MAX_SOURCE_LENGTH))
    
def log_log_manager(message):
    print(format_message('Conversations.json', Fore.LIGHTRED_EX, message, MAX_SOURCE_LENGTH))
    
def log_restart(message):
    print(format_message('ERROR', Fore.RED, message, MAX_SOURCE_LENGTH))