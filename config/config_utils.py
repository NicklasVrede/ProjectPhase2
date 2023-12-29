#options_utilities.py
from typing import Dict, Union

def read_options(options: Dict[int, Union[str, int]]) -> Dict[int, Union[str, int]]:
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
        user_input = input('Enter the path to the file, press [Enter] to load "options.txt" or type "back": ')
        if user_input == "":
            user_input = "options.txt"

        if user_input == "back":
            from config.config import read_options_from_file
            return read_options_from_file(options)
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

def convert_to_int(options: Dict[int, Union[str, int]]) -> Dict[int, Union[str, int]]:
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

def options_validater(options: Dict[int, Union[str, int]]) -> Dict[int, Union[str, int]]:
    """
    Checks if the options are valid
    Only checks, if the option is defined.

    Parameters:
    options (Dict[int, str]): A dictionary of options.

    Returns:
    bool: True if all options are valid, otherwise raises ValueError.
    """
    for option in ["ini_woods", "ini_fires"]:
        if option in options:
            if not isinstance(options.get(option), int) or not 0 <= options.get(option) <= 100:
                print(f'Wrong value for {option}: {options.get(option)}')
                print(f'Please reasign in basic config.')
                options[option] = None #Reset, so user must pick in basic config


    for option in ["iter_num", "growth_rate", "burn_rate", "new_forrest_probability", "fire_spread_rate"]:
        if option in options:
            if not isinstance(options.get(option), int) or options.get(option) < 0:
                print(f'Value for {option}, must be positive')
                print(f'Please reasign or use default')
                options[option] = None

    if "gen_method" in options and options.get("gen_method") not in ["read", "random"]:
        print(f'Wrong value for gen_method: {options.get("gen_method")}')
        print(f'Please reasign in basic config.')
        options["gen_method"] = None
    

    if "firefighter_level" in options and not 0 < options.get("firefighter_level") < 4:
        print(f'Wrong value for firefighter_level: {options.get("firefighter_level")}')
        print(f'Please reasign in basic config.')
        options["firefighter_level"] = None
    

    if "firefighter_num" in options and isinstance(options.get("firefighter_num"), str):
        num = options.get("firefighter_num")
        num = num.split("%")[0]
        try:
            num = int(num)
            if num < 0:
                raise ValueError("Value for firefighter_num must be between 0 and 100")
        except ValueError:
            raise ValueError("Wrong value for firefighter_num")
    else:
        if "firefighter_num" in options:
            if options.get("firefighter_num") < 0:
                print(f'Value for "firefighter_num must be positive')
                print(f'Please reasign in basic config.')
                options["firefighter_num"] = None

    return options

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