import visualiser_random_forest_graph
import graph_helper
import random

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
                user_input = input('Enter file path or "back" to start over: ')

                if user_input == "back":
                    from configuration import main
                    return main(options)
                
                edges = read_edges_from_file(user_input)

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

        while not graph_helper.edges_planar(edges):  #Potential endless loop?
            print("Edges not planar, trying agian..")
            edges, positions = graph_helper.voronoi_to_edges(user_input)

        color_map = {i:random.randint(0,265) for i in random.sample(list(positions.keys()),int(0.8*len(positions)))}   #Notice 0.8 ratio 
        graph_object = visualiser_random_forest_graph.Visualiser(edges,Colour_map=color_map, pos_nodes=positions,node_size=200, vis_labels=True)
        graph_object._replot()

        #Fire_fighter_position = random.sample(list(positions.keys()),options.get("firefighter_num"))  #Highlight firefighters! Check if greater than number og nodes!
        #graph_object.update_node_edges(Fire_fighter_position)
        

        # graph_object.update_node_colours(cmap)  #use this to update colors
        # graph_object.update_node_edges(edges_labels) #use this to update "labels"?
        

        print(f'Edges = {edges}')
        print(f'pos = {positions}')
        print(f'color_map = {color_map}')
        

        graph_object.wait_close()


if __name__ == "__main__":
    options = {"gen_method" : "random",
               "ini_land_pattern" : "wood",
               "firefighter_num" : 5,
               "firefighter_level" : "low",
               "iter_num" : 5
               }
    generate_edges(options)






