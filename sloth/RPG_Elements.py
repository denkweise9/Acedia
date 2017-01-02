   # Format is the NPC, { Currency* dropped, XP Gained, Items dropped if any }
   # Current values are proposed, main point of this is the RPG model
   # Notice anything past the 2nd key in the sub dictionary is an item dropped.


'''
Things to do,

1) Separate values vertically by the following categories: 
  A) Animals
  B) Skeletons (undead races)
  C) Humans (Humanoid Races)
  D) Goblins (Bandosian Races (Ogres, hobgoblins, etc) )


2) Approve/Change Logic Structure

3) Approve/Change Values
  
'''


RPG_Elements = {
  

    #* Different race nations have different currencies

    #Non-Human NPC's
    "Goblin":{3,5,"Bones"}, 
    "Cow":{0,5,"Cow_Hide","Bones"},
    "Chicken":{0,3,"Feathers"},
    "Vampire":{500,1000,"Ashes","Heirloom"},
    "Wood Elf":{100,500,"Elf Bones","Crystal"},
    "Dark Elf":{100,600,"Elf Bones","Black Blood"},
    "Tree Gnome":{85,60,"Gnome Bones"},
    "Forest Gnome":{100,120,"Gnome Bones"},
    "Mountain Dwarf":{35,40,"Bones","Iron Pickaxe"},
    "Stray Dog":{0,10,"Bones"},
    
    #Human NPC's
    "Farmer":{15,15,"Knife","Pitch Fork","Bones"}, 
    "Man":{5,10,"Bones"},
    "Woman":{3,10,"Bones"},
    "Syler City Guard":{45,100,"Bones"},
    "Solider of Syler":{65,250,"Steel Longsword","Steel Helm"},
    "Knight":{120,275,"Bones","Steel Body","Steel Helm","Steel Plate Legs"},
    "Mugger":{40,40,"Bones","Face Mask"},
    "Bartender":{3,11,"Bones","Hops"},
    "Cook":{3,11,"Bones","Sugar","Nutmeg","Cinnamon"},
    "Child":{0,1,"Bones"},

    

}
