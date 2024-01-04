from config.menu_str import menu_strings
import random

def growth_rate(options:dict):
    if options.get("growth_rate"):
        return burn_rate(options)
    print(menu_strings.get("growth_rate"))

    string = 'Enter a number, "r" for random (5-50), or "d" for default (10): '
    while True:
        user_input = input(string)
        
        if user_input == "r":
            choice = random.randint(5, 50)
            break

        if user_input == "d":
            choice = 10
            break

        try:
            choice = int(user_input)
            if choice < 0:
                print("Enter a positive number")
                continue
            break

        except ValueError:
            print("Enter a whole number")

    options.update({"growth_rate" : choice})
    return burn_rate(options)

def burn_rate(options:dict):
    if options.get("burn_rate"):
        return new_forrest_probability(options)
    print(menu_strings.get("burn_rate"))

    string = 'Enter a number, "r" for random (5-50), or "d" for default (20): '
    while True:
        user_input = input(string)
        
        if user_input == "r":
            choice = random.randint(5, 50)
            break

        if user_input == "d":
            choice = 20
            break

        try:
            choice = int(user_input)
            if choice < 0:
                print("Enter a positive number")
                continue
            break

        except ValueError:
            print("Enter a whole number")

            
    options.update({"burn_rate" : choice})
    return new_forrest_probability(options)

def new_forrest_probability(options:dict):
    if options.get("new_forrest_probability"):
        return fire_spread_rate(options)
    print(menu_strings.get("new_forrest_probability"))

    string = 'Enter a number, "r" for random, or "d" for default (1 %): '
    while True:
        user_input = input(string)
        if user_input == "r":
            choice = random.randint(1, 100)
            break

        if user_input == "d":
            choice = 100
            break

        try:
            choice = int(user_input)
            if choice < 0 or choice > 10000:
                print("Enter a number between 0 and 10000")
                continue
            break

        except ValueError:
            print("Enter a whole number")
            
    options.update({"new_forrest_probability" : choice})
    return fire_spread_rate(options)


def fire_spread_rate(options:dict):
    if options.get("fire_spread_rate"):
        from config.config import config_final
        return config_final(options)
    print(menu_strings.get("fire_spread_rate"))

    string = 'Enter a number, "r" for random (1-100), or "d" for default (30): '
    while True:
        user_input = input(string)
        if user_input == "r":
            choice = random.randint(1, 100)
            break

        if user_input == "d":
            choice = 30
            break

        try:
            choice = int(user_input)
            if choice < 0 or choice > 100:
                print("Enter a number between 0 and 100")
                continue
            break

        except ValueError:
            print("Enter a whole number")
            
    options.update({"fire_spread_rate" : choice})
    from config.config import config_final
    return config_final(options)