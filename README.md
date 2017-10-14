# Scenic Oxygen
## A simple shell for hosting python bots on Google App Engine.

### What is Scenic Oxygen?
Scenic Oxygen turns Google App Engine into Google Bot Engine.

### How does it work?
Scenic Oxygen can: 
1. Perform *autherization* for for linking bots together or to the web.
2. Perform scheduled *CRON jobs* and *store data* about bot's state. 
3. Listens for all messages in many chat groups (either directly with him or in a group chat room) starting with a forward slash  (eg: "/get happy dog"). These "slashtags" are used to execute explicit commands. If that message is "/login" or "/login some_new_password" then the bot executes the python file in "commands/login.py". For example "/get happy dog" would execute the python file "commands/get.py" and pass it the text "happy dog".
4. Hook into Github repositories to automatically update commands.

### What is commands/login.py?
The login command stores encrypted passwords that other bots and websites use to execute commands remotely and send messages to the chat room in the bot's name. All commands are handled by seperate python files in the "commands/" folder. These command files distinguish the bots from each other. If two bots both have a file "commands/executeme.py" and they are both members of the same group chat room then whenever a user sends the slashtag "/executeme" both of them will respond. Unless they are programmed not to like the login command is.

### How do I add new commands?
Create a seperate GitHub repo. Add a folder called "commands" and add each command into that folder as a seperate python file named after the command. Send a message to the bot who is running Scenic Oxygen of the form: "/add [[Repo Username or Organization Name]] [[Repo Name]] [[Acces Token]]" Where [[Repo Username or Organization Name]] and [[Repo Name]] are parts of the git hub url of the repo and [[Acces Token]] is a Personal Access token granted to you by GitHub (in your user settings) which permission to create hooks, delete hooks and read content on the new command's repository. Scenic Oxygen willl automatically update from Github when there is a push to the hooked repository.

tl;dr: Look at one of the existing commands, you must have a run(chat_id, user, request_text, keyConfig, number_of_responses) function.

### How do I make my own bot using this?
Go to https://console.developers.google.com and create a Google App Engine project. Then take that project id (it could be two random words and a number eg. gorilla-something-374635 depending on if your chosen name was taken) and your Telegram Bot ID which the Bot Father gave you and do the following:

1. Copy bot_keys.ini.template and rename the copy to bot_keys.ini.
2. Update {Your Telegram Bot ID here} in bot_keys.ini and do the same for Discord, Skype and Facebook bots.

```bash
git clone (url for your Scenic Oxygen fork) ~/bot
cd ~/bot
(PATH TO PYTHON27 INSTALL)\scripts\pip.exe install -t lib python-telegram-bot
(PATH TO GOOGLE APP ENGINE LAUNCHER INSTALL)appcfg.py -A {GOOGLE APP ENGINE PROJECT ID} update .
```

Finally go to https://{GOOGLE APP ENGINE PROJECT ID}.appspot.com/set_webhook?url=https://{GOOGLE APP ENGINE PROJECT ID}.appspot.com/webhook (replace both {GOOGLE APP ENGINE PROJECT ID}s with the Google App Engine Project ID) to tell Telegram where to send web hooks. This is all that is required to setup web hooks, you do not need to tell the Bot Father anything about web hooks.

### Why the name Scenic Oxygen?
This repository contains code all my personalized Goole App Engine code. Scenic Oxygen is the codename Google gave my first ever App Engine project.
