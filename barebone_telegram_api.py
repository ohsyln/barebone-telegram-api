import json
import requests
import threading
import time
import traceback

class TelegramAPI():
  def __init__(self, api_key):
    self.latest_msg_id = 0
    self.API_KEY = api_key.strip()
    self.API_PREFIX = 'https://api.telegram.org/bot'
    self.API_SEND = '/sendMessage'
    self.API_GET = '/getUpdates'
    self.MAX_THREADS = 23
    self.callback = None

  def start_poll_for_messages(self, callback):
    """
    Starts infinite polling for user input via /getUpdates API

    :param callback: function(dict), where dict is the message received
    See https://core.telegram.org/bots/api#getupdates

    :return: thread
    """
    self.callback = callback

    t = threading.Thread(target=self.infinite_poll)
    t.start()
    return t

  def get_chat_id(self, d):
    """
    To be used inside the callback function to quickly retrieve chat_id

    :params d: first arg of callback function
    """
    return d['message']['chat']['id']

  def infinite_poll(self):
    """
    Run internally by start_poll_for_messages() via separate Thread

    Infinite loop to poll for new messages via API /getUpdates
    """
    URL = self.API_PREFIX + self.API_KEY + self.API_GET
    while 1:
      PARAMS = {'offset':self.latest_msg_id,'limit':1,'timeout':60}
      # Poll for next new message
      try:
        r = requests.get(URL,params=PARAMS)
      except:
        print('{}'.format(traceback.print_exc()))
        continue

      # Check if response is valid
      if r.status_code != 200:
        print('(infinite_poll) response code: {}, text: {}'.format(r.status_code, r.text))
        continue
       
      # Parse incoming message
      j = json.loads(r.text) 
      msgs = j['result']
      # Check if there are any new messages
      if len(msgs) == 0:
        continue

      # Pass user_input to callback function
      if self.callback is not None:
        thread_queue = []
        # Use threading to run self.callback in parallel to avoid waiting
        for msg in msgs:
          t = threading.Thread(target=self.callback, args=(msg,))
          t.start()
          thread_queue.append(t)
          if len(thread_queue) > self.MAX_THREADS:
            thread_queue.pop(0).join()

      # Increment update_id so we read the next message later
      self.latest_msg_id = msg[-1]['update_id'] + 1

  def send_msg(self, chat_id, msg):
    """
    Sends message to user via /sendMessage API

    :param1 chat_id: int (to reference correct user)
    :param2 msg: str (msg to send)
    """
    URL = self.API_PREFIX + self.API_KEY + self.API_SEND
    PARAMS = {'chat_id': chat_id, 'text': msg}
    while 1:
      try:
        r = requests.get(url=URL, params=PARAMS)
      except:
        print('(send_msg) response code: {}, text: {}'.format(r.status_code, r.text))
        time.sleep(60)
      else:
        # Successfully sent msg to user
        return
