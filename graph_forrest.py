from typing import List, Dict
from configuration import welcome
from initialiser import generate_edges, initialize_patches, initialise_color_map, initialise_firefighters, initialise_neighbours
import visualiser_random_forest_graph
from simulation import Simulation
from reporting import reporting
import time

def main(options: Dict[str, int] = dict()) -> None:
    """
    The main function of the program.

    Parameters:
    options (Dict[str, int]): A dictionary of options.

    Following steps are executed:
    1. Initiates the configuration. - options Dict[str, int]
    2. Generates edges and positions. - edges List[Tuple[int, int]], positions Dict[int, Tuple[float, float]
    3. Initialises patch objects. - patches Dict[int, Union[TreePatch, RockPatch]]
    4. Initialises neighbour register. - neighbour_id_register Dict[int, List[int]]
    5. Initialises color map. - color_map Dict[int, int]
    6. Initialises firefighter objects. - firefighters Dict[int, Firefighter]
    7. Initialises graph info object. - graph_info GraphInfo
    8. Initiates the graph object. - graph_object visualiser_random_forest_graph.Visualiser
    9. Initiates simulation. 
    10. Initiates reporting.
    """
    #1. initiate configuration - Configuration.py:
    if options is None or len(options) < 6:
        if options is None:
            return welcome()
        else:
            return welcome(options)
    
    #2. Generate edges and positions - Initialiser.py:
    edges, positions = generate_edges(options)

    #3. Initialise patch objects - Initialiser.py:
    patches = initialize_patches(edges, positions, options)

    #4. Initialise neighbour register - Initialiser.py:
    neighbour_id_register = initialise_neighbours(edges)
    
    #5. Initialise color map - Initialiser.py:
    color_map = initialise_color_map(patches)

    #6. Initialise firefighter objects - Initialiser.py:
    firefighters = initialise_firefighters(patches, options)

    #7. Initialise graph info object - Graph_forrest.py:
    graph_info = GraphInfo(options, patches, color_map, firefighters, neighbour_id_register)
    
    #8. Initialise graph object - Visualiser_random_forest_graph.py:
    graph_object = visualiser_random_forest_graph.Visualiser(edges,Colour_map=graph_info.get_color_map(), pos_nodes=positions,node_size=300, vis_labels=True)
    graph_object.update_node_edges(graph_info.get_firefighter_positions())  #Update initial fire fighters positions


    #9. Initiate simulation - Simulation.py:
    current_simulation = Simulation(graph_info)
    for _ in range(options.get("iter_num")):  #Move this to simulation.py?
        current_simulation.evolve() #Evolve the simulation
        graph_object.update_node_colours(graph_info.get_color_map()) #Update color map
        graph_object.update_node_edges(list(graph_info.get_firefighter_positions())) #Update fire fighters positions

        sleep_time = 10 / options.get("iter_num")
        time.sleep(sleep_time)

    print("Simulation finished.")

    #10. Initiate reporting - Reporting.py:
    reporting(current_simulation.get_history())
    
    return main()


class GraphInfo:
    """
    Stores information about the graph.

    Attributes:
    options (Dict[str, int]): A dictionary of options.
    patches (Dict[int, Union[TreePatch, RockPatch]]): A dictionary of patch objects.
    neighbour_id_register (Dict[int, List[int]]): A dictionary of patch IDs and their neighbour IDs.
    neighbour_register (Dict[int, List[Union[TreePatch, RockPatch]]]): A dictionary of patch IDs and their neighbours.
    color_map (Dict[int, int]): A dictionary of patch IDs and their colors.
    firefighters (Dict[int, Firefighter]): A dictionary of firefighters.

    Methods:
    _initialise_links: Initialises links between objects, and updates rates based on options.
    update_patch: Updates a patch in the patches dict.
    get_color_map: Returns the color map.
    get_patches: Returns the patches dict.
    get_firefighter_positions: Returns a list of firefighter positions.
    """
    def __init__(self, options, patches, color_map, firefighters, neighbour_id_register):
        self.options = options #dict of options
        self.patches = patches #dict of patch ids and their objects. Has to be updated, when mutations happens
        self.neighbour_id_register = neighbour_id_register #dict of patch ids and their neighbour ids. Once initialise it remiains constant.
        self.neighbour_register = {} #Not used yet.
        self.color_map =  color_map
        self.firefighters =  firefighters
        self._initialise_links()

    def _initialise_links(self):
        """
        Initialises links between objects, and updates rates based on options
        """
        for patch in list(self.patches.values()): # list() is actually not needed, since we dont need indexes.
            patch.graph_info = self

            if patch.treestat > 0:
                patch.growthrate = self.options.get('growth_rate')
                patch.burnrate = self.options.get('burn_rate')
                patch.spread_rate= self.options.get('fire_spread_rate')

        for firefighter in list(self.firefighters.values()):
            firefighter.graph_info = self

    def update_patch(self, patch:object):
        """
        Updates a patch in the patches dict.
        Used when a patch mutates.
        """
        self.patches[patch.patch_id] = patch

    def get_color_map(self):
        """
        Returns the color map.
        """
        return self.color_map
    
    def get_patches(self):
        """
        returns the patches dict.
        """
        return self.patches
        
    def get_firefighter_positions(self):
        """
        Returns a list of firefighter positions.
        """
        res = []
        for fighter in list(self.firefighters.values()):
            res.append(fighter.position)
        
        return res

        #return [firefighter.position.patch_id for firefighter in list(self.firefighters.values())]




#Run the program
if __name__ == "__main__":
    options = {"gen_method" : "random",
            "ini_woods" : 80, #Percentage of forrests in the graph, rest = rocks
            "firefighter_num" : 10, #Number of firefighters
            "firefighter_level" : 3, #low, medium, high
            "ini_fires" : 10, #Percentage of fires in forrests
            "iter_num" : 40, #Number of sumulation iterations
            "growth_rate" : 10, #Growth rate of trees
            "burn_rate" : 20, #Growth rate of fire
            "fire_spread_rate" : 30, #Probability of fire spreading
            "new_forrest_probability" : 100 #Probability of new forrest in permille ie. 50 = 0,5 %
            }
    main()