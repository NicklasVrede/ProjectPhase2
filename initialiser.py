import random
from copy import copy
from typing import Dict, List, Tuple, Union
from land_rep import TreePatch, RockPatch
from firefighter import Firefighter
import networkx as nx
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
            user_input = input('Enter file path to read edges from or type "back": ')

            if user_input == "back":
                from graph_forrest import main
                return main(options)
            
            try:
                edges = read_edges("graphs/"+ user_input)
                positions = planar_positions(edges)

            except FileNotFoundError:
                try:
                    edges = read_edges(user_input)
                    positions = planar_positions(edges)

                except FileNotFoundError:
                    print("Could not find file, please try again.")
                    continue
                
                else:
                    print("Wrong input, please try again.")

            if len(edges) == 0:
                print("Could not generate edges from file, please try an other file.")
                continue

            if graph_helper.edges_planar(edges):
                if check_connections(edges):
                    break
                print("The graph is not connected, please try an other file.")
            else:
                print("The graph is not planar, please try an other file.")


    elif options.get("gen_method") == "random":
        print("Specify the minimal number of patches for the graph (Min. 4). Or type 'back' to go back.")
        while True:
            try:
                user_input = input('Enter a number, "r" (40-120), "d" (80) or "back": ')
                if user_input == "back":
                    from config.config import config_final
                    return config_final(options)
                
                if user_input == "r":
                    user_input = random.randint(40, 120)    
                    print(f'Minimum patches = {user_input}.')
                    break

                if user_input == "d":
                    user_input = 80
                    break
                
                user_input = int(user_input)
                if user_input >= 4:
                    break
                else:
                    print("Minimum number of sites must be greater than 3")
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
    empty_counter = 0
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
                if line.strip() == "":
                    if empty_counter is None:
                        empty_counter = 0
                    else:
                        empty_counter += 1
                    continue
                print(f'Ignoring invalid line, cannot form edgde with input: "{line.strip()}"')
    
    if empty_counter:
        print(f'Ignored {empty_counter} empty lines.')

    return edges

def check_connections(edges:List[tuple]) -> bool:
    """
    Check if a graph is connected.

    Parameters:
    - graph: The graph to check.

    Returns:
    - connected: True if the graph is connected, False otherwise.

    Examples:
    >>> get_connections([{1, 2}, {3, 4}])
    [{1, 2}, {3, 4}]

    >>> get_connections([{1, 2}, {2, 3}, {2,4}, {7}])
    [{1, 2, 3, 4}, {7}]
    """
    edge_connections = [set(edge) for edge in edges]
    
    def has_intersection(edges_connections: list[set]) -> bool:
        """
        Check if there is an intersection between any two sets in the list.

        Parameters:
        - edges_connections (list[set]): The list of sets to check for intersections.

        Returns:
        - bool: True if there is an intersection, False otherwise.

        Example:
        >>> has_intersection([{1, 2}, {3, 4}])
        False

        >>>has_intersection([{1, 2}, {2, 3}, {3, 4}]
        True
        """
        for a_set in edges_connections:
            for b_set in edges_connections:
                if a_set == b_set:
                    continue
                elif a_set.intersection(b_set):
                    return True
        return False

    while has_intersection(edge_connections):
        for a_set in edge_connections:
            for b_set in edge_connections:
                if a_set is b_set:
                    continue
                if a_set.intersection(b_set):
                    a_set.update(b_set)
                    edge_connections.remove(b_set)
                    break
    
    if len(edge_connections) > 1:
        return False
    else:
        return True
    
def planar_positions(edges: List[Tuple[int, int]]) -> Dict[int, Tuple[float, float]]:
    """
    Generates positions for a planar graph.

    Parameters:
    edges (List[Tuple[int, int]]): A list of edges.

    Returns:
    positions - Dict[int, Tuple[float, float]]: A dictionary of positions. Each key is a patch ID, and each value is a position.
    """
    graph = nx.Graph(edges)
    positions = nx.planar_layout(graph) #This makes it more pretty than spring_layout.
    #correcting datatype to adhere to visualiser module:
    #key: array([0.5, 0.5]) -> key: (0.5, 0.5)
    positions = {key: tuple(value) for key, value in positions.items()}


    return positions

def initialise_patches(edges: List[Tuple[int, int]], positions: Union[None, Dict[int, Tuple[float, float]]], options: Dict[str, int]) -> Dict[int, Union[TreePatch, RockPatch]]:
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
        all_nodes = list(set.union(*[set(edge) for edge in edges]))

    #Initialise ratio of woods and fires
    tree_ratio = options.get("ini_woods") * 0.01
    fire_ratio = options.get("ini_fires") * 0.01

    tree_nodes = random.sample(all_nodes, int(tree_ratio*len(all_nodes)))
    rock_nodes = list(set(all_nodes).difference(tree_nodes))
    num_fires = round(len(tree_nodes) * fire_ratio)
    fire_nodes = random.sample(tree_nodes, num_fires)
    tree_nodes = list(set(tree_nodes).difference(fire_nodes))


    #Initialise patches
    patches = {}
    for i in tree_nodes:
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
    neighbour_id_register - Dict[int, List[int]]: 
    A dictionary mapping each patch to a list of its neighbours.
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
    color_map - Dict[int, Tuple[int, int, int]]: A color map. 
    Each key is a patch ID, and each value is a color.
    """
    res = {}
    for patch in list(patches.values()):
        if patch.get_treestat() == 0:
            continue
        else:
            res[patch.get_id()] = patch.get_color()
    
    return res

def initialise_firefighters(patches, options) -> Dict[int, Firefighter]:
    """
    Initializes firefighters.

    Returns:
    firefighters - Dict[int, Firefighter]: A dictionary of firefighters. 
    Each key is a firefighter ID, and each value is a Firefighter object.
    """
    number = options.get("firefighter_num")
    if isinstance(number, str):
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



