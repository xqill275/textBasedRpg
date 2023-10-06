import class_script
import random
import pprint
import os

controller = class_script.game_controller()
controller.set_running()

# search the "game_files" folder for a file named that ends with ".py"
# if it finds one, it display the name of the file and ads it to an array
# it then asks if you want to load one of the files

def load_game():
    game_files = os.listdir("game_files")
    found_files = []
    for file in game_files:
        if file.endswith(".py"):
            print(f"found: {file}")
            found_files.append(file)
    if len(found_files) > 0:
        print("would you like to load one of these files?")
        for file in found_files:
            print(f"{found_files.index(file)}: {file}")
        load_file = input("file number: ")
        if load_file.isdigit():
            load_file = int(load_file)
            if load_file < len(found_files):
                controller.load_game("game_files/"+found_files[load_file])
            else:
                print("invalid file number")
        else:
            print("invalid file number")
load_game()


# test script