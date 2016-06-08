# Thorin
## A simple python bot for Telegram who does things and stuff.

### What is Thorin?
Thorin is a chat bot for telegram that makes is easy to add new commands. You can even add new commands while he's running!

### How does it work?
Thorin will listen for all messages in a given chat (either directly with him or in a chat room which you invite him to) starting with "/".

### How do I add new commands?
All you have to do is create a new python script in commands/ that has a function called run which takes three arguments, the first argument is the 
id of the chat to reply to, the second is the name of the user to address when replying (I'm going to change this to message_id in the future so the bot can reply to that message) and the third is the incoming message text.

tl;dr: Look at one of the existing commands, you must have a run(chat_id, user, message) function.

### How do I make my own bot using this?
Go to https://console.developers.google.com and create a Google App Engine project. Then take that project id (it will be two random words and a number eg. gorilla-something-374635) and your Telegram Bot ID which the Bot Father gave you and do the following:

1. Copy app.yaml.template and rename the copy to to app.yaml.
2. Update {GOOGLE APP ENGINE PROJECT ID} in app.yaml.
3. Copy keys.ini.template and rename the copy to keys.ini.
4. Update {Your Telegram Bot ID here} in keys.ini 
OPTIONAL:
5. Update the rest of keys.ini with keys for each command you want to use.

```bash
git clone (url for your thorin fork) ~/bot
cd ~/bot
(PATH TO PYTHON27 INSTALL)\scripts\pip.exe install -t lib python-telegram-bot bs4 xmltodict six soundcloud feedparser requests tungsten
(PATH TO GOOGLE APP ENGINE LAUNCHER INSTALL)appcfg.py -A {GOOGLE APP ENGINE PROJECT ID} update .
```

oh ja, /launch command needs a module called "dateutil", pip can't find it, GAE can't find it, a better man than I can fix that, I'm out.

When you add commands Thorin will pick them up when he's asked to perform them while running, this means that you don't need to restart Thorin to add 
new commands. However if you edit an existing command Thorin won't reload it until you restart him.

### Why the name Thorin?
I'm an alpha nerd and play Dungeons and Dragons, currently I'm playing a Dwarf Tempest Cleric in 5th edition named Thorin. 
I love Thorin and his name so that's how I named the bot. 

### Contributing

I love getting contributions, well I haven't gotten any yet but I'm sure that I'll love it!

The only thing I ask that if adding a new command that you include a description of it and how to configure it in the PR 
(using a module with it's on README would be da bomb, I'm working on this for my own commands now.) If you have an idea for 
a command or how we can add multiple backends to Thorin let me know via a Github Issue! I'd love to use Thorin on other chat services.

Open all PR's against the develop branch thanks!

### License Info

Thorin is distributed under the Apache 2.0 License
