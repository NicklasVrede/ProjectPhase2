# land_representation.py
class GraphInfo():
    def __new__(cls):
        if not hasattr(cls, 'instance'):  #checks if instance exists
            cls.instance = super(graph_info, cls).__new__(cls)
            return cls.instance
        
    def __init__(self):
        self.neighbours = {}

    def initialise_neighbour_register(self, edges):
        """
        Generates the neighbour_register for a given vertex.
        
        Parameters:
        - vertex_value (int): The vertex for which to calculate neighbour_register.
        - edges (list): The graph represented as a list of sets.

        Returns:
        - list: The neighbour_register for the given vertex.

        """
        all_nodes = set.union(*[set(edge) for edge in edges]) #Merges a new set of nodes
        edges = [set(edge) for edge in edges]
       

        for node in all_nodes:
            print(f'Node = {node}')
            vertex_value_set = {node}
            print(f'vertex_value_set = {vertex_value_set}')
            neighbours = []
            for edge in edges:
                if vertex_value_set.intersection(edge):
                    #Here its important we account for self-loops.
                    if len(edge) == 1:
                        neighbours.append(vertex_value)
                        continue #if we dont continue we get KeyError, since there is no differnce
                    
                    #If no selfloop we can check difference:
                    neighbours.append(edge.difference(vertex_value_set).pop())
            self.neighbours[node] = neighbours
        # Store the result in the register
        

class LandPatch:
    def __init__(self, patch_id):
        self.patch_id = patch_id
        self.neighbors = set()

    def get_neighbors(self):
        graph_info

class RockPatch(LandPatch):
    def mutate(self):
        # Allow swapping this RockPatch with a Treepatch without losing connections
        pass

class TreePatch(LandPatch):
    def update_land(self):
        # Update the value of treestats due to fire or firefighter action
        pass

    def mutate(self):
        # Allow swapping this Treepatch with a Rockpatch without losing connections
        pass

class Firefighter:
    def __init__(self, skill_level):
        self.skill_level = skill_level  # Variable identifying its skill in extinguishing fires
        # Additional attributes as needed

    def move(self):
        # Define the logic for firefighter movement
        pass

    def extinguish_fire(self, patch):
        # Define the logic for extinguishing fire in a specific patch
        pass