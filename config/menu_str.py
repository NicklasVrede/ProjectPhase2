options = {} #defined to express f-strings in menu_strings
line =  "\n"*3 + "-" * 40 + "\n"*3


def change_setting(options):
    """
    Returns the change setting menu string
    """
    return line + f"""
Which option would you like to change?

1. Generation Method ({options.get("gen_method")})
2. Initial landscape pattern ({options.get("ini_woods")} %)
3. Initial amount of fires ({options.get("ini_fires")} %)
4. Firefighter number ({options.get("firefighter_num")})
5. Firefighter skill level ({options.get("firefighter_level")})
6. Iteration steps ({options.get("iter_num")})
7. All basic options. Restart the configuration.

Advanced options:
8. Set all advanced options.
9. Tree growth (+{options.get("growth_rate")})
10. Burn rate (-{options.get("burn_rate")})
11. New random forrest probability ({options.get("new_forrest_probability")/100} %)
12. Fire spread rate ({options.get("fire_spread_rate")} %)

Proceed:
13. Proceed with graph generation

"""

def config_final(options):
    """
    returns the final configuration menu string
    """
    return line + f"""
Current options:

Generation Method: {options.get("gen_method")}
Initial woods: {options.get("ini_woods")} %
Initial fires: {options.get("ini_fires")} %
Firefighter number: {options.get("firefighter_num")}
Firefighter skill level: {options.get("firefighter_level")}
Iteration steps: {options.get("iter_num")}

#Advanced options:
Tree growth: +{options.get("growth_rate")} treestat
burn rate: -{options.get("burn_rate")} treestat
New random forrest probability: {options.get("new_forrest_probability")/100} %
Fire spread rate: {options.get("fire_spread_rate")} %

How would you like to proceed?

1. Proceed with graph generation

2. Change a setting

"""

menu_strings = {
    "welcome" : line + """
Welcome to the Forest Fire Simulation Program!

In this simulation, you will explore the dynamic evolution of a population 
of automata in a simulated forest environment. The fate of the landscape 
is in your hands as you influence the simulation parameters.

Press [Enter] to start the configuration.
""",

    "read_options_from_file" : line + """
Would you like to read the options from a file?
Note: Please see the template file "options.txt" in the config folder.

1. Yes

2. No
""",

    "gen_method" : line + """
Please pick a generation method of the graph.

1. Read from file

d or r. Random
""",

    "ini_woods" : line + """
Choose an option for the initial landscape pattern:

1. All woods

2. All rocks

d. Default (80% percent of woods, 20% rock)

r. Random amount of woods (between 0% and 100 %)
""",

    "firefigter_num" : line + """
Choose the number or percentage of firefighters.
The percentage will be of the minimum number of patches.
(Can exceed the number of patches)
""",

    "ini_fires" : line + """
Enter the initial percentage of fires. (As a whole number)
d. Default (20% percent of woods)

r. Random number (between 0% and 100 %)
""",

    "firefigter_level" : line + """
Choose the average skill level firefighters:

1. Low (Low power, no intelligence)

2. Medium (High power, no intelligence)

3. High (High power, intelligent)
Can navigate to the nearest fire.

    """,

    "iter_num" : line + """
How many iteration steps would you like?
""",

    "change_setting" : change_setting,


    "config_final" : config_final,

#advanced options:
     "growth_rate" : line + """
Enter the growth rate of trees each iteration.
This rate is an fixed amount added to treestat (256 max) each iteration.

d. Default (10)

r. Random number (between 0 and 100)

""",


    "burn_rate" : line + """
Enter the fires burn rate each iteration.
If a patch is burning its treestat will be reduced by the burn rate each iteration.

d. Default (20)

r. Random number (between 0 and 100)

""",

    "new_forrest_probability" : line + """
Enter the probability of a new forrest each iteration.
This probability is a probability in permille, i.e. 100 = 1 %.

d. Default (100 (1 %))

r. Random number (between 0 and 1000 (0 - 10 %))

""",

    "fire_spread_rate" : line + """
Enter the probability of a fire spreading to a neighbouring patch each iteration.
This probability is in percent. 

d. Default (30 (30 %))

r. Random number (0 to 100 (0 - 100 %))

""",

    }

