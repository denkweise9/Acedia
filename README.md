**HAVE YOU EVER WANTED TO FIGHT HUGE DRAGONS?**  
**WHAT ABOUT KICK A SKELETON IN THE TEETH?**  
**MAN THOSE SOUND AMAZING, DON'T THEY?**  
  
Well, imagine an RPG game tied to your physical fitness.  
The stronger YOU get, the stronger your character gets.  
  
**SO GO OUT AND TRAIN SO YOU CAN SHOW NO MERCY TO YOUR ENEMIES!**  
  
### I want to help!
- That's great! Feel free to take a look at the following:  
    - https://bitbucket.org/pride/sloth/issues?status=new&status=open&sort=-priority  
        - Everything at the top is what I'd like to be done first.  
        - You're free to work on whatever you'd like as long as it's not assigned to someone else.  
        - ( You're free to get in contact with them and see if they need help, though. )  
- Our IRC channel is #sloth-game on irc.freenode.net if you'd like to come in and say hi.
  
### FAQ  
- WHERE ARE MY SETTINGS/LOGS?
    - They're stored in the directory you were in when you started the program.  
- What operating systems are supported?  
    - The following have been tested:  
        - GNU/Linux: Arch, Debian 8, Fedora 23, Ubuntu 14.04 LTS  
        - Mac: 10.11 El Capitan  
        - Windows: 7/10  
- Python 2 or 3?  
    - 3, and it's also at the top of most of the .py files  
- What exactly does this program give me?  
    - Motivation in the form of:  
        - Deteriorating experience points ( 20% ) for every 7 days you haven't logged anything.
            - The first level ( 0 - 249 XP ) is a safe zone  
        - Weekly bosses ( not yet implemented )  
        - Monsters to fight ( not yet implemented )  
        - Items [ armor, weapons, gold, etc ] ( not yet implemented )  
    - Ability to log every exercise you do, and complete access to your data  
  
### How do I get this running?  
- Download the project using one of these ways:  
    - git  
    - https://bitbucket.org/pride/sloth/downloads  
    - https://bitbucket.org/pride/sloth/get/HEAD.zip  
- A virtualenv is not necessary, but recommended  
- I'm using Windows:  
    - Download python3 for your architecture from python.org  
        - MAKE SURE PYTHON IS SET TO BE INSTALLED IN YOUR PATH!  
    - pip install virtualenv  
    - virtualenv C:/sloth-virtualenv  
    - C:/sloth-virtualenv/scripts/pip.exe install pyreadline  
    - C:/sloth-virtualenv/scripts/python.exe setup.py install  
    - C:/sloth-virtualenv/scripts/sloth-game.exe  
- I'm using Linux:  
    - Download python3 using your repo  
    - apt-get install python3-virtualenv  
    - virtualenv -p python3 sloth-virtualenv  
    - Store the game in ~/sloth  
    - if distro == 'Ubuntu':    
        - sloth-virtualenv/bin/pip install -U setuptools  
    - sloth-virtualenv/bin/pip install ~/sloth  
    - sloth-virtualenv/bin/sloth-game  
- I'm using Mac:  
    - Download python3 for your architecture from python.org  
        - MAKE SURE PYTHON IS SET TO BE INSTALLED IN YOUR PATH!  
    - Store the game in ~/sloth  
    - pip3 install virtualenv  
    - virtualenv -p python3 ~/sloth/virtualenv  
    - virtualenv/bin/pip install ~/sloth  
    - virtualenv/bin/sloth-game  
- I use something else:  
    - Let me know what you're running and I'll help you.   
  
### How do I run the tests?  
- Install tox, and run it inside the repository directory  

### What needs done for tests?:  
- cardio.py  
- main.py  
- physical.py  
- start.py  
- finishing up store.py  
- workouts.py  

### What tests have been completed?:  
- userinput.py  

### Test coverage:  

```
Name                                             Stmts   Miss  Cover  
--------------------------------------------------------------------  
lib/python3.4/site-packages/sloth/__init__.py        0      0   100%  
lib/python3.4/site-packages/sloth/physical.py        8      6    25%  
lib/python3.4/site-packages/sloth/store.py         106     27    75%  
lib/python3.4/site-packages/sloth/userinput.py     241      0   100%  
--------------------------------------------------------------------  
TOTAL                                              355     33    91%  
```

### FYI  
- This game is not remotely close to complete, and things may change.  
