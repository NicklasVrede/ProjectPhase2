import visualiser_random_forest_graph
import graph_helper
import random
from land_representation import GraphInfo, TreePatch, RockPatch
from simulation import Simulation

def read_edges_from_file(file_path:str) -> list[set]:
    """
    Read graph edges from a file and return a list of sets representing the edges.

    The file should contain lines representing edges, with each line
    containing two vertices separated by a comma. Lines starting with
    '#' are considered comments and are ignored. Invalid lines are also ignored.

    Parameters:
    - file_path (str): The path to the file containing graph edges.

    Returns:
    - edges (list[set]): A list of sets representing the edges of the graph.

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
                    edge = {int(parts[0].strip()), int(parts[1].strip())}  
                    edges.append(edge)
                except ValueError:
                    print(f'Ignoring line, invalid value, with input: "{line.strip()}"')
            if len(parts) > 2 or len(parts) < 2:
                print(f'Ignoring invalid line, cannot form edgde with input: "{line.strip()}"')

    return edges

def generate_edges(options):
    if options.get("gen_method") == "read":
        while True:
            try:
                user_input = input('Enter file path to read edges from or type "back": ')

                if user_input == "back":
                    from configuration import main
                    return main(options)
                
                edges = read_edges_from_file(user_input)
                positions = None

                if len(edges) == 0:
                    print("Could not generate edges from file, please try an other file.")
                    continue
            
            except FileNotFoundError:
                print("File not found. Please enter a valid file path.")

    elif options.get("gen_method") == "random":
        print("Specify the minimal number of sites for the graph.")
        while True:
            try:
                user_input = int(input("Enter a number: "))
                break
                
            except ValueError:
                print("Input must be a number")

        
        edges, positions = graph_helper.voronoi_to_edges(user_input)


    #check if the graph is planar?
    #check if the graph is connected?

    #Update neighbour register:
    graph_info = GraphInfo()
    graph_info.initialise_neighbour_register(edges)
    neighbour_register = graph_info.neighbours
    #print(f'neighbour_register = {neighbour_register}')
    

    #Positions:
    list_of_positions = (list(positions.keys()))  # We need this in order to pick random positions

    #Initialize land patches:
    patches = {}
    wood_ratio = options.get("ini_woods") * 0.01
    wood_nodes = random.sample(list(positions.keys()), int(wood_ratio*len(positions)))
    for i in wood_nodes:
        wood_patch = TreePatch(i, 100, positions.get(i), neighbour_register.get(i))
        patches[i] = wood_patch

    #Initialize fire patches:
    #Set the initial fires:
    num_fires = int(len(wood_nodes) * options.get("ini_fires") * 0.01)  #Percentage of fire nodes
    fire_nodes = random.sample(wood_nodes, num_fires)
    
    #Update fire nodes:   #we are replacing some exsisting wood nodes with fire nodes
    for i in fire_nodes:
        fire_patch = TreePatch(i, -100, positions.get(i), neighbour_register.get(i))
        patches[i] = fire_patch   #Reassign patch to fire_patch

    #Initialize rock patches:  
    rock_nodes = set(positions.keys()).difference(wood_nodes)
    for i in rock_nodes:
        rock_patch = RockPatch(i, None, positions.get(i), neighbour_register.get(i))
        patches[i] = rock_patch    

    #Set initial fire fighters:
    fire_fighter_position = random.sample(list(positions.keys()),options.get("firefighter_num"))  #Highlight firefighters! Check if greater than number og nodes!


    #Initialize graph info:
    graph_info = GraphInfo()
    graph_info.initialise_land_patches(patches)
    graph_info.initialise_color_map(patches)


    #initialize graph object:
    graph_object = visualiser_random_forest_graph.Visualiser(edges,Colour_map=graph_info.color_map, pos_nodes=positions,node_size=300, vis_labels=True)
    graph_object.update_node_edges(fire_fighter_position)  #Update initial fire fighters positions


    #print(f'Fire fighter position = {fire_fighter_position}')
    

    # graph_object.update_node_colours(cmap)  #use this to update colors
    # graph_object.update_node_edges(edges_labels) #use this to update "labels"?
     

    #print(f'Edges = {edges}')
    #print(f'positions = {positions}')
    #print(f'color_map = {color_map}')
    #print(f'list of positions = {list_of_positions}')   

    current_simulation = Simulation(graph_info, options)
    for i in range(options.get("iter_num")):
        current_simulation.evolve()

    graph_object.wait_close()




if __name__ == "__main__":
    options = {"gen_method" : "random",
               "ini_woods" : 100,
               "firefighter_num" : 5,
               "firefighter_level" : "low",
               "ini_fires" : 20,
               "iter_num" : 5,
               "treegrowth" : 10,
               "firegrowth" : 20,
               "newforrest" : 50 #50 permille / 0.5 %
               }
    generate_edges(options)


