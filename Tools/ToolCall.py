import openai
from discord import Client, User

import Tools.RecordBank
import Tools.ReminderBank

class ToolCall:
  def __init__(self, call_type, tool, args, client, discord, user, recordbank, reminderbank):
    self.call_type: str = call_type
    self.args: dict = args
    self.tool = tool
    self.client: openai.Client = client
    self.discord: Client = discord
    self.user: User = user
    self.recordbank: Tools.RecordBank.RecordBank = recordbank
    self.reminderbank: Tools.ReminderBank.ReminderBank = reminderbank