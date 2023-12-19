from abc import abstractmethod
import random
# land_representation.py

def wrap(obj):
    return [obj]

def unwrap(obj):
    return obj[0]

class GraphInfo: 
    def __init__(self, edges, options, patches):
        self.edges = edges
        self.options = options
        self.patches = self._patch_wrapper(patches) #Dict of patch ids and their wrapped objects
        print(f'patches = {self.patches}')
        self._color_map = self._initialise_color_map(patches) #Dict of patch ids and their color
        self.firefighters = self._initialise_firefighters() #Dict of firefighter ids and their objects
        print(self.options)
        self._initialise_neighbours()

    def _patch_wrapper(self, patches):
        print(f'patches = {patches}')
        return {patch.patch_id: wrap(patch) for patch in list(patches.values())}

    def _initialise_neighbours(self):
        all_nodes = set.union(*[set(edge) for edge in self.edges]) #Merges a new set of nodes
        edges = [set(edge) for edge in self.edges]
        patches = self.get_patches()

        for node in all_nodes:
            vertex_value_set = {node}
            neighbours = []
            for edge in edges:
                if vertex_value_set.intersection(edge):
                    #Here its important we account for self-loops. is it?
                    if len(edge) == 1:
                        neighbours.append(node)
                        continue #if we dont continue we get KeyError, since there is no differnce
                    
                    #If no selfloop we can check difference:
                    neighbours.append(edge.difference(vertex_value_set).pop())
            
            res = []
            for neighbour in neighbours:
                res.append(self.patches.get(neighbour))

            patches.get(node).initiate_neighbours(res)

    def get_patches(self):
        return {unwrap(patch).patch_id: unwrap(patch) for patch in list(self.patches.values())}

    def get_patch(self, patch_id):
        return unwrap(self.patches.get(patch_id))
    
    def get_wrapped(self,patch_id):
        return self.patches.get(patch_id)

    def _initialise_color_map(self, patches):
        self._color_map = {}
        for patch in patches.values():
            self._color_map[patch.patch_id] = patch.get_color()

        return self._color_map
    
    def _initialise_firefighters(self):
        res = {}
        for i in range(1, self.options.get("firefighter_num") + 1):
            random_patch = random.choice(self.patches)
            random_neighbours = unwrap(random_patch).get_neighbours()
            level = self.options.get("firefighter_level")
            new_fire_fighter = Firefighter(i, level, random_patch)
            new_fire_fighter.position = random_patch  #already wrapped object.
            res[i] = new_fire_fighter   #Instances of fire
        
        print(f'firefighters = {res}')
        return res
    
    def update_color_map(self):
        patches = self.get_patches()
        for patch in patches.values():
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
        for fighter in list(self.firefighters.values()):
            res.append(unwrap(fighter.position).patch_id)
        
        return res

class LandPatch:
    def __init__(self, patch_id, treestat, neighbors, burning):
        self.patch_id = patch_id  # Identifies the LandPatch
        self.treestat = treestat  # Variable identifying its health status
        self.burning = burning
        self._neighbours = neighbors  # List of neighbouring LandPatches
        self.firefighters = {}
  # Variable identifying its color

    def __eq__(self, other: object) -> bool:
        return self.patch_id == other.patch_id

    def __repr__(self):
        return f'LandPatch {self.patch_id} with neighbours {self.get_neighbour_id()}'
    
    def get_id(self):
        return self.patch_id
    
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
        return f"RockPatch {self.patch_id}"

    def get_color(self):
        return self._color
    
    def mutate(self, wrapped_self):
        new_patch = TreePatch(self.patch_id, 40, self.get_neighbours())
        wrapped_self[0] = new_patch

        return wrapped_self

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
        return f'Treepatch {self.patch_id}'
        
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
        
    def grow_or_burn(self, wrapped_self):
        if self.burning:
            self.treestat -= self.burnrate
            self.update_color()
            if self.treestat <= 0:
                print(f'Tree {self.patch_id} burned down')
                self.mutate(wrapped_self)
        else:
            self.treestat += self.growthrate
            self.update_color()
            if self.treestat > 256:
                self.treestat = 256

    def modify_treestat(self, amount, wrapped_self) -> LandPatch:
        if self.treestat >= 256:
                self.treestat = 256
                return self

        self.treestat += amount
        if self.treestat >= 0:
            return self.mutate(wrapped_self)
        
        self.update_color()

        return self

    def mutate(self, wrapped_self) -> RockPatch:
        new_patch = RockPatch(self.patch_id, 0, self.get_neighbours())
        wrapped_self[0] = new_patch
        return wrapped_self
    
class Firefighter:
    def __init__(self, id, skill_level, position):
        self.id = id
        self.skill_level = skill_level  # Variable identifying its skill in extinguishing fires
        self.position = position  # Identifies the Firefighter's position patch id

    def __repr__(self) -> str:
        return f"Firefighter {self.id} at {self.position}"
    
    def get_position(self):
        return unwrap(self.position)
    
    def get_neighbours_wrapped(self):
        return unwrap(self.position).get_neighbours()

    def move(self):
        position = self.get_position()
        if position.burning:
            print(f'Firefighter is standing still at {self.position}')
            return None #If firefighter is at fire, he will not move.

        move_pool = []
        neighbours = self.get_neighbours_wrapped()
        for neighbour in neighbours:
            if unwrap(neighbour).burning:
                move_pool.append(neighbour)

        if not move_pool: #if no fire
            move_pool = neighbours

        new_position = random.choice(move_pool)
        print(f'new position for firefighter {self.id} is {new_position}')
        self.neighbours = unwrap(new_position).get_neighbours()
        self.position = new_position

    def extinguish_fire(self):
        position = self.get_position()
        if not position.burning:
            return None #if no fire we do nothing
        
        else:
            pass

