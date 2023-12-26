#options_utilities.py
from menu_strings import menu_strings
from configuration_advanced import growth_rate

def read_file(options:dict):
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
            options.update(eval(file_content))
            print(f'Options read from file: {options}')
            break

        except FileNotFoundError:
            print("File not found, please try agian")

        except SyntaxError:
            print('File syntax error, use the template "options.txt"')

    return options

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

def advanced_defaults(options:dict):
    """
    Sets the advanced options to default values, if not set.
    """
    if "growth_rate" not in options:
        options.update({"growth_rate" : 10})
    if "burn_rate" not in options:
        options.update({"burn_rate" : 20})
    if "new_forrest_probability" not in options:
        options.update({"new_forrest_probability" : 100})
    if "fire_spread_rate" not in options:
        options.update({"fire_spread_rate" : 30})

    return options