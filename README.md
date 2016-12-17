**Have you ever wanted to overthrow a kingdom?**    
  
Well, did you ever take into account what would happen if you did?  
The enemies you'd make, the new allies you'd have, and economical issues you'd cause?
  
**Imagine a game where your choices mattered.**  

**The way you speak, act, and approach other people and situations.**  
**All of these having an effect on the world around you.**  
**Welcome to Sloth, The Choices RPG**  


### What are your plans?
- https://github.com/Lvl4Sword/Sloth/wiki/Vision
  
### I want to help!
- That's great! Feel free to take a look at the following:  
    - https://github.com/Lvl4Sword/Sloth/issues/ 

- Our IRC channel is #sloth-game on irc.freenode.net if you'd like to come in and say hi.
  
### FAQ  
- WHERE ARE MY SETTINGS/LOGS?
    - They're stored in your home/user directory
    - for example /home/user or C:\Users\USERNAME  
- What operating systems are supported?  
    - The following have been tested:  
        - GNU/Linux: Arch, Debian 8, Fedora 23, Ubuntu 14.04 LTS  
        - Mac: 10.11 El Capitan  
        - Windows: 7/10  
- Python 2 or 3?  
    - 3, and it's also at the top of most of the .py files  
  
### How do I get this running?  
- Download the project using one of these ways:  
    - git  
    - https://github.com/Lvl4Sword/Sloth/archive/master.zip
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
- ( such as: virtualenv/bin/tox ~/sloth )

### What needs done for tests?:  
- main.py  
- start.py  
- finishing up store.py  

### What tests have been completed?:  
- None :-(

### FYI  
- This game is not remotely close to complete, and things may change.  
