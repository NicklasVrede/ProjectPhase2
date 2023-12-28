import random
from typing import Dict, List, Tuple, Union
from land_representation import TreePatch, RockPatch
from firefighter import Firefighter
import graph_helper

def generate_edges(options: Dict[str, Union[str, int]]) -> Tuple[List[Tuple[int, int]], Dict[int, Tuple[float, float]]]:
    """
    Generates edges and positions based on the provided options.

    Parameters:
    options (Dict[str, Union[str, int]]): A dictionary containing generation options. 
 
    Returns:
    edges - Tuple[List[Tuple[int, int]]: A tuple containing a list of edges and a dictionary of positions.
    positions - Dict[int, Tuple[float, float]]]: Each edge is a tuple of two integers, and each position is a tuple of two floats.
    """
    if options.get("gen_method") == "read":
        while True:
            try:
                user_input = input('Enter file path to read edges from or type "back": ')

                if user_input == "back":
                    from configuration import main
                    return main(options)
                
                edges = read_edges(user_input)
                positions = None

                if len(edges) == 0:
                    print("Could not generate edges from file, please try an other file.")
                    continue

                if graph_helper.edges_planar(edges):
                    break
                else:
                    print("The graph is not planar, please try an other file.")
            
            except FileNotFoundError:
                print("File not found. Please enter a valid file path.")

    elif options.get("gen_method") == "random":
        print("Specify the minimal number of sites for the graph (Min. 4). Or type 'back' to go back.")
        while True:
            try:
                user_input = input('Enter a number or "back": ')
                if user_input == "back":
                    from graph_forrest import main
                    return main(options)
                
                user_input = int(user_input)
                if user_input >= 4:
                    break
                else:
                    print("Minimum number of sites must be greater than 4")
                    continue
                
            except ValueError:
                print("Invalid input, please try again.")

        
        edges, positions = graph_helper.voronoi_to_edges(user_input)
    
    return edges, positions
    

def read_edges(file_path: str) -> List[Tuple[int, int]]:
    """
    Reads graph edges from a file.

    Parameters:
    file_path (str): The path to the file.

    Returns:
    edges - List[Tuple[int, int]]: A list of edges. Each edge is a tuple of two integers.
   """
    edges = []
    with open(file_path, 'r') as file: 
        for line in file:
            if line.strip().startswith("#"):
                continue

            # Split each line into two vertices using a comma.
            parts = line.strip().split(',')
            if len(parts) == 2:
                try:    #Compose edge, and check correct values.
                    edge = (int(parts[0].strip()), int(parts[1].strip()))
                    edges.append(edge)
                except ValueError:
                    print(f'Ignoring line, invalid value, with input: "{line.strip()}"')
            if len(parts) > 2 or len(parts) < 2:
                print(f'Ignoring invalid line, cannot form edgde with input: "{line.strip()}"')

    return edges

def initialize_patches(edges: List[Tuple[int, int]], positions: Union[None, Dict[int, Tuple[float, float]]], options: Dict[str, int]) -> Dict[int, Union[TreePatch, RockPatch]]:
    """
    Initializes patches based on the given edges, positions, and options.

    Parameters:
    edges (List[Tuple[int, int]]): A list of edges.
    positions (Dict[int, Tuple[float, float]]): A dictionary of positions.
    options (Dict[str, Union[str, int]]): A dictionary of options.

    Returns:
    patches - Dict[int, Union[TreePatch, RockPatch]]: A dictionary of patch objects.
    """
    if positions is not None:
        all_nodes = list(positions.keys()) #Merges a new set of nodes
    else:
        all_nodes = set.union(*[set(edge) for edge in edges])

    #Initialize ration of woods and fires
    wood_ratio = options.get("ini_woods") * 0.01
    fire_ratio = options.get("ini_fires") * 0.01

    wood_nodes = random.sample(all_nodes, int(wood_ratio*len(all_nodes)))
    rock_nodes = list(set(all_nodes).difference(wood_nodes))
    num_fires = round(len(wood_nodes) * fire_ratio)
    fire_nodes = random.sample(wood_nodes, num_fires)
    wood_nodes = list(set(wood_nodes).difference(fire_nodes))

    #Create patches
    patches = {}
    for i in wood_nodes:
        patches[i] = TreePatch(i, 100) #100 = treestat
    for i in rock_nodes:
        patches[i] = RockPatch(i, 0)
    for i in fire_nodes:
        patches[i] = TreePatch(i, 100, burning=True)
  
    return patches

def initialise_neighbours(edges) -> Dict[int, List[int]]:
    """
    Initializes neighbour_id_register based on the given edges.

    Returns:
    neighbour_id_register - Dict[int, List[int]]: A dictionary mapping each patch to a list of its neighbours.
    """
    all_patches = set.union(*[set(edge) for edge in edges]) #Merges a new set of nodes
    edges = [set(edge) for edge in edges]
    res = {}

    for i in all_patches:
        vertex_value_set = {i}
        neighbours = []
        for edge in edges:
            if vertex_value_set.intersection(edge): #There is no self loops, so we dont check.
                neighbours.append(edge.difference(vertex_value_set).pop())
        
        res[i] = neighbours

    return res

def initialise_color_map(patches: Dict[int, Union[TreePatch, RockPatch]]) -> Dict[int, int]:
    """
    Initializes a color map based on the given patches.

    Parameters:
    patches (Dict[int, Union[TreePatch, RockPatch]]): A dictionary of patches.

    Returns:
    color_map - Dict[int, Tuple[int, int, int]]: A color map. Each key is a patch ID, and each value is a color.
    """
    res = {}
    for patch in list(patches.values()):
        if patch.treestat == 0:
            continue
        else:
            res[patch.patch_id] = patch.get_color()
    
    return res

def initialise_firefighters(patches, options) -> Dict[int, Firefighter]:
    """
    Initializes firefighters.

    Returns:
    firefighters - Dict[int, Firefighter]: A dictionary of firefighters. Each key is a firefighter ID, and each value is a Firefighter object.
    """
    number = options.get("firefighter_num")
    if number.endswith("%"):
        number = int(number.split("%")[0]) #we split at % and calculate the final number:
        number = int(number * len(patches) * 0.01)
        print(f'Scaled the number of firefighters to {number} based on the number of patches and the firefighter percentage.')
    res = {}
    for i in range(number):
        random_id = random.choice(list(patches.keys()))
        level = options.get("firefighter_level")
        new_fire_fighter = Firefighter(i, level, random_id)
        res[i+1] = new_fire_fighter
    
    return res



