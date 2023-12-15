# land_representation.py
class graph_info():
    def __new__(cls):
        if not hasattr(cls, 'instance'):  #checks if instance exists
            cls.instance = super(graph_info, cls).__new__(cls)
            return cls.instance
        
    def __init__(self):
        neighbors = {}

class LandPatch:
    def __init__(self, patch_id):
        self.patch_id = patch_id
        self.neighbors = set()  # Set of neighboring patch_ids

    def get_neighbors(self):
        # Return the IDs of neighboring patches
        pass

class RockPatch(LandPatch):
    def mutate(self):
        # Allow swapping this RockPatch with a Treepatch without losing connections
        pass

class TreePatch(LandPatch):
    def __init__(self, patch_id, treestats):
        super().__init__(patch_id)
        self.treestats = treestats  # Identifies the health of the Treepatch [0-256]

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