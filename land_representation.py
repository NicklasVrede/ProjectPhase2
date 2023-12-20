from abc import abstractmethod
import random
# land_representation.py


class GraphInfo: 
    def __init__(self, edges, options, patches):
        self.edges = edges #list of edges
        self.options = options #dict of options
        self.patches = patches #dict of patch ids and their objects. Has to be updated, when mutations happens
        self.neigbour_id_register = {} #dict of patch ids and their neighbour ids. Once initialise it remiains constant.
        self.neigbour_register = {} #Not used yet.
        self.color_map = self._initialise_color_map() #dict of patch ids and their color
        self.firefighters = self._initialise_firefighters() #dict of firefighter ids and their objects
        self._initialise_neighbours() #initialise neighbours
        self._initialise_observer()
    
    def _initialise_color_map(self):
        res = {}
        for patch in list(self.patches.values()):
            if isinstance(patch, RockPatch):
                continue
            else:
                res[patch.patch_id] = patch.get_color()
        
        return res
    
    def _initialise_firefighters(self):
        res = {}
        for i in range(1, self.options.get("firefighter_num") + 1):
            random_patch = random.choice(self.patches)
            level = self.options.get("firefighter_level")
            new_fire_fighter = Firefighter(i, level, random_patch.patch_id, self)
            res[i] = new_fire_fighter   #Instances of fire
        
        print(f'firefighters = {res}')
        return res
    
    def _initialise_neighbours(self):
        all_patches = set.union(*[set(edge) for edge in self.edges]) #Merges a new set of nodes
        edges = [set(edge) for edge in self.edges]
        patches = self.patches

        for i in all_patches:
            vertex_value_set = {i}
            neighbours = []
            for edge in edges:
                if vertex_value_set.intersection(edge):
                    #Here its important we account for self-loops. is it?
                    if len(edge) == 1:
                        neighbours.append(i)
                        continue #if we dont continue we get KeyError, since there is no differnce
                    
                    #If no selfloop we can check difference:
                    neighbours.append(edge.difference(vertex_value_set).pop())
            
            self.neigbour_id_register[i] = neighbours

        #add objects to neigbour_register?
    
    def _initialise_observer(self):
        for patch in list(self.patches.values()):
            patch.graph_info = self

    
    def update_color(self, patch:object, color=None):
        """
        """
        if isinstance(patch, RockPatch):
            if patch.patch_id in self.color_map:
                self.color_map.pop(patch.patch_id)
        
        else:
            self.color_map[patch.patch_id] = patch.get_color()

    def update_patch(self, patch:object):
        self.patches[patch.patch_id] = patch
        print(f'Updated patch {patch.patch_id} to {patch}')

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

class LandPatch:
    def __init__(self, patch_id, treestat, neighbors, burning, graph_info=None):
        self.patch_id = patch_id  # Identifies the LandPatch
        self.treestat = treestat  # Variable identifying its health status
        self.burning = burning
        self.firefighters = {}
        self.graph_info = graph_info
        
    def __repr__(self):
        return f'LandPatch {self.patch_id} with neighbours {self.get_neighbours_ids()}'
    
    def get_neighbours_ids(self):
        return self.graph_info.neigbour_id_register.get(self.patch_id)
    
    def get_neighbours(self):
        res = []
        neighbours_id = self.get_neighbours_ids()
        for i in neighbours_id:
            res.append(self.graph_info.patches.get(i))

        return res
    
    @abstractmethod
    def get_color(self):
        raise NotImplementedError
    
    @abstractmethod
    def update_color(self):
        raise NotImplementedError
    
    @abstractmethod
    def mutate(self):
        raise NotImplementedError

class RockPatch(LandPatch):
    def __init__(self, patch_id, treestat, neighbors=None, forrest_prob=1, graph_info=None):
        super().__init__(patch_id, treestat, neighbors, False, graph_info)
        self.forrest_prob = forrest_prob

        if self.graph_info:
            self.graph_info.update_color(self)
        
    def __repr__(self):
        return f"RockPatch {self.patch_id}"
    
    def get_color(self):
        raise ValueError('RockPatch has no color')
    
    def update_color(self):
        if self.patch_id in self.graph_info.color_map:
            self.graph_info.color_map.pop(self.patch_id)
    
    def mutate(self):
        new_patch = TreePatch(self.patch_id, 40, self.get_neighbours(), graph_info=self.graph_info)
        self.graph_info.update_patch(new_patch)

        return new_patch

class TreePatch(LandPatch):
    def __init__(self, patch_id, treestat, neighbors=None, burning=False, graph_info=None):
        super().__init__(patch_id, treestat, neighbors, burning, graph_info)
        self.growthrate = 10
        self.burnrate = 20
        self.spread_rate= 30

        if self.burning:
            self.fire_health = 10
            print(f'Patch {self.patch_id} is burning with health {self.fire_health}')
    
        if self.graph_info:
            self.graph_info.update_color(self)

    def __repr__(self):
        return f'Treepatch {self.patch_id}'
    
    def get_color(self):
        if self.burning:
            color = -int(self.fire_health *2.56)  #int is important. otherwise visualiser fucks up the color
            return color
        else:
            return self.treestat
    
    def update_color(self):
        self.graph_info.update_color(self, self.get_color())  #Update color in graphinfo
        
    def ignite(self):
        self.burning = True
        self.fire_health = 10
        self.update_color()

    def spread_fire(self):
        if self.burning:
            neighbours = self.get_neighbours()
            for neighbour in neighbours:
                if not neighbour.burning and neighbour.treestat > 0:
                    if random.randint(0, 100) < self.spread_rate:  #30 by defualt
                        neighbour.ignite()

    def modify_fire_health(self, amount):
        self.fire_health += amount
        print(f'new fire health = {self.fire_health}')
        if self.fire_health < 0:
            self.burning = False
            self.update_color()

    def burn_speed_calculator(self):
        value = int(self.fire_health * 1.6)
        return value
    
    def modify_treestat(self):
        if self.treestat >= 256:
            self.treestat = 256
            return

        else:
            self.treestat -= self.burnrate
            self.update_color()
            if self.treestat < 0:
                self.mutate()
    
    def grow_or_burn(self):
        if self.burning:
            self.modify_treestat()
            self.modify_fire_health(self.burn_speed_calculator())
            
        else:
            self.treestat += self.growthrate
            self.update_color()
            if self.treestat > 256:
                self.treestat = 256


    def mutate(self) -> RockPatch:
        new_patch = RockPatch(self.patch_id, 0, self.get_neighbours(), graph_info=self.graph_info)
        self.graph_info.update_patch(new_patch)
        return new_patch
    
class Firefighter:
    def __init__(self, id, skill_level, position, graph_info):
        self.id = id
        self.position = position  # Identifies the Firefighter's position patch id
        self.graph_info = graph_info
        self._initiate_stats(skill_level)

    def __repr__(self) -> str:
        return f"Firefighter {self.id} at {self.position}"
    
    def _initiate_stats(self, skill_level):
        if skill_level == "low":
            self.power = 20
        if skill_level == "medium":
            self.power = 40
        if skill_level == "high":
            self.power = 40
            self.brain = True
    
    def get_pos_object(self):
        return self.graph_info.patches.get(self.position)
    
    def get_neighbours_objects(self):
        neighbours_ids = self.get_pos_object().get_neighbours_ids() 
        
        res = []
        for i in neighbours_ids:
            res.append(self.graph_info.patches.get(i))
        
        return res

    def move(self):
        position = self.get_pos_object()
        if position.burning:
            print(f'Firefighter is standing still at {self.position}')
            return None #If firefighter is at fire, he will not move.

        move_pool = []
        neighbours = self.get_neighbours_objects()
        for neighbour in neighbours:
            if neighbour.burning:
                move_pool.append(neighbour)

        if not move_pool: #if no fire
            move_pool = neighbours

        new_position = random.choice(move_pool)
        print(f'new position for firefighter {self.id} is {new_position}')
        self.position = new_position.patch_id

    def extinguish_fire(self):
        if self.get_pos_object.burning:
            self.get_pos_object().modify_fire_health(-self.power)
            print(f'Firefighter {self.id} is fighting fire at {self.position}')
