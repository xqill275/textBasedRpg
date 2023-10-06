import class_script
import random
import pprint

controller = class_script.game_controller()
controller.set_running()

def char_sheet():
    if controller.running == False:
        print("The game is not running")
    else:
        player.show_char()

player_stats = controller.char_maker()
player = class_script.char("player",player_stats[0],player_stats[1],player_stats[2],player_stats[3],player_stats[4],player_stats[5])

player.make_char()
player.show_char()
controller.exsport_char(player)