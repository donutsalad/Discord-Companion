import asyncio
import datetime
from Tools import RecordBank, ReminderBank
import conlog

class Ticker:
  def __init__(self, reminderbank: ReminderBank.ReminderBank, record: RecordBank.RecordBank, outqueue: asyncio.Queue):
    self.reminders = reminderbank
    self.record = record

    self.outqueue = outqueue
    
  async def TickerLoop(self) -> None:
    savetime = datetime.datetime.now()
    
    while True:
      now = datetime.datetime.now()
        
      triggered = self.reminders.CheckTriggered(now)
      for trigger in triggered:
        await self.outqueue.put(trigger)
        self.reminders.RemoveReminder(trigger)
        
      if now > savetime:
        
        try:
          self.reminders.Save()
          self.record.Save()
          savetime = now + datetime.timedelta(minutes = 10)
          conlog.log_ticker("Saved!")
          
        except Exception as e:
          #TODO: Make sure.
          conlog.log_ticker("Failed to save something, potentially being saved too right now.")
          savetime = now + datetime.timedelta(minutes = 1)
      
      await asyncio.sleep(1)