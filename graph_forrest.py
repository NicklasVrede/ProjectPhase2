import visualiser_random_forest_graph
import graph_helper
import random
from land_representation import GraphInfo, TreePatch, RockPatch, Firefighter
from simulation import Simulation
import time
import matplotlib.pyplot as plt

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
    positions = {}
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
                    positions = generate_positions(edges)
                except ValueError:
                    print(f'Ignoring line, invalid value, with input: "{line.strip()}"')
            if len(parts) > 2 or len(parts) < 2:
                print(f'Ignoring invalid line, cannot form edgde with input: "{line.strip()}"')

    return edges, positions

def generate_positions(edges): 
    """
    Generates Voronoi data (coordinate map) from a given set of edges.

    Parameters:
    ----------
    edges: List[(int, int)]
        List containing the edges (Tuples of 2 vertices) forming the 2D surface.

    Returns:
    ----------
    positions: Dict[int: (float, float)]
        Dictionary containing the coordinate of each vertex (expressed as a tuple of float in [0,1]x[0,1]).
    """
    vertices = set([vertex for edge in edges for vertex in edge])
    positions = {vertex: tuple(random.rand(2)) for vertex in vertices}
    return positions

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

    return initiatlize_patches(edges, positions, options)

def initiatlize_patches(edges, positions, options):
    #check if the graph is planar?
    #check if the graph is connected?

    #Positions:
    all_vertices = list(set.union(*[set(edge) for edge in edges])) #Merges a new set of nodes

    #Initialize land patches:
    patches = {}
    wood_ratio = options.get("ini_woods") * 0.01
    fire_ratio = options.get("ini_fires") * 0.01

    wood_nodes = random.sample(all_vertices, int(wood_ratio*len(all_vertices)))
    rock_nodes = list(set(all_vertices).difference(wood_nodes))
    num_fires = int(len(wood_nodes) * fire_ratio)  #Percentage of fire nodes
    fire_nodes = random.sample(wood_nodes, num_fires)
    wood_nodes = list(set(wood_nodes).difference(fire_nodes))

    #Create patches
    patches = {}
    for i in wood_nodes:
        patches[i] = TreePatch(i, 100)
    for i in rock_nodes:
        patches[i] = RockPatch(i, 0)
    for i in fire_nodes:
        patches[i] = TreePatch(i, 100, burning=True)
  
    graph_info = GraphInfo(edges, options, patches)


    
    return initiate_simulation(edges, positions, options, graph_info)

def initiate_simulation(edges, positions, options, graph_info):
    #initialize graph object:
    graph_object = visualiser_random_forest_graph.Visualiser(edges,Colour_map=graph_info.get_color_map(), pos_nodes=positions,node_size=300, vis_labels=True)
    graph_object.update_node_edges(graph_info.get_firefighter_positions())  #Update initial fire fighters positions

    
    #Initialize simulation:
    #Scale wait time with number of iterations
    if options.get("iter_num") < 10:
        wait_time = 1
    elif options.get("iter_num") < 20:
        wait_time = 0.7
    elif options.get("iter_num") < 50:
        wait_time = 0.3
    elif options.get("iter_num") < 99:
        wait_time = 0.1
    elif options.get("iter_num") < 200:
        wait_time = 0.05
    elif options.get("iter_num") >= 200:
        wait_time = 0.01


    current_simulation = Simulation(graph_info, options)
    for _ in range(options.get("iter_num")):
        current_simulation.evolve() #Evolve the simulation
        graph_object.update_node_colours(graph_info.get_color_map()) #Update color map
        graph_object.update_node_edges(list(graph_info.get_firefighter_positions())) #Update fire fighters positions

        time.sleep(1)

    print("Simulation finished.")

    graph_object.wait_close()
    return None

def reporting(history, options):
    print("Reporting")
    iterations = list(history.keys())
    tree_populations = [history[i]["Tree_population"] for i in iterations]
    rock_populations = [history[i]["Rock_population"] for i in iterations]
    fire_populations = [history[i]["Fire_population"] for i in iterations]

    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, tree_populations, label='Tree Population')
    plt.plot(iterations, rock_populations, label='Rock Population')
    plt.plot(iterations, fire_populations, label='Fire Population')

    # Add details
    plt.xlabel('Iterations')
    plt.ylabel('Population')
    plt.title('Population over Iterations')
    plt.legend()

    # Show plot
    plt.show()


if __name__ == "__main__":
    options = {"gen_method" : "random",
               "ini_woods" : 80,
               "firefighter_num" : 2,
               "firefighter_level" : "low",
               "ini_fires" : 50,
               "iter_num" : 6,
               "treegrowth" : 10,
               "firegrowth" : 20,
               "newforrest" : 100 #50 permille / 0.5 %
               }
    generate_edges(options)


