import visualiser_random_forest_graph as vr
import graph_helper as gh
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
                
            except ValueError("Must be a whole number"):
                print("Input must be a number")

        
        edges, pos = gh.voronoi_to_edges(300)
        print(gh.edges_planar(edges))
        mvr=vr.Visualiser(edges,pos_nodes=pos,node_size=50)
        cmap= {i:random.randint(0,265) for i in random.sample(list(pos.keys()),int(0.8*len(pos)))}
        mvr.update_node_colours(cmap)
        nodes_edges=random.sample(list(pos.keys()),0)
        mvr.update_node_edges(nodes_edges)

        mvr.wait_close()








