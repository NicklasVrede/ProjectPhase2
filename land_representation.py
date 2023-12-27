from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union
import random
# land_representation.py

class LandPatch:
    """
    Base class for patches, TreePatch and RockPatch.

    Attributes:
    patch_id (int): Identifies the LandPatch.
    treestat (int): Variable identifying its health status.
    burning (bool): Variable identifying if the patch is burning.
    graph_info (GraphInfo): Stores information about the graph.

    """
    def __init__(self, patch_id: int, treestat: int, burning: bool, graph_info = None):
        self.patch_id = patch_id
        self.treestat = treestat
        self.burning = burning 
        self.graph_info = graph_info

    def get_neighbours_ids(self) -> List[int]:
        """
        Return a list of IDs of neighbouring patches.
        """
        return self.graph_info.neighbour_id_register.get(self.patch_id)
    
    def get_neighbours(self) -> List[Union['TreePatch', 'RockPatch']]:
        """
        Return a list the neighbouring patches.
        """
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

class TreePatch(LandPatch):
    """
    Class for patches with trees.
    Inherits from LandPatch.

    Attributes:
    patch_id (int): Identifies the LandPatch.
    treestat (int): Variable identifying its health status.
    burning (bool): Variable identifying if the patch is burning.
    firestat (int): Variable identifying the fire status.
    graph_info (GraphInfo): Stores information about the graph.
    growthrate (int): Variable identifying the growth rate of the patch.
    burnrate (int): Variable identifying the burn rate of the patch.
    spread_rate (int): Variable identifying the spread rate of the patch.
    """
    def __init__(self, patch_id: int, treestat: int, burning: bool=False, graph_info=None):
        super().__init__(patch_id, treestat, burning, graph_info)

        if self.burning:
            self.firestat = 10
    
        if self.graph_info:
            self.update_color()
            self.growthrate = graph_info.options.get('growth_rate') #10 by default
            self.burnrate = graph_info.options.get('burn_rate') #10 by default
            self.spread_rate= graph_info.options.get('fire_spread_rate') #30 by default

    def __repr__(self) -> str:
        """
        Return a string representation of the TreePatch.
        """
        return f'Treepatch {self.patch_id}'
    
    def get_color(self) -> int:
        """
        Return a color for the TreePatch.
        """
        if self.burning:
            color = -int(self.firestat * 2.56)  #int is important. otherwise visualiser fucks up the color
            return color
        else:
            return self.treestat
    
    def update_color(self) -> None:
        """
        Updates the color of the patch in the color_map
        """
        self.graph_info.color_map[self.patch_id] = self.get_color()
        
    def ignite(self) -> None:
        """
        Ignites the patch.
        Changing the state of the patch.
        """
        self.burning = True
        self.firestat = 10
        self.update_color()

    def spread_fire(self) -> None:
        """
        Spread fire to neighbouring patches based on spread rate
        """
        if self.burning:
            neighbours = self.get_neighbours()
            for neighbour in neighbours:
                if not neighbour.burning and neighbour.treestat > 0:
                    if random.randint(0, 100) < self.spread_rate:  #30 by defualt
                        print(f'Fire spread from {self} to {neighbour}')
                        neighbour.ignite()

    def evolve_firestat(self) -> None:
        """
        Evolves the firestat of the patch.
        """
        self.firestat += int(self.firestat * 0.1 + 10)
        
        if self.firestat > 100:
            self.firestat = 100
            return
        
        if self.firestat < 0:
            self.burning = False
            print(f'Fire was extinguished at {self}, treestat = {self.treestat}')
        self.update_color()

    def evolve_treestat(self) -> None:
        """
        Evolves the treestat of the patch.
        """
        if self.burning:
            self.treestat -= self.burnrate
            if self.treestat < 0:
                self.mutate()

        else:
            self.treestat += self.growthrate
            if self.treestat >= 256:
                self.treestat = 256
            self.update_color()

    def spread_forrest(self) -> None:
        """
        Spreads forrest to neighbouring patches with variable probability based on treestat
        """
        neighbours = self.get_neighbours()
        for neighbour in neighbours:
            if isinstance(neighbour, RockPatch):
                probability = int(5 + 20 * (self.treestat / 256))   #variable probability 5-20%
                random_num = random.randint(0, 100)
                if random_num < probability:
                    neighbour.mutate()
    
    def evolve_tree(self) -> None:
        """
        Initiates the evolution of the patch.
        """
        if self.burning:
            self.evolve_firestat()
        
        self.evolve_treestat()
        self.spread_forrest()
        
    def mutate(self) -> 'RockPatch':
        """
        Mutates the patch into a RockPatch.
        """
        self.burning = False #for firefigthers functionallity, since they store target patches
        new_patch = RockPatch(self.patch_id, 0, graph_info=self.graph_info)
        self.graph_info.update_patch(new_patch)
        return new_patch
    
class RockPatch(LandPatch):
    """
    Class for stone patches.
    Inherits from LandPatch.

    Attributes:
    patch_id (int): Identifies the LandPatch.
    treestat (int): Variable identifying its health status.
    burning (bool): Variable identifying if the patch is burning.
    graph_info (GraphInfo): Stores information about the graph.
    """
    def __init__(self, patch_id: int, treestat: int, graph_info=None):
        super().__init__(patch_id, treestat, False, graph_info) #burning = False

        if self.graph_info:
            self._update_color()
        
    def __repr__(self) -> str:
        """
        Return a string representation of the RockPatch.
        """
        return f"RockPatch {self.patch_id}"
    
    def _update_color(self) -> None:
        """
        Removes the color from color_map.
        Note: This only run once, when the patch is created.
        """
        del self.graph_info.color_map[self.patch_id]
    
    def get_color(self) -> None:
        """
        Raises a ValueError, since RockPatch has no value in color_map.
        """
        raise ValueError('RockPatch has no color')
    
    def spread_fire(self) -> None:
        """
        Raises a ValueError, since RockPatch cannot spread fire.
        """
        raise ValueError('RockPatch cannot spread fire')
    
    def random_forrest(self) -> TreePatch:
        """
        Calculates probability of new forrest and mutates the patch if the probability is met.
        """
        probability = self.graph_info.options.get("new_forrest_probability")  #move to self?
        random_num = random.randint(0, 10000)  #Making the probability act as permille.
        if random_num < probability:  #Newforrest
            print(f'Random forrest appeared at {self}!') #For testing
            self.mutate()
    
    def mutate(self) -> 'TreePatch':
        """
        Mutates the patch into a TreePatch or RockPatch.
        """
        new_patch = TreePatch(self.patch_id, 40, graph_info=self.graph_info)
        self.graph_info.update_patch(new_patch)

        return new_patch
        
