 # barebone-telegram-api

Pure Python barebone wrapper that only provides access to /getUpdates (by constant polling) and /sendMessage Telegram Bot REST APIs.

### Prerequisites (Raspbian/macOS/Ubuntu)

The entire setup requires setting up a Telegram Bot (easy step-by-step guide [here](https://medium.com/@wk0/send-and-receive-messages-with-the-telegram-api-17de9102ab78)), as well as an Internet-connected machine hosting this script.

Install python3 and pip3, in the system hosting the script (I used a Raspberry Pi Zero, Python 3.7):

```
sudo apt-get install python3
```

### Demo

Clone to your local directory:

```
git clone https://github.com/ohsyln/barebone-telegram-api
cd barebone-telegram-api
```

Edit `BOT_API_KEY` in `demo.py` with a text editor:

```
BOT_API_KEY = "<YOUR TELEGRAM BOT API KEY HERE>"
```

Run script, which takes in user input from Telegram Bot (via /getUpdates) and sends the JSON-structured message back to the user (via /sendMessage).
```
python3 demo.py
```

## License

MIT
