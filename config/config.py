import random
from typing import Dict, Union

from config.menu_str import line, menu_strings
from config.config_utils import (
    advanced_defaults, 
    read_options, 
    convert_to_int, 
    options_validater
    )
from config.config_adv import (
    growth_rate, 
    burn_rate, 
    new_forrest_probability, 
    fire_spread_rate
    )

def welcome(options: Dict[int, Union[str, int]] = dict()):
    options = advanced_defaults(options)
    print(menu_strings.get("welcome"))
    input()

    return read_options_from_file(options)

def read_options_from_file(options: Dict[int, Union[str, int]]):
    print(menu_strings.get("read_options_from_file"))
    while True:
        user_input = input('Enter "1" or "2": ')

        if user_input == "1":
            options = read_options(options)
            options = convert_to_int(options)
            options = options_validater(options)
            break

        elif user_input == "2":
           break
        
        else:
            print("Wrong input, please try agian")

    return gen_method(options)

def gen_method(options: Dict[int, Union[str, int]]):
    if options.get("gen_method"):
        return ini_woods(options)

    print(menu_strings.get("gen_method"))
    while True:
        user_input = input('Enter "1", "r" or "d": ')

        if user_input == "1":
            choice = "read"
            break

        elif user_input == "r" or user_input == "d":
            choice = "random"
            break

        else:
            print("Wrong input, please try agian")

    options.update({"gen_method" : choice})
    
    return ini_woods(options)


def ini_woods(options: Dict[int, Union[str, int]]):
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

        elif user_input == "d":
            choice = 80
            break

        elif user_input == "r":
            choice = random.randint(1, 100)
            break

        else:
            print("Wrong input, please try agian")

    options.update({"ini_woods" : choice})

    return ini_fires(options)
    
def ini_fires(options: Dict[int, Union[str, int]]):
    if options.get("ini_fires"):
        return firefighter_num(options)
    print(menu_strings.get("ini_fires"))

    while True:
        user_input = input('Enter "d" "r" or a number: ')

        if user_input == "r":
            choice = random.randint(1, 100)
            break

        elif user_input == "d":
            choice = 20
            break

        try:
            choice = int(user_input)
            if choice < 0:
                print("Enter a number greater than 0")
                continue
            if choice > 100:
                print("Enter a number less than 100")
                continue
            break

        except ValueError:
            print("Wrong input, please try agian")
        

    options.update({"ini_fires" : choice})


    return firefighter_num(options)


def firefighter_num(options: Dict[int, Union[str, int]]):
    if options.get("firefighter_num"):
        return firefighter_level(options)
    print(menu_strings.get("firefigter_num"))

    while True:
        user_input = input('Enter a amount, "r" for random or "d" for 10%: ')
        if user_input == "d":
            user_input = "10%"
        if user_input.endswith("%"):
            number = user_input.split("%")[0]
            try:
                number = int(number)
                if number < 0:
                    print("Enter a number greater than 0")
                    continue
                if len(user_input.split("%")) > 2: #check if there is more than one %
                    print("Wrong % format, please try agian")
                    continue
                choice = user_input
                break
            except ValueError:
                print("Wrong input, please try agian")
                continue

        if user_input == "r":
            choice = random.randint(1, 100)
            break

        try:
            choice = int(user_input)
            if choice < 0:
                print("Enter a number greater than 0")
                continue
            break

        except ValueError:
            print("Enter a whole number")

    
    options.update({"firefighter_num" : choice})


    return firefighter_level(options)

def firefighter_level(options: Dict[int, Union[str, int]]):
    if options.get("firefighter_level"):
        return iter_num(options)
    print(menu_strings.get("firefigter_level"))

    while True:
        user_input = input('Enter a "1", "2", "3", "r" for random: ')
        if user_input == "d":
            user_input = 3

        if user_input == "r":
            choice = random.randint(1, 3)
            break

        try:
            choice = int(user_input)
            if choice < 1 or choice > 3:
                print("Enter a number between 1 and 3")
                continue
            break

        except ValueError:
            print("Wrong input, please try agian")

    print(choice)
    options.update({"firefighter_level" : choice})


    return iter_num(options)

def iter_num(options: Dict[int, Union[str, int]]):
    if options.get("iter_num"):
        return config_final(options)
    print(menu_strings.get("iter_num"))

    while True:
        user_input = input('Enter a number, "r" (20-100), d2 for 40: ')
        if user_input == "d":
            user_input = 20

        if user_input == "r":
            choice = random.randint(20, 100)
            break

        try:
            choice = int(user_input)
            if choice < 1:
                print("Enter a number greater than 0")
                continue
            break

        except ValueError:
            print("Enter a whole number")
            
    options.update({"iter_num" : choice})

    return config_final(options)

def change_setting(options: Dict[int, Union[str, int]]):
    print(menu_strings.get("change_setting")(options))

    while True:
        user_input = input('Enter a number: ')
        if user_input == "1":
            options["gen_method"] = None
            return gen_method(options)

        elif user_input == "2":
            options["ini_woods"] = None
            return ini_woods(options)
        
        elif user_input == "3":
            options["ini_fires"] = None
            return ini_fires(options)

        elif user_input == "4":
            options["firefighter_num"] = None
            return firefighter_num(options)
    
        elif user_input == "5":
            options["firefighter_level"] = None
            return firefighter_level(options)

        elif user_input == "6":
            options["iter_num"] = None
            return iter_num(options)
        
        elif user_input == "7":
            options = dict()
            return welcome(options)
        
        elif user_input == "8":
            options.update(
                {"growth_rate" : None, 
                "burn_rate" : None, 
                "new_forrest_probability" : None, 
                "fire_spread_rate" : None}
                )
            return growth_rate(options)
        
        elif user_input == "9":
            options["growth_rate"] = None
            return growth_rate(options)

        elif user_input == "10":
            options["burn_rate"] = None
            return burn_rate(options)
        
        elif user_input == "11":
            options["new_forrest_probability"] = None
            return new_forrest_probability(options)
        
        elif user_input == "12":
            options["fire_spread_rate"] = None
            return fire_spread_rate(options)
        
        elif user_input == "13":
            return config_final(options)
        
        else:
            print("Wrong input, please try agian")

      
def config_final(options: Dict[int, Union[str, int]]): 
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