#configuration_advanced.py
from menu_strings import menu_strings
import random

def growth_rate(options:dict):
    if options.get("growth_rate"):
        return burn_rate(options)
    print(menu_strings.get("growth_rate"))

    while True:
        user_input = input('Enter a number, or "r" for random (5-50), or "d" for default: ')
        if user_input == "r":
            choice = random.randint(5, 50)
            break

        if user_input == "d":
            choice = 10
            break

        try:
            choice = int(user_input)
            break

        except ValueError:
            print("Enter a whole number")

        print("Wrong input, please try agian")
            
    options.update({"growth_rate" : choice})

    return burn_rate(options)

def burn_rate(options:dict):
    if options.get("burn_rate"):
        return new_forrest_probability(options)
    print(menu_strings.get("burn_rate"))
    while True:
        user_input = input('Enter a number, "r" for random (5-50), "d" for default: ')
        if user_input == "r":
            choice = random.randint(5, 50)
            break

        if user_input == "d":
            choice = 20
            break

        try:
            choice = int(user_input)
            break

        except ValueError:
            print("Enter a whole number")

        print("Wrong input, please try agian")
            
    options.update({"burn_rate" : choice})

    return new_forrest_probability(options)

def new_forrest_probability(options:dict):
    if options.get("new_forrest_probability"):
        return fire_spread_rate(options)
    print(menu_strings.get("new_forrest_probability"))

    while True:
        user_input = input('Enter a number, "r" for random, or "d" for default: ')
        if user_input == "r":
            choice = random.randint(1, 100)
            break

        if user_input == "d":
            choice = 100
            break

        try:
            choice = int(user_input)
            break

        except ValueError:
            print("Enter a whole number")

        print("Wrong input, please try agian")
            
    options.update({"new_forrest_probability" : choice})

    return fire_spread_rate(options)


def fire_spread_rate(options:dict):
    if options.get("fire_spread_rate"):
        return config_final(options)
    print(menu_strings.get("fire_spread_rate"))

    while True:
        user_input = input('Enter a number, "r" for random (1-100) or "d" for default: ')
        if user_input == "r":
            choice = random.randint(1, 100)
            break

        if user_input == "d":
            choice = 30
            break

        try:
            choice = int(user_input)
            break

        except ValueError:
            print("Enter a whole number")

        print("Wrong input, please try agian")
            
    options.update({"fire_spread_rate" : choice})
    
    from configuration import config_final
    return config_final(options)