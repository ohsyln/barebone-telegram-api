import barebone_telegram_api

BOT_API_KEY = '1234567890:AAAAAAAA-BBBB-CCCCCCCC-DDDDDDDD-ee'
  
# Instantiate the TelegramAPI class with the API key
API = barebone_telegram_api.TelegramAPI(BOT_API_KEY)

# Create your callback function to handle incoming messages from users
def callback(d):
  """
  Callback function to be passed into start_poll_for_messages(callback)
  Everytime a message is received by the bot, your callback() is run
  
  :param d: dict, the message received from user
  """
  # Retrieve chat_id to reply to the respective user
  chat_id = API.get_chat_id(d)

  # Sends message received back to user for testing
  API.send_msg(chat_id, str(d))

# Starts the long polling via API /getUpdates
thread = API.start_poll_for_messages(callback)

