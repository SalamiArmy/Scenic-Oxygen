# Scenic Oxygen
## A simple shell for hosting python bots on Google App Engine.

### What is Scenic Oxygen?
Scenic Oxygen can perform autherization for for linking bots together or to the web, perform scheduled CRON jobs and store data about bot's state.

### How does it work?
Scenic Oxygen will listen for all messages in many chat groups (either directly with him or in a chat room which you invite him to) starting with "/".

### How do I add new commands?
All you have to do is create a new python script in commands/ that has a function called run which takes five arguments, the first argument is the id of the chat to reply to, the second is the name of the user to address when replying, the third is the incoming message text and the fourth and fifth are the keys if your command uses any and the number of responses the user is expecting.

tl;dr: Look at one of the existing commands, you must have a run(chat_id, user, message, keyConfig, number_of_responses) function.

### How do I make my own bot using this?
Go to https://console.developers.google.com and create a Google App Engine project. Then take that project id (it will be two random words and a number eg. gorilla-something-374635) and your Telegram Bot ID which the Bot Father gave you and do the following:

1. Copy bot_keys.ini.template and rename the copy to keys.ini.
2. Update {Your Telegram Bot ID here} in keys.ini and do the same for Skype and Facebook bots.

```bash
git clone (url for your Scenic Oxygen fork) ~/bot
cd ~/bot
(PATH TO GOOGLE APP ENGINE LAUNCHER INSTALL)appcfg.py -A {GOOGLE APP ENGINE PROJECT ID} update .
```

Finally go to https://{GOOGLE APP ENGINE PROJECT ID}.appspot.com/set_webhook?url=https://{GOOGLE APP ENGINE PROJECT ID}.appspot.com/webhook (replace both {GOOGLE APP ENGINE PROJECT ID}s with the Google App Engine Project ID) to tell Telegram where to send web hooks. This is all that is required to setup web hooks, you do not need to tell the Bot Father anything about web hooks.

### Why the name Scenic Oxygen?
This repository contains code all my bots share. Scenic Oxygen is the codename Google gave my first ever bot.
