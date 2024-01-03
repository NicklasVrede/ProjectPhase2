from typing import List, Dict, Union
from config import config
from firefighter import Firefighter
from initialiser import generate_edges, initialise_patches, initialise_color_map, initialise_firefighters, initialise_neighbours
import visualiser_random_forest_graph
from simulation import Simulation
from reporting import reporting
from land_rep import TreePatch, RockPatch
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
    if options is None or len(options) < 10:
        if options is None:
            return config.welcome()
        else:
            return config.welcome(options)
    
    #2. Generate edges and positions - Initialiser.py:
    edges, positions = generate_edges(options)

    #3. Initialise patch objects - Initialiser.py:
    patches = initialise_patches(edges, positions, options)

    #4. Initialise neighbour register - Initialiser.py:
    neighbour_id_register = initialise_neighbours(edges)
    
    #5. Initialise color map - Initialiser.py:
    color_map = initialise_color_map(patches)

    #6. Initialise firefighter objects - Initialiser.py:
    firefighters = initialise_firefighters(patches, options)

    #7. Initialise graph info object - Graph_forrest.py:
    graph_info = GraphInfo(options, patches, color_map, firefighters, neighbour_id_register)
    
    #8. Initialise graph object - Visualiser_random_forest_graph.py:
    graph_object = visualiser_random_forest_graph.Visualiser(edges,Colour_map=graph_info.get_color_map(), pos_nodes=positions,node_size=200, vis_labels=True)
    graph_object.update_node_edges(graph_info.get_firefighter_positions())  #Update initial fire fighters positions


    #9. Initiate simulation - Simulation.py:
    promt_interval = 0
    sleep_time = 5 / options.get("iter_num") #Minor addition wait time to make the simulation more visible at low iterations
    current_simulation = Simulation(graph_info)

    for i in range(options.get("iter_num")):  #Move this to simulation.py?
        if promt_interval >= 1.3:
            promt_interval = 0
            print(f"Iteration {i+1} of {options.get('iter_num')}")

        current_simulation.evolve() #Evolve the simulation
        graph_object.update_node_colours(graph_info.get_color_map()) #Update color map
        graph_object.update_node_edges(list(graph_info.get_firefighter_positions())) #Update fire fighters positions
        
        promt_interval += sleep_time

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
        self._patches = patches #dict of patch ids and their objects. Has to be updated, when mutations happens
        self._neighbour_id_register = neighbour_id_register #dict of patch ids and their neighbour ids. Once initialise it remiains constant.
        self._color_map =  color_map
        self._firefighters =  firefighters
        self._initialise_links()

    def _initialise_links(self) -> None:
        """
        Initialises links between objects, and updates rates based on options
        """
        for patch in list(self._patches.values()): # list() is actually not needed, since we dont need indexes.
            patch._graph_info = self

        for firefighter in list(self._firefighters.values()):
            firefighter._graph_info = self

    def get_patch(self, patch_id: int) -> Union[TreePatch, RockPatch]:
        """
        Returns a patch object.
        """
        return self._patches[patch_id]

    def get_patches(self) -> Dict[int, Union[TreePatch, RockPatch]]:
        """
        Returns the patches dict.
        """
        return self._patches

    def update_patch(self, patch: Union[TreePatch, RockPatch]) -> None:
        """
        Updates a patch in the patches dict.
        Used when a patch mutates.
        """
        self._patches[patch.get_id()] = patch

    def get_neighbours_ids(self, patch_id: int) -> List[Union[TreePatch, RockPatch]]:
        """
        Returns a list of neighbouring patches objects.
        """
        return self._neighbour_id_register[patch_id]

    def update_color(self, patch_id: int, color: int) -> None:
        """
        Updates the color map.
        """
        self._color_map[patch_id] = color

    def remove_color(self, patch_id: int) -> None:
        """
        Removes a patch from the color map.
        """
        del self._color_map[patch_id]

    def get_color_map(self) -> Dict[int, int]:
        """
        Returns the color map.
        """
        return self._color_map
        
    def get_firefighter_positions(self) -> List[int]:
        """
        Returns a list of firefighter positions.
        """
        res = []
        for fighter in list(self._firefighters.values()):
            res.append(fighter.get_position())
        
        return res

        #return [firefighter.position.patch_id for firefighter in list(self.firefighters.values())] 
        
    def activate_firefighters(self) -> Dict[int, Firefighter]:
        """
        Returns the firefighters dict.
        """
        for fighter in list(self._firefighters.values()):
            fighter.move()


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