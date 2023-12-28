#options_utilities.py
from typing import Dict
from menu_strings import menu_strings
from configuration_advanced import growth_rate

def read_options(options: Dict[int, str]) -> Dict[int, str]:
    """
    Prompts the user to enter the path to a file, and reads the options from the file.

    Parameters:
    options (Dict[int, str]): A dictionary of options.

    Returns:
    options (Dict[int, str]): A dictionary of options.
    """
    print()
    print("Please note, that the option file is case-sentitive.")
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
            break

        except FileNotFoundError:
            print("File not found, please try agian")

        except SyntaxError:
            print('File syntax error, use the template "options.txt"')

    return options

def convert_to_int(options: Dict[int, str]) -> Dict[int, str]:
    """
    Converts the values of the options to int, if possible.

    Parameters:
    options (Dict[int, str]): A dictionary of options.

    Returns:
    options (Dict[int, str]): A dictionary of options.
    """
    for key, value in options.items():
        try:
            options[key] = int(value)
        except ValueError:
            continue  #Do nothing if the value is not an int

    return options

def options_validater(options: Dict[int, str]) -> bool:
    """
    Checks if the options are valid
    Only checks, if the option is defined.

    Parameters:
    options (Dict[int, str]): A dictionary of options.

    Returns:
    bool: True if all options are valid, otherwise raises ValueError.
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
        if options.get("ini_woods") < 0 or options.get("ini_woods") > 100:
            raise ValueError("Value for ini_woods must be between 0 and 100")
        
    if "ini_fires" not in options:
        print("Initial fires not read from file.")
    elif options.get("ini_fires") not in ["default", "random"]:
        if not isinstance(options.get("ini_fires"), int):
            raise ValueError("Wrong value for ini_fires")
        else:
            if options.get("ini_fires") < 0 or options.get("ini_fires") > 100:
                raise ValueError("Value for ini_fires must be between 0 and 100")
        
    if "firefighter_num" not in options:
        print("Firefighter number not read from file.")
    else:
        if isinstance(options.get("firefighter_num"), str): #if str
            num = options.get("firefighter_num")
            num = num.split("%")[0]
            try:
                num = int(num)
                if num < 0:
                    raise ValueError("Value for firefighter_num must be between 0 and 100")
            except ValueError:
                raise ValueError("Wrong value for firefighter_num")
        else:
            if not isinstance(options.get("firefighter_num"), int): #if not str check if int
                raise ValueError("Wrong value for firefighter_num")
            else: 
                if options.get("firefighter_num") < 0:
                    raise ValueError("Value for firefighter_num must be positive")

    if "firefighter_level" not in options:
        print("Firefighter level not read from file.")
    elif not isinstance(options.get("firefighter_level"), int):
        raise ValueError("Wrong value for firefighter_level")
    else:
        if options.get("firefighter_level") < 1 or options.get("firefighter_level") > 3:
            raise ValueError("Value for firefighter_level must be between 1 and 3")
    
    if "iter_num" not in options:
        print("Iteration steps not read from file.")
    elif not isinstance(options.get("iter_num"), int): #not needed?
        raise ValueError("Wrong value for iter_num")
    else:
        if options.get("iter_num") < 1:
            raise ValueError("Value for iter_num must be positive")
    
    #Defaults are set prior to read, so checks are different.
    if not isinstance(options.get("growth_rate"), int):
        raise ValueError("Wrong value for growth_rate")
    else:
        if options.get("growth_rate") < 1:
            raise ValueError("Value for growth_rate must be positive")
    
    if not isinstance(options.get("burn_rate"), int):
        raise ValueError("Wrong value for burn_rate")
    else:
        if options.get("burn_rate") < 1:
            raise ValueError("Value for burn_rate must be positive")
    
    if not isinstance(options.get("new_forrest_probability"), int):
        raise ValueError("Wrong value for new_forrest_probability")
    else:
        if options.get("new_forrest_probability") < 1 or options.get("new_forrest_probability") > 100:
            raise ValueError("Value for new_forrest_probability must be between 1 and 100")
    
    if not isinstance(options.get("fire_spread_rate"), int):
        raise ValueError("Wrong value for fire_spread_rate")
    else:
        if options.get("fire_spread_rate") < 1:
            raise ValueError("Value for fire_spread_rate must be positive")

    return True

def advanced_defaults(options: Dict[int, str]) -> Dict[int, str]:
    """
    Sets default values for the advanced options.

    Parameters:
    options (Dict[int, str]): A dictionary of options.

    Returns:
    options (Dict[int, str]): A dictionary of options.
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