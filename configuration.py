"""
Config Module
"""
import random

line =  "\n"*3 + "-" * 40 + "\n"*3
menu_strings = {
    "welcome" : line + """
Welcome to the Forest Fire Simulation Program!

In this simulation, you will explore the dynamic evolution of a population 
of automata in a simulated forest environment. The fate of the landscape 
is in your hands as you influence the growth of trees, the movement of firefighters, 
and the spread of wildfires.

Press [Enter] to embark on this exciting journey and configure the simulation parameters.
""",

    "gen_method" : line + """
Please pick a generation method of the graph.

1. From file

r. Random
    """,

    "ini_woods" : line + """
Choose an option for the initial landscape pattern:

1. All woods

2. All rocks

r. Random amount of woods (between 0% and 100 %)
    """,

    "firefigter_num" : line + """
Choose the number of firefighter.
    """,

    "ini_fires" : line + """
Enter the initial percentage of fires. (As a whole number)
d. Default (3% percent of woods)

r. Random number (between 0% and 100 %)
    """,

    "firefigter_level" : line + """
Choose the average skill level firefighters:

1. Low

2. Medium

3. High
    """,

    "iter_num" : line + """
How many iteration steps would you like?
    """,

    "change_setting" : line + """
Which option would you like to change?

1. Generation Method

2. Initial landscape pattern

3. Firefighter number

4. Firefighter skill level

5. Iteration steps

6. All
    """
    
    }

def welcome(options):
    print (menu_strings.get("welcome"))
    input()

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
            choice = "r"
            break

        try:
            choice = int(user_input)
            break

        except ValueError:
            print("Enter a whole number")

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
    print(menu_strings.get("change_setting"))

    while True:
        user_input = input('Enter "1", "2", "3", "4" or "5":')
        if user_input == "1":
            return gen_method(options)

        elif user_input == "2":
            return ini_woods(options)

        elif user_input == "3":
            return firefighter_num(options)
    
        elif user_input == "4":
            return firefighter_level(options)

        elif user_input == "5":
            return iter_num(options)

        else:
            print("Wrong input, please try agian")
      
def config_final(options:dict=dict()):
    print(line + f"""
Current options:

Generation Method: {options.get("gen_method")}
Initial woods: {options.get("ini_woods")} %
Initial fires: {options.get("ini_fires")} %
Firefighter number: {options.get("firefighter_num")}
Firefighter skill level: {options.get("firefighter_level")}
Iteration steps: {options.get("iter_num")}

How would you like to proceed?

1. Proceed with graph generation

2. Change a setting.
""")
    
    while True:
        user_input = input('Enter "1" or "2": ')

        if user_input == "1":
            print(line)
            from graph_forrest import main
            return main(options)

        elif user_input == "2":
            return change_setting(options)
   


if __name__ == "__main__":
    welcome()