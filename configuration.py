"""
Config Module
"""
import random

options = {} #defined to express f-strings in menu_strings
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

    "read_options_from_file" : line + """
Would you like to read the options from a file?

1. Yes

2. No
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

    "change_setting" : line + f"""
Which option would you like to change?

1. Generation Method ({options.get("gen_method")})

2. Initial landscape pattern ({options.get("ini_woods")} %)

3. Firefighter number ({options.get("firefighter_num")})

4. Firefighter skill level ({options.get("firefighter_level")})

5. Iteration steps ({options.get("iter_num")})

Advanced options:
6. Tree growth rate ({options.get("tree_growth_rate")})

7. Tree burn rate ({options.get("tree_burn_rate")})

8. New random forrest probability ({options.get("new_forrest_probability")})

9. Fire spread rate ({options.get("fire_spread_rate")})

10. Proceed with graph generation.

All options:
11. All options. Restart the configuration.

"""
    
    }

def welcome(options):
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

    print()
    while True:
        user_input = input('Enter the path to the file, or press [Enter] to load "options.txt": ')
        if user_input == "":
            user_input = "options.txt"
        try:
            with open(user_input, "r") as file:
                lines = file.readlines()
            
            # Remove comments and strip whitespace
            lines = [line.split('#')[0].strip() for line in lines]

            # Join the lines back into a single string
            file_content = ''.join(lines)

            # Now you can evaluate the file content as before
            options = eval(file_content) 
            print(f'Options read from file: {options}')
            break

        except FileNotFoundError:
            print("File not found, please try agian")

        except SyntaxError:
            print('File syntax error, use the template "options.txt"')

    #Correct and check options
    options = convert_to_int(options)
    try:
        options_checker(options)
    except ValueError as error:
        print(str(error) + "\n" + "Please try again")
        return read_options_from_file(options)

    return gen_method(options)

def convert_to_int(options:dict):
    for key, value in options.items():
        try:
            options[key] = int(value)
        except ValueError:
            continue  #Do nothing if the value is not an int

    return options

def options_checker(options:dict):
    """
    Checks if the options are valid

    Only checks, if the option is defined.
    """
    if "gen_method" not in options:
        print("Generation method not read from file.")
    elif options.get("gen_method") not in ["read", "random"]:
        raise ValueError("Wrong value for gen_method")
    
    if "ini_woods" not in options:
        print("Initial woods not read from file.")
    elif options.get("ini_woods") not in ["default", "random"]:
        if not isinstance(options.get("ini_woods"), int):
            raise ValueError("Wrong value for ini_woods")
        
    if "ini_fires" not in options:
        print("Initial fires not read from file.")
    elif options.get("ini_fires") not in ["default", "random"]:
        if not isinstance(options.get("ini_fires"), int):
            raise ValueError("Wrong value for ini_fires")
        
    if "firefighter_num" not in options:
        print("Firefighter number not read from file.")
    elif not isinstance(options.get("firefighter_num"), int):
        raise ValueError("Wrong value for firefighter_num")
    
    if "firefighter_level" not in options:
        print("Firefighter level not read from file.")
    elif not isinstance(options.get("firefighter_level"), int):
        raise ValueError("Wrong value for firefighter_level")
    
    if "iter_num" not in options:
        print("Iteration steps not read from file.")
    elif not isinstance(options.get("iter_num"), int): #not needed?
        raise ValueError("Wrong value for iter_num")

    return True


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
        
        elif user_input == "6":

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

#Advanced options:
Tree growth rate: {options.get("tree_growth_rate")}
Tree burn rate: {options.get("tree_burn_rate")}
New random forrest probability: {options.get("new_forrest_probability")}
Fire spread rate: {options.get("fire_spread_rate")}

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
    welcome(dict())