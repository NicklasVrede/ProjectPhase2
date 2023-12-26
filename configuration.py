"""
Config Module
"""
import random
from menu_strings import line, menu_strings
from options_utilities import advanced_defaults, read_file, convert_to_int, options_checker
from configuration_advanced import growth_rate, burn_rate, new_forrest_probability, fire_spread_rate

def welcome(options):
    options = advanced_defaults(options)
    print(menu_strings.get("welcome"))
    input()

    return read_options_from_file(options)

def read_options_from_file(options):
    print(menu_strings.get("read_options_from_file"))
    while True:
        user_input = input('Enter "1" or "2": ')

        if user_input == "1":
            break

        elif user_input == "2":
            return gen_method(options)

        else:
            print("Wrong input, please try agian")

    #Correct and check options
    options = read_file(options)
    options = convert_to_int(options)
    try:
        options_checker(options)
    except ValueError as error:
        print(str(error) + "\n" + "Please try again")
        return read_options_from_file(options)

    return gen_method(options)

def gen_method(options:dict=dict()):
    if options.get("gen_method"):
        return ini_woods(options)

    print(menu_strings.get("gen_method"))
    while True:
        user_input = input('Enter "1" or "r": ')

        if user_input == "1":
            choice = "read"
            break

        elif user_input == "r":
            choice = "random"
            break

        else:
            print("Wrong input, please try agian")

    options.update({"gen_method" : choice})
    
    return ini_woods(options)


def ini_woods(options:dict):
    if options.get("ini_woods"):
        return ini_fires(options)
    print(menu_strings.get("ini_woods"))

    while True:
        user_input = input('Enter "1", "2", "r": ')
        if user_input == "1":
            choice = 100
            break

        elif user_input == "2":
            choice = 0
            break

        elif user_input == "r":
            choice = random.randint(1, 100)
            break

        else:
            print("Wrong input, please try agian")

    options.update({"ini_woods" : choice})

    return ini_fires(options)
    
def ini_fires(options:dict):
    if options.get("ini_fires"):
        return firefighter_num(options)
    print(menu_strings.get("ini_fires"))

    while True:
        user_input = input('Enter "d" "r" or a number: ')

        if user_input == "r":
            choice = random.randint(1, 100)
            break

        elif user_input == "d":
            choice = "default"
            break

        try:
            choice = int(user_input)
            break

        except ValueError:
            print("Wrong input, please try agian")
        

    options.update({"ini_fires" : choice})


    return firefighter_num(options)


def firefighter_num(options:dict):
    if options.get("firefighter_num"):
        return firefighter_level(options)
    print(menu_strings.get("firefigter_num"))

    while True:
        user_input = input('Enter a number or "r" for random: ')
        if user_input == "r":
            choice = random.randint(1, 100)
            break

        try:
            choice = int(user_input)
            break

        except ValueError:
            print("Enter a whole number")

    
    options.update({"firefighter_num" : choice})


    return firefighter_level(options)

def firefighter_level(options:dict):
    if options.get("firefighter_level"):
        return iter_num(options)
    print(menu_strings.get("firefigter_level"))

    while True:
        user_input = input('Enter a "1", "2", "3", or "r" for random: ')
        if user_input == "r":
            choice = random.randint(1, 3)
            break

        try:
            choice = int(user_input)
            break

        except ValueError:
            print("Wrong input, please try agian")

    print(choice)
    options.update({"firefighter_level" : choice})


    return iter_num(options)

def iter_num(options:dict):
    if options.get("iter_num"):
        return config_final(options)
    print(menu_strings.get("iter_num"))

    while True:
        user_input = input('Enter a number, or "r" for random: ')
        if user_input == "r":
            choice = "r"
            break

        try:
            choice = int(user_input)
            break

        except ValueError:
            print("Enter a whole number")
            
    options.update({"iter_num" : choice})

    return config_final(options)

def change_setting(options):
    print(menu_strings.get("change_setting")(options))

    while True:
        user_input = input('Enter a number: ')
        if user_input == "1":
            options.update({"gen_method" : None})
            return gen_method(options)

        elif user_input == "2":
            options.update({"ini_woods" : None})
            return ini_woods(options)

        elif user_input == "3":
            options.update({"firefighter_num" : None})
            return firefighter_num(options)
    
        elif user_input == "4":
            options.update({"firefighter_level" : None})
            return firefighter_level(options)

        elif user_input == "5":
            options.update({"iter_num" : None})
            return iter_num(options)
        
        elif user_input == "6":
            options = dict()
            return welcome(options)
        
        elif user_input == "7":
            options.update({"growth_rate" : None, "burn_rate" : None, "new_forrest_probability" : None, "fire_spread_rate" : None})
            return growth_rate(options)
        
        elif user_input == "8":
            options.update({"growth_rate" : None})
            return growth_rate(options)

        elif user_input == "9":
            options.update({"burn_rate" : None})
            return burn_rate(options)
        
        elif user_input == "10":
            options.update({"new_forrest_probability" : None})
            return new_forrest_probability(options)
        
        elif user_input == "11":
            options.update({"fire_spread_rate" : None})
            return fire_spread_rate(options)
        
        elif user_input == "12":
            return config_final(options)
        
        else:
            print("Wrong input, please try agian")

      
def config_final(options:dict=dict()):
    print(menu_strings.get("config_final")(options))
    
    while True:
        user_input = input('Enter "1" or "2": ')

        if user_input == "1":
            print(line)
            from graph_forrest import main
            return main(options)

        elif user_input == "2":
            return change_setting(options)
   

if __name__ == "__main__":
    welcome(dict())