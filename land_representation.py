# land_representation.py
class GraphInfo: 
    def __init__(self):
        self.patches = {}
        self.neighbour_register= {}
        self.color_map = {}
        self.firefighters = {}
        
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
            
            res = []
            for neighbour in neighbours:
                res.append(self.patches.get(neighbour))

            self.neighbour_register[node] = res

        return self.neighbour_register

    def initialise_land_patches(self, patches):
        self.patches = patches

        return self.patches

    def initialise_color_map(self, patches):
        for id in patches:
            if patches.get(id).healthstat == None:   #If patch is stone, we set nothing
                continue
            self.color_map[id] = patches.get(id).healthstat

        return self.color_map


    def get_neighbours(self, patch_id):
        return self.neighbour_patches.get(patch_id)

    def update_patch_color(self, patch):
        if patch.healthstat == None:
            self.color_map.pop(patch.patch_id) #If patch is stone, we it from the color_map dict
        else:
            self.color_map[patch.patch_id] = patch.healthstat

class LandPatch:
    def __init__(self, patch_id, healthstat, position):
        self.patch_id = patch_id  # Identifies the LandPatch
        self.position = position # Identifies the position of the LandPatch
        self.healthstat = healthstat  # Variable identifying its health status

    def __eq__(self, other: object) -> bool:
        return self.patch_id == other.patch_id

    def __repr__(self):
        #graph_info = GraphInfo()
        #neighbour_patches = graph_info.get_neighbours(self.patch_id)
        #print("neighbour_patches = ", neighbour_patches)
        #str_neighbour_patches = ""
        #for patch in neighbour_patches:
        #    str_neighbour_patches += f'{patch.patch_id}'
        
        return f"LandPatch {self.patch_id} with healthstat {self.healthstat}"

class RockPatch(LandPatch):
    def __repr__(self):
        return f"RockPatch {self.patch_id}"
    
    def mutate(self):
        self.healthstat = None

class TreePatch(LandPatch):
    def __repr__(self):
        if self.healthstat > 0:
            return f"TreePatch {self.patch_id} with healthstat {self.healthstat}"
        else:
            return f"FirePatch {self.patch_id} with healthstat {self.healthstat}"
    
        

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