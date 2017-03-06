#!/usr/bin/python3
#RPG_Elements.py

'''
    RPG_Elements.py contains all the elements and data needed for npc's 
    Copyright (C) 2017 Acedia, Lvl4Sword     Authors: Denkweise9, Lvl4Sword

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/.
'''

import sloth, random

# Values are Races in Game, Keys are the classes to each object
RPG_Elements_Races = {
"Elves":[Elf_general, Elf_guard],
"Humans":[General, Guard, Farmer, Blacksmith, Merchant],
"Dwarves":[Dwarf_guard],
"Goblins":[Goblin_reg, Goblin_general, Goblin_guard],
"Skeletons":[Zombie, Skeleton],
"Animals":[Cow, Pig, Chicken, Horse, Goat]
}

# Values are Characters that are teamed with our user through quests and adventure, keys are the stats
RPG_Elements_Characters = {
     User:{},
     Ivan:{},

}


#NPC's to kill. Just General NPC's not quest/story related ones.
#Would contain Currency_Dropped, Items Dropped, and XP_Given.
RPG_Elements_NPCs = {
    Goblin_reg:{},
    Goblin_general:{},
    Skeleton:{},
    Cow:{},
    Pig:{},
    Horse:{},
    Chicken:{},
    Goat:{},
   

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
    intelligence = 10
    
    def __init__(self, life, attack_lvl, defence_lvl, agility_lvl, charisma_lvl, strength_lvl, 
               rh, lh, rl, ll ): #rh = right hand, ll = left leg. these slots hold equipment  
        self.life = life
        self.attack_lvl = attack_lvl
        self.defence_lvl = defence_lvl
        self.agility_lvl = agility_lvl
        self.charisma_lvl = charisma_lvl
        self.strength_lvl = strength_lvl
        self.rh = rh
        self.lh = lh
        self.rl = rl
        self.ll = ll
    def attack(self, target):
        if attack_lvl >= target.defence_lvl:
            target.life -= 10
            if taget.life <= 0:
                print("target dead")
                return False
              
class General(object  #this is basically a human general
    intelligence = 10
    living = True
    
    def __init__(self, life, attack_lvl, defence_lvl, agility_lvl, charisma_lvl, strength_lvl, 
               rh, lh, rl, ll ): #rh = right hand, ll = left leg. these slots hold equipment  
        self.life = life
        self.attack_lvl = attack_lvl
        self.defence_lvl = defence_lvl
        self.agility_lvl = agility_lvl
        self.charisma_lvl = charisma_lvl
        self.strength_lvl = strength_lvl
        self.rh = rh
        self.lh = lh
        self.rl = rl
        self.ll = ll
    def attack(self, target):
        if attack_lvl >= target.defence_lvl:
            target.life -= 10
            if taget.life <= 0:
                living = False
                print("target dead")
                return living
              
              
              
#This code is modular, so fixing one animal class can apply to others        
class Goat(object):
     living = True

     def __init__(self, life, attack_lvl, strength_lvl, defence_lvl):
          self.life = life
          self.attack_lvl = attack_lvl
          self.strength_lvl = strength_lvl
          self.defence_lvl = defence_lvl
     def attack(self, target):
         if attack_lvl >= target.defence_lvl:
             target.life -= 10
             if taget.life <= 0:
                 living = False
                 print("target dead")
                 return living

class Pig(object):
     living = True

     def __init__(self, life, attack_lvl, strength_lvl, defence_lvl):
          self.life = life
          self.attack_lvl = attack_lvl
          self.strength_lvl = strength_lvl
          self.defence_lvl = defence_lvl
     def attack(self, target):
         if attack_lvl >= target.defence_lvl:
             target.life -= 10
             if taget.life <= 0:
                 living = False
                 print("target dead")
                 return living

class Horse(object):
     living = True

     def __init__(self, life, attack_lvl, strength_lvl, defence_lvl):
          self.life = life
          self.attack_lvl = attack_lvl
          self.strength_lvl = strength_lvl
          self.defence_lvl = defence_lvl
     def attack(self, target):
         if attack_lvl >= target.defence_lvl:
             target.life -= 10
             if taget.life <= 0:
                 living = False
                 print("target dead")
                 return living    

class Chicken(object):
     living = True

     def __init__(self, life, attack_lvl, strength_lvl, defence_lvl):
          self.life = life
          self.attack_lvl = attack_lvl
          self.strength_lvl = strength_lvl
          self.defence_lvl = defence_lvl
     def attack(self, target):
         if attack_lvl >= target.defence_lvl:
             target.life -= 10
             if taget.life <= 0:
                 living = False
                 print("target dead")
                 return living      

class Cow(object):
     living = True

     def __init__(self, life, attack_lvl, strength_lvl, defence_lvl):
          self.life = life
          self.attack_lvl = attack_lvl
          self.strength_lvl = strength_lvl
          self.defence_lvl = defence_lvl
     def attack(self, target):
         if attack_lvl >= target.defence_lvl:
             target.life -= 10
             if taget.life <= 0:
                 living = False
                 print("target dead")
                 return living

class Dog(object):
     living = True

     def __init__(self, life, attack_lvl, strength_lvl, defence_lvl):
          self.life = life
          self.attack_lvl = attack_lvl
          self.strength_lvl = strength_lvl
          self.defence_lvl = defence_lvl
     def attack(self, target):
         if attack_lvl >= target.defence_lvl:
             target.life -= 10
             if taget.life <= 0:
                 living = False
                 print("target dead")
                 return living


class Cat(object):
     living = True

     def __init__(self, life, attack_lvl, strength_lvl, defence_lvl):
          self.life = life
          self.attack_lvl = attack_lvl
          self.strength_lvl = strength_lvl
          self.defence_lvl = defence_lvl
     def attack(self, target):
         if attack_lvl >= target.defence_lvl:
             target.life -= 10
             if taget.life <= 0:
                 living = False
                 print("target dead")
                 return living

class Wolf(object):
     living = True

     def __init__(self, life, attack_lvl, strength_lvl, defence_lvl):
          self.life = life
          self.attack_lvl = attack_lvl
          self.strength_lvl = strength_lvl
          self.defence_lvl = defence_lvl
     def attack(self, target):
         if attack_lvl >= target.defence_lvl:
             target.life -= 10
             if taget.life <= 0:
                 living = False
                 print("target dead")
                 return living
#The following below is for exmaples only
c = Goblin_reg(10,10,10)
g = Goblin_reg(10,10,10)

'''
The following was tested
In [69]: c.attack(g)
target dead
Out[69]: False
'''
