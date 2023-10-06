import math
import random
import pprint
import os
import json

class game_controller():
    def __init__(self):
        self.running = False

    def set_running(self):
        if self.running == False:
            self.running = True
        else:
            self.running = False

    def roll_dice(self,num_rolls,dice,setting,bonus):
        using_bonus = False
        if self.running == True:
            if bonus != 0:
                using_bonus = True
            total = 0
            dice_output = []
            if setting == "show":
                print("rolling "+str(num_rolls)+"D"+str(dice))
            for x in range(num_rolls):
                rolled = random.randint(1,dice)
                dice_output.append(rolled)
                total = (total + rolled) + bonus
            if setting == "show":
                print("dice output:"+ str(dice_output))
            return total
        
    def load_game(self,game_file):
        with open(game_file,"r") as f:
            exec(f.read())
    
    def char_maker(self):
        print("welcome what is your name?")
        if self.running == False:
            print("The game is not running")
        else:
            name = input("name: ")
            stats = []
            print("generating stats...")
            for x in range(6):
                stat_num = self.roll_dice(1,20,"n",0)
                stats.append(stat_num)
            return stats

    def exsport_char(self,char):
        char_dict = vars(char)
        with open("game_files/characters/"+char.name+".json","w") as f:
            json.dump(char_dict,f)

    def import_char(self,char_name):
        # import the json file
        with open("game_files/characters/"+char_name+".json","r") as f:
            char_dict = json.load(f)
        # create a new class with the dictionary
        char = char(char_dict["name"],char_dict["strength"],char_dict["dexterity"],char_dict["constitution"],char_dict["intelligence"],char_dict["wisdom"],char_dict["charisma"])
        # update the class with the dictionary
        char.update_strength(char_dict["strength"])
        char.update_dexterity(char_dict["dexterity"])
        char.update_constitution(char_dict["constitution"])
        char.update_intelligence(char_dict["intelligence"])
        char.update_wisdom(char_dict["wisdom"])
        char.update_charisma(char_dict["charisma"])
        char.update_stat_bonus()
        char.update_ac()
        char.update_initative()
        char.calculate_max_weight()
        char.calculate_hp()
        char.update_inventory(char_dict["inventory"])
        char.update_equipped(char_dict["equipped"])
        char.update_spells(char_dict["spells"])
        return char


        
    
class char():
    def __init__(self,name,strength,dexterity,constitution,intelligence,wisdom,charisma):
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.level = 1
        self.strength_bonus = 0
        self.dexterity_bonus = 0
        self.constitution_bonus = 0
        self.intelligence_bonus = 0
        self.wisdom_bonus = 0
        self.charisma_bonus = 0
        self.proficiency_bonus = 2
        self.saving_throws = {
            "strength": 0,
            "dexterity": 0,
            "consitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0
        }
        self.skills = {
            "Acrobatics": 0,
            "Animal_Handling": 0,
            "Arcana": 0,
            "Athletics": 0,
            "Deception": 0, 
            "History": 0,
            "Insight": 0, 
            "Intimidation": 0,
            "Investigation": 0,
            "Medicine": 0,
            "Nature": 0,
            "Perception": 0,
            "Performance": 0,
            "Persuasion": 0,
            "Religion": 0,
            "Sleight_of_Hand": 0,
            "Stealth": 0,
            "Survival": 0
        }
        self.armor_class = 0
        self.initative = 0
        self.speed = 0
        self.hit_points = 0
        self.hit_dice = 10
        self.death_saves = {
            "successes": 0,
            "fails": 0
         }
        self.inventory = []
        self.max_weight = 0
        self.current_weight = 0
        self.equipped = {
            "Armour": "",
            "Weapon": ""
        }
        self.spells = {
            "Cantrips": [],
            "Level_1": [],
            "Level_2": [],
            "Level_3": [],
            "Level_4": [],
            "Level_5": [],
            "Level_6": [],
            "Level_7": [],
            "Level_8": [],
            "Level_9": []
        }

    def update_strength(self,new_val):
        self.strength = new_val

    def update_str_bonus(self,new_val):
        self.strength_bonus = new_val

    def update_dexterity(self,new_val):
        self.dexterity = new_val

    def update_dex_bonus(self,new_val):
        self.dexterity_bonus = new_val

    def update_constitution(self,new_val):
        self.constitution = new_val

    def update_con_bonus(self,new_val):
        self.constitution_bonus = new_val

    def update_intelligence(self,new_val):
        self.intelligence = new_val

    def update_int_bonus(self,new_val):
        self.intelligence_bonus = new_val
    
    def update_wisdom(self,new_val):
        self.wisdom = new_val

    def update_wis_bonus(self,new_val):
        self.wisdom_bonus = new_val

    def update_charisma(self,new_val):
        self.charisma = new_val

    def update_char_bonus(self,new_val):
        self.charisma_bonus = new_val

    def cal_bonus(self,value):
        return math.floor((value - 10) / 2)
    
    def update_stat_bonus(self):
        stats = [self.strength,self.dexterity,self.constitution,self.intelligence,self.wisdom,self.charisma]
        update_list = [self.update_str_bonus,self.update_dex_bonus,self.update_con_bonus,self.update_int_bonus,self.update_wis_bonus,self.update_char_bonus]
        bonus = []
        for x in stats:
            num = self.cal_bonus(x)
            bonus.append(num)
        for x in update_list:
            index = update_list.index(x)
            x(bonus[index])
        self.update_saving_throws(bonus)
        self.update_skills(bonus)

    def update_saving_throws(self,bonus):
        z = 0
        for x,y in self.saving_throws.items():
            self.saving_throws[x] = bonus[z]
            z += 1

    def update_skills(self,bonus):
        z = 0
        strength_skills = ["Athletics"]
        dexterity_skills = ["Acrobatics","Sleight_of_Hand","Stealth"]
        constitution_skills = []
        intelligence_skills = ["Arcana","History","Investigation","Nature","Religion"]
        wisdom_skills = ["Animal_Handling","Insight","Medicine","Perception","Survival"]
        charisma_skills = ["Deception","Intimidation","Performance","Persuasion"]
        ordered_skills = [strength_skills,dexterity_skills,constitution_skills,intelligence_skills,wisdom_skills,charisma_skills]
        print(self.skills)
        for x in ordered_skills:
            for y in x:
                self.skills[y] = bonus[z]
            z += 1
        print(self.skills)

    def make_proficent(self,option,skill):
        if skill in self.saving_throws or skill in self.skills:
            if option == "save":
                self.saving_throws[skill] = self.saving_throws[skill] + self.proficiency_bonus
            elif option == "skill":
                self.skills[skill] += self.proficiency_bonus
            else:
                print("unknown dictionary")
        else:
            print("skill not known")
    
    def update_ac(self):
        if self.equipped["Armour"] == "":
            self.armor_class = 10 + self.dexterity_bonus
        else:
            self.armor_class = self.equipped["Armour"].ac + self.dexterity_bonus

    def calculate_max_weight(self):
        self.max_weight = 15 * self.strength
    
    def update_speed(self,new_speed):
        self.speed = new_speed

    def update_initative(self):
        self.initative = self.dexterity_bonus

    def calculate_hp(self):
        temp_hp = 0
        if self.level > 1:
            rand_score = 0
            for x in range(self.level):
                if temp_hp == 0:
                    temp_hp += (12 + self.constitution_bonus)
                rand = random.randint(0,self.hit_dice)
                if rand < 7:
                    temp_hp += (7 + self.constitution_bonus)
                else:
                    temp_hp += (rand + self.constitution_bonus)
        else:
            temp_hp += (12 + self.constitution_bonus)
        self.hit_points = temp_hp
        print("test hp :"+ str(self.hit_points))

    def update_hp(self,new_hp):
        self.hit_points = new_hp

    def make_char(self):
        self.update_stat_bonus()
        self.update_speed(30)
        self.update_ac()
        self.update_initative()
        self.calculate_max_weight()
        self.calculate_hp()

    def show_char(self):
        pprint.pprint(vars(self))

    def update_inventory(self,item):
        self.inventory.append(item)
        self.current_weight += item.weight

    def equip_item(self,item):
        if item.ac != 0:
            self.equipped["Armour"] = item.name
            self.update_ac()
        elif item.damage != 0:
            self.equipped["Weapon"] = item.name
            self.weapon = item
        else:
            print("item is not equippable")

    def unequip_item(self,item):
        if item.ac != 0:
            self.equipped["armour"] = ""
            self.update_ac()

class weapon:
    def __init__(self,name,damage,weapon_range,weight):
        self.name = name
        self.damage = damage
        self.weapon_range = weapon_range
        self.weight = weight

class armour:
    def __init__(self,name,ac,weight):
        self.name = name
        self.ac = ac
        self.weight = weight

class item:
    def __init__(self,name,weight):
        self.name = name
        self.weight = weight

class spell:
    def __init__(self,name,level,casting_time,range,components,duration,description):
        self.name = name
        self.level = level
        self.casting_time = casting_time
        self.range = range
        self.components = components
        self.duration = duration
        self.description = description



armour_test = armour("test_armour",10,10)
weapon_test = weapon("test_weapon",10,10,10)
item_test = item("test_item",10)


