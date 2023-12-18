from abc import abstractmethod
import random

# land_representation.py
class GraphInfo: 
    def __init__(self, edges, patches):
        self.edges = edges
        self.patches = patches #Dict of patch ids and their objects
        self._color_map = self._initialise_color_map(patches) #Dict of patch ids and their color
        self.fighter_positions = {} #Dict of firefighter ids and their position
        self._initialise_neighbours()
        
    def _initialise_neighbours(self):
        all_nodes = set.union(*[set(edge) for edge in self.edges]) #Merges a new set of nodes
        edges = [set(edge) for edge in self.edges]

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

            self.patches.get(node).initiate_neighbours(res)

    def _initialise_color_map(self, patches):
        for id in patches:
            if patches.get(id).treestat == None:   #If patch is stone, we set nothing
                continue
            self._color_map[id] = patches.get(id).treestat

        return self.color_map
    
    def get_color_map(self):
        return self._color_map

class LandPatch:
    def __init__(self, patch_id, treestat, neighbors=None):
        self.patch_id = patch_id  # Identifies the LandPatch
        self.treestat = treestat  # Variable identifying its health status
        self.burning = False
        self._neighbours = neighbors  # List of neighbouring LandPatches
        self._color = self.get_color()

    def __eq__(self, other: object) -> bool:
        return self.patch_id == other.patch_id

    def __repr__(self):
        #graph_info = GraphInfo()
        #neighbour_patches = graph_info.get_neighbours(self.patch_id)
        #print("neighbour_patches = ", neighbour_patches)
        #str_neighbour_patches = ""
        #for patch in neighbour_patches:
        #    str_neighbour_patches += f'{patch.patch_id}'
        
        return f"LandPatch {self.patch_id} with treestat {self.treestat}"
    
    def initiate_neighbours(self, neighbours):
        self._neighbours = neighbours
    
    def get_neighbour_id(self):
        neighbour_ids = []
        for neighbour in self._neighbours:
            neighbour_ids.append(neighbour.patch_id)
        return self._neighbours_ids
    
    def get_neighbours(self):
        return self._neighbours
    
    def get_nhealth(self):
        neighbours_health = {}
        for neighbour in self._neighbours:
            neighbours_health[neighbour.patch_id] = neighbour.treestat
        return neighbours_health
    
    def get_color(self):
        return self._color
    
    @abstractmethod
    def update_color(self):
        raise NotImplementedError
    
    @abstractmethod
    def mutate(self):
        raise NotImplementedError

class RockPatch(LandPatch):
    def __init__(self, patch_id, treestat=0, forrest_prob=1, neighbours=None):
        super().__init__(patch_id, treestat, neighbours)
        self.forrest_prob = forrest_prob
        
    def __repr__(self):
        return f"RockPatch {self.patch_id}"
    
    def mutate(self):
        self = TreePatch(self.patch_id, 40, self.get_neighbours())
        return self
    
    def update_color(self):
        self._color = 0

class TreePatch(LandPatch):
    def __init__(self, patch_id, treestat=40):
        super().__init__(patch_id, treestat)
        self.growthrate = 10
        self.burnrate = 20
        self.buring = False

    def __repr__(self):
        if self.treestat > 0:
            return f"TreePatch {self.patch_id} with treestat {self.treestat}"
        
    def update_color(self):
        if self.burning:
            self._color = -self.treestat
        else:
            self._color = self.treestat
        
    def ignite(self):
        self.burning = True
        self.update_color()
    
    def grow_or_burn(self):
        if self.burning:
            self.treestat -= self.burnrate
            if self.treestat <= 0:
                self.mutate()
        else:
            self.treestat += self.growthrate
            if self.treestat > 256:
                self.treestat = 256

    def mutate(self):
        self = RockPatch(self.patch_id, 0, self.get_neighbours())

    

class Firefighter:
    def __init__(self, id, skill_level, postion, neighbours=None):
        self.id = id
        self.skill_level = skill_level  # Variable identifying its skill in extinguishing fires
        self.position = postion  # Identifies the Firefighter's current LandPatch
        self.neighbours = neighbours  # List of neighbouring LandPatches

    def move(self):
        if self.position.burning:
            return None #If firefighter is at fire, he will not move.

        move_pool = []
        for neighbour in self.neighbours:
            if neighbour.treestat and neighbour.burning:  #we check treestat first or we crash..
                move_pool.append(neighbour)

        if not move_pool: #if no fire
            move_pool = self.neighbours

        self.neighbours = new_position.neighbours
        new_position = random.choice(move_pool).patch_id   #id not object!
        self.position = new_position

    def extinguish_fire(self):
        if not self.position.burning:
            return None #if no fire we do nothing
        
        else:
            self.position.treestat -= 50  #flat amount, becuase that makes most sence

            if self.position.treestat < 0:
                self.position.mutate()
                print(f'Firefighter {self.id} extinguished fire at: {self.position.patch_id}')

