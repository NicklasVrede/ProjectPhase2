from typing import Dict, Union


def read_options(
        options: Dict[int, Union[str, int]]
        ) -> Dict[int, Union[str, int]]:
    """
    Prompts the user to enter the path to a file, 
    and reads the options from the file.

    Parameters:
    options (Dict[int, str]): A dictionary of options.

    Returns:
    options (Dict[int, str]): A dictionary of options.
    """
    def read_file(file_path: str) -> Dict[int, Union[str, int]]:
        """
        Reads the options from a file.

        Parameters:
        file_path (str): The path to the file.

        Returns:
        options (Dict[int, str]): A dictionary of options.
        """
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        # Remove comments and strip whitespace
        lines = [line.split('#')[0].strip() for line in lines]

        # Join the lines back into a single string
        file_content = ''.join(lines)

        # Now you can evaluate the file content as before
        options.update(eval(file_content))

        return options

    print()
    print("Please note, that the option file is case-sentitive.")
    
    string = "Enter the path to the file, press [Enter] to load 'options.txt' or type 'back':"
    while True:
        user_input = input(string) 
        if user_input == "":
            user_input = "options.txt"

        if user_input == "back":
            from config.config import read_options_from_file
            return read_options_from_file(options)
        
        try:
            options = read_file("config/" + user_input)
            break
        
        except FileNotFoundError:
            try:
                options = read_file(user_input)
                break

            except FileNotFoundError:
                print("File not found, please try agian")
            
            except SyntaxError:
                print('File syntax error, use the template "options.txt"')

            except NameError:
                print('NameError, please check format of the options')
        
        except SyntaxError:
            print('File syntax error, use the template "options.txt"')

        except NameError:
                print('NameError, please check format of the options')

    return options

def convert_to_int(
                    options: Dict[int, Union[str, int]]
                    ) -> Dict[int, Union[str, int]]:
    """
    Converts the values of the options to int, if possible.

    Parameters:
    options (Dict[int, str]): A dictionary of options.

    Returns:
    options (Dict[int, str]): A dictionary of options.
    """
    for key, value in options.items():
        try:
            if isinstance(value, float):
                print(f'Converted {key}: {value} to {int(value)}')
            options[key] = int(value)
        except ValueError:
            continue  #Do nothing if the value is not an int

    return options

def options_validater(
                        options: Dict[int, Union[str, int]]
                        ) -> Dict[int, Union[str, int]]:
    """
    Checks if the options are valid
    Only checks, if the option is defined.

    Parameters:
    options (Dict[int, str]): A dictionary of options.

    Returns:
    bool: Returns options. If invalid, the option is set to None.
    """
    for option in ["ini_woods", "ini_fires", "fire_spread_rate"]:
        if option in options:
            if (
                not isinstance(options.get(option), int) or 
                (0 > options.get(option) or options.get(option) > 100)
                ):
                print(f'Wrong value for {option}: {options.get(option)}')
                print(f'Please reasign in basic config.')
                options[option] = None #Reset, so user must pick in basic config
    

    for option in ["iter_num", "growth_rate", "burn_rate"]:
        if option in options:
            if not isinstance(options.get(option), int) or options.get(option) <= 0:
                print(f'Value for {option}, must be positive')
                print(f'Please reasign or use default')
                options[option] = None

    if "gen_method" in options and options.get("gen_method") not in ["read", "random"]:
        print(f'Wrong value for gen_method: {options.get("gen_method")}')
        print(f'Please reasign in basic config.')
        options["gen_method"] = None
    

    if "firefighter_level" in options:
        if (
            not isinstance(options.get("firefighter_level"), int) or not
            0 < options.get("firefighter_level") < 4
            ):
            print(f'Wrong value for firefighter_level: {options.get("firefighter_level")}')
            print(f'Please reasign in basic config.')
            options["firefighter_level"] = None
    

    if "firefighter_num" in options and isinstance(options.get("firefighter_num"), str):
        try:
            num = options.get("firefighter_num")
            num = num.split("%")[0]
            num = int(num)
            print(f'num: {num}')
            if num < 0:
                raise ValueError("Value for firefighter_num must be positive")
        except ValueError:
            print(f'Wrong value for firefighter_num: {options.get("firefighter_num")}')
            print(f'Please reasign in basic config.')
            options["firefighter_num"] = None

    else:
        if "firefighter_num" in options:
            if options.get("firefighter_num") < 0:
                print(f'Value for "firefighter_num must be positive')
                print(f'Please reasign in basic config.')
                options["firefighter_num"] = None

    if "new_forrest_probability" in options:
        if not isinstance(options.get("new_forrest_probability"), int) or not 0 <= options.get("new_forrest_probability") <= 10000:
            print(f'Wrong value for new_forrest_probability: {options.get("new_forrest_probability")}')
            print(f'Please reasign in basic config.')
            options["new_forrest_probability"] = None

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
        options["growth_rate"] = 10
    if "burn_rate" not in options:
        options["burn_rate"] = 20
    if "new_forrest_probability" not in options:
        options["new_forrest_probability"] = 100
    if "fire_spread_rate" not in options:
        options["fire_spread_rate"] = 30


    return options