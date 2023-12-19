from abc import abstractmethod
import random

# land_representation.py
class GraphInfo: 
    def __init__(self, edges, patches):
        self.edges = edges
        self.patches = patches #Dict of patch ids and their objects
        self._color_map = self._initialise_color_map(patches) #Dict of patch ids and their color
        self.fighter_positions = {} #Dict of firefighter ids and their position
        self.firefighters = {} #Dict of firefighter ids and their objects
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
        self._color_map = {}
        for patch in patches.values():
            self._color_map[patch.patch_id] = patch.get_color()

        return self._color_map
    
    def update_color_map(self):
        for patch in self.patches.values():
            if patch.get_color() == 0:
                if patch.patch_id in self._color_map:    #important to check if key exists or we crash
                    del self._color_map[patch.patch_id]
                continue

            self._color_map[patch.patch_id] = patch.get_color()

        return self._color_map

    def pop_color_map(self, patch_id):
        self._color_map.pop(patch_id)
    
    def get_color_map(self):
        return self._color_map
    
    def get_firefighter_positions(self):
        res = []
        for fighter in self.firefighters.values():
            res.append(fighter.position.patch_id)
        
        return res

class LandPatch:
    def __init__(self, patch_id, treestat, burning, neighbors):
        self.patch_id = patch_id  # Identifies the LandPatch
        self.treestat = treestat  # Variable identifying its health status
        self.burning = burning
        self._neighbours = neighbors  # List of neighbouring LandPatches
  # Variable identifying its color

    def __eq__(self, other: object) -> bool:
        return self.patch_id == other.patch_id

    def __repr__(self):
        return f'LandPatch {self.patch_id} with color {self._color}'
    
    def initiate_neighbours(self, neighbours):
        self._neighbours = neighbours
    
    def get_neighbour_id(self):
        neighbours_ids = []
        for neighbour in self._neighbours:
            neighbours_ids.append(neighbour.patch_id)
        return neighbours_ids
    
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
    def mutate(self):
        raise NotImplementedError

class RockPatch(LandPatch):
    def __init__(self, patch_id, treestat, neighbors=None, forrest_prob=1):
        super().__init__(patch_id, treestat, neighbors, False)
        self.burning = False
        self.forrest_prob = forrest_prob
        self._color = 0
        
    def __repr__(self):
        return f"RockPatch {self.patch_id} with color {self._color}"

    def get_color(self):
        return self._color
    
    def mutate(self):
        new_patch = TreePatch(self.patch_id, 40, self.get_neighbours())
        return new_patch

class TreePatch(LandPatch):
    def __init__(self, patch_id, treestat, neighbors=None, burning=False):
        super().__init__(patch_id, treestat, neighbors, burning)
        self.growthrate = 10
        self.burnrate = 20
        if burning:
            self._color = -self.treestat
        else:
            self._color = self.treestat

    def __repr__(self):
        return f'Treepatch {self.patch_id} with color, on fire = {self.burning}'
        
    def update_color(self):
        if self.burning:
            self._color = -self.treestat
        else:
            self._color = self.treestat
        
    def ignite(self):
        self.burning = True
        self.update_color()

    def spread_fire(self):
        if self.burning:
            neighbours = self._neighbours
            for neighbour in neighbours:
                if neighbour.burning == False and neighbour.treestat > 0:
                    probability = int(30)
                    random_num = random.randint(0, 100)
                    if random_num < probability:
                        neighbour.ignite()
                        print(f'Fire spread from {self.patch_id} to {neighbour.patch_id}')
        else: 
            raise ValueError('Tree is not burning')
        
    def grow_or_burn(self):
        if self.burning:
            self.treestat -= self.burnrate
            self.update_color()
            if self.treestat <= 0:
                print(f'Tree {self.patch_id} burned down')
                self.mutate()
        else:
            self.treestat += self.growthrate
            self.update_color()
            if self.treestat > 256:
                self.treestat = 256

    def modify_treestat(self, amount) -> LandPatch:
        if self.treestat >= 256:
                self.treestat = 256
                return self

        self.treestat += amount
        if self.treestat >= 0:
            return self.mutate()
        
        self.update_color()

        return self

    def mutate(self) -> RockPatch:
        print(f'Tree {self.patch_id} mutated to rock')
        new_patch = RockPatch(self.patch_id, 0, self.get_neighbours())
        return new_patch
    
class Firefighter:
    def __init__(self, id, skill_level, position, neighbours):
        self.id = id
        self.skill_level = skill_level  # Variable identifying its skill in extinguishing fires
        self.position = position  # Identifies the Firefighter's current LandPatch
        self.neighbours = neighbours  # List of neighbouring LandPatches

    def __repr__(self) -> str:
        return f"Firefighter {self.id} at {self.position}"

    def move(self):
        print(f'self.position.burning = {self.position.burning}')
        if self.position.burning:
            print(f'Firefighter is standing still at {self.position}')
            return None #If firefighter is at fire, he will not move.

        move_pool = []
        for neighbour in self.neighbours:
            if neighbour.treestat and neighbour.burning:  #we check treestat first or we crash..
                move_pool.append(neighbour)

        if not move_pool: #if no fire
            move_pool = self.neighbours

        new_position = random.choice(move_pool)
        self.neighbours = new_position.get_neighbours()
        self.position = new_position


    def extinguish_fire(self):
        if not self.position.burning:
            return None #if no fire we do nothing
        
        else:
            print(f'new position for firefighter {self.id} is {self.position}')

