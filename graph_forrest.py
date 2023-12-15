import visualiser_random_forest_graph
import graph_helper
import random
from land_representation import GraphInfo

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
    
    #Set initial land pattern:
    if options.get("ini_land_pattern") == "wood":
        wood_ratio = 0.8

    if options.get("ini_land_pattern") == "rock":
        wood_ratio = 0

    if options.get("ini_land_pattern") == "random":
        wood_ratio = random.random() #random float between 0-1

    #generate initial color map:
    list_of_positions = (list(positions.keys()))  # We need this in order to pick random
    #print(f'number of nodes = {number_of_nodes}')


    #Set wood nodes etc:
    wood_nodes = random.sample(list(positions.keys()), int(wood_ratio*len(positions)))
    color_map = {i:100 for i in wood_nodes}

    #Set the initial fires:
    num_fires = int(len(wood_nodes)*0.5)
    fire_nodes = random.sample(wood_nodes, num_fires)
    
    #Update fire nodes:
    for i in fire_nodes:
        color_map[i] = -100

    #print(f'num_fires = {num_fires}')
    #print(f'fire_nodes = {fire_nodes}')
    
    graph_object = visualiser_random_forest_graph.Visualiser(edges,Colour_map=color_map, pos_nodes=positions,node_size=300, vis_labels=True)
    graph_object._replot()


    fire_fighter_position = random.sample(list(positions.keys()),options.get("firefighter_num"))  #Highlight firefighters! Check if greater than number og nodes!
    graph_object.update_node_edges(fire_fighter_position)
    #print(f'Fire fighter position = {fire_fighter_position}')
    

    # graph_object.update_node_colours(cmap)  #use this to update colors
    # graph_object.update_node_edges(edges_labels) #use this to update "labels"?
    

    print(f'Edges = {edges}')
    #print(f'positions = {positions}')
    #print(f'color_map = {color_map}')
    #print(f'list of positions = {list_of_positions}')   

    info = GraphInfo()
    info.initialise_neighbour_register(edges)

    print(f'Neighbours register = {info.neighbours}')


    graph_object.wait_close()




if __name__ == "__main__":
    options = {"gen_method" : "random",
               "ini_land_pattern" : "wood",
               "firefighter_num" : 5,
               "firefighter_level" : "low",
               "iter_num" : 5
               }
    generate_edges(options)


