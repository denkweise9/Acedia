#!/usr/bin/python3
#RPG_Elements.py

import sloth, random

#Races in Game
RPG_Elements_Races = {
"Elves":[],
"Humans":[],
"Dwarves":[],
"Goblins":[Goblin_reg, Goblin_general],
"Skeletons":[Zombie, Skeleton],
"Animals":[Cow, Pig, Chicke, Horse, Goat]
}

#Characters that are teamed with our user
RPG_Elements_Characters = {
     User,
     Ivan,

}


#NPC's to kill. Just General NPC's not quest/story related ones.
#Would contain Currency_Dropped, Items Dropped, and XP_Given.
RPG_Elements_NPCs = {
    Goblin_reg,
    Goblin_general,
    Skeleton,
    Cow,
    Pig,
    Horse,
    Chicken,
    Goat,
   

}



#below is an experiment, is not final, and needs updating
class Goblin_reg(object):
    agility = 3
    #charisma and intelligence are not applied because this is a regular npc goblin
    def __init__(self, life, attack_lvl, defence_lvl):   #rh = right hand, ll = left leg
        self.life = life
        self.attack_lvl = attack_lvl
        self.defence_lvl = defence_lvl
    def attack(self, target):
        if attack_lvl >= target.defence_lvl:
            target.life -= 10
            if taget.life <= 0:
                print("target dead")
                return False
            
class Goblin_general(object):
    agility = 3
    
    def __init__(self, life, attack_lvl, defence_lvl):  
        self.life = life
        self.attack_lvl = attack_lvl
        self.defence_lvl = defence_lvl
    def attack(self, target):
        if attack_lvl >= target.defence_lvl:
            target.life -= 10
            if taget.life <= 0:
                print("target dead")
                return False
              
class Goat(object):
     
     def __init__(self, life, attack_lvl, defence_lvl):
          self.life = life
          self.attack_lvl = attack_lvl
          self.defence_lvl = defence_lvl
     def attack(self, target):
         if attack_lvl >= target.defence_lvl:
             target.life -= 10
             if taget.life <= 0:
                 print("target dead")
                 return False
          
          
#The following below is for exmaples only
c = Goblin_reg(10,10,10)
g = Goblin_reg(10,10,10)

'''
The following was tested
In [69]: c.attack(g)
target dead
Out[69]: False
'''
