# land_representation.py
class GraphInfo():
    def __new__(cls):
        cls.instance = super(GraphInfo, cls).__new__(cls)
        return cls.instance
        
    def __init__(self):
        self.neighbours = {}
        self.patches = set()
        self.color_map = {}
        
    def initialise_neighbour_register(self, edges):
        all_nodes = set.union(*[set(edge) for edge in edges]) #Merges a new set of nodes
        edges = [set(edge) for edge in edges]
       

        for node in all_nodes:
            vertex_value_set = {node}
            neighbours = []
            for edge in edges:
                if vertex_value_set.intersection(edge):
                    #Here its important we account for self-loops.
                    if len(edge) == 1:
                        neighbours.append(node)
                        continue #if we dont continue we get KeyError, since there is no differnce
                    
                    #If no selfloop we can check difference:
                    neighbours.append(edge.difference(vertex_value_set).pop())
            self.neighbours[node] = neighbours

        # Store the result in the register

    def initialise_land_patches(self, patches):
        self.patches = patches


    def initialise_color_map(self, patches):
        for id in patches:
            if patches.get(id).healthstat == None:   #If patch is stone, we set nothing
                continue
            self.color_map[id] = patches.get(id).healthstat

    def update_patch_color(self, patch):
        if patch.healthstat == None:
            self.color_map.pop(patch.patch_id) #If patch is stone, we it from the color_map dict
        else:
            self.color_map[patch.patch_id] = patch.healthstat

class LandPatch:
    def __init__(self, patch_id, healthstat, position, neighbours):
        self.patch_id = patch_id  # Identifies the LandPatch
        self.position = position # Identifies the position of the LandPatch
        self.healthstat = healthstat  # Variable identifying its health status
        self.neighbours = neighbours # Set of neighbouring LandPatches

    def __eq__(self, other: object) -> bool:
        return self.patch_id == other.patch_id

    def __repr__(self):
        return f'{__class__.__name__}({self.patch_id}, {self.healthstat}, {self.position})'

    def get_neighbours(self):
        return self.neighbours

class RockPatch(LandPatch):
    def mutate(self):
        self.healthstat = None

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