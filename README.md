Chatbot
====

### I want to get it running!

First you have to adapt `.env.proto` with your login data and move it to `.env`. 
The bot will use these credentials for logging into the chat.

##### 1. With docker:
```shell script
$ docker build -t chatbot:latest .
$ docker run --name chatbot -d chatbot
```

#####2. With python
```shell script
$ pip install -r requirements.txt
$ pip install -e .
$ python -m chatbot 
```

### I want to write my own bot!

In `chatbot/bots/bot_srcs` you find two examples of very simple bots.
They need the following things:

```python
from chatbot.bots.abc import BotABC # for marking the class as a bot.import 
from chatbot.interface.messages import OutgoingMessage, IncomingMessage

class MyBot:
    async def react(self, incoming_message):  # If you don't know what that async means, you can ignore it
        # do some stuff
        return OutgoingMessage( message="Hi", 
                                name="MyBot", 
                                channel= incoming_message.channel,  # Or any other channel we are listening to
                                delay = incoming_message.delay + 1) # So we answer on the right message

BotABC.register(MyBot) # So we know that it is a bot.

def create_bot():   # The loader does not need to know the class name
    return MyBot()
```

Just put your bot into `chatbot/bots/bot_srcs` and add its name in `data/configuration/botmaster_config.json` and your are good to go.