from configuration import welcome
from initializer import generate_edges, initialize_patches, initialise_color_map, initialise_firefighters
import visualiser_random_forest_graph
from simulation import Simulation
import time

def main(options=dict()):
    if options is None or len(options) < 6:
        if options is None:
            return welcome()
        else:
            return welcome(options)
    
    edges, positions = generate_edges(options)

    #initialize patch objects:
    patches = initialize_patches(edges, positions, options)
    
    #initialize color map:
    color_map = initialise_color_map(patches)

    #initialize firefighter objects:
    firefighters = initialise_firefighters(patches, options)

    #initialize graph info object:
    graph_info = GraphInfo(edges, options, patches, color_map, firefighters)

    #initialize simulation:
    return initiate_simulation(edges, positions, options, graph_info)


class GraphInfo: 
    def __init__(self, edges, options, patches, color_map, firefighters):
        self.edges = edges #list of edges
        self.options = options #dict of options
        self.patches = patches #dict of patch ids and their objects. Has to be updated, when mutations happens
        self.neighbour_id_register = self._initialise_neighbours() #dict of patch ids and their neighbour ids. Once initialise it remiains constant.
        self.neighbour_register = {} #Not used yet.
        self.color_map =  color_map
        self.firefighters =  firefighters
        self._initialise_link_to_patches()

    def _initialise_link_to_patches(self):
        for patch in list(self.patches.values()): # list() is actually not needed, since we dont need indexes.
            patch.graph_info = self

    def update_patch(self, patch:object):
        self.patches[patch.patch_id] = patch

    def get_color_map(self):
        return self.color_map
    
    def get_patches(self):
        return self.patches
        
    def get_firefighter_positions(self):
        res = []
        for fighter in list(self.firefighters.values()):
            res.append(fighter.position)
        
        return res

        #return [firefighter.position.patch_id for firefighter in list(self.firefighters.values())]


def initiate_simulation(edges, positions, options, graph_info):
    #initialize graph object:
    graph_object = visualiser_random_forest_graph.Visualiser(edges,Colour_map=graph_info.get_color_map(), pos_nodes=positions,node_size=300, vis_labels=True)
    graph_object.update_node_edges(graph_info.get_firefighter_positions())  #Update initial fire fighters positions

    
    #Initialize simulation:
    current_simulation = Simulation(graph_info, options)
    for _ in range(options.get("iter_num")):
        current_simulation.evolve() #Evolve the simulation
        graph_object.update_node_colours(graph_info.get_color_map()) #Update color map
        graph_object.update_node_edges(list(graph_info.get_firefighter_positions())) #Update fire fighters positions

        time.sleep(1)

    print("Simulation finished.")

    graph_object.wait_close()
    return None


if __name__ == "__main__":
    options = {"gen_method" : "random",
               "ini_woods" : 80,
               "firefighter_num" : 1,
               "firefighter_level" : "high",
               "ini_fires" : 30,
               "iter_num" : 40,
               "treegrowth" : 10,
               "firegrowth" : 20,
               "newforrest" : 100 #50 permille / 0.5 %
               }
    main()