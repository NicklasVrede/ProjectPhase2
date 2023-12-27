from abc import abstractmethod
from typing import Any, Dict, List, Optional, Union
import random
# land_representation.py

class LandPatch:
    def __init__(self, patch_id, treestat, burning, graph_info=None):
        self.patch_id = patch_id  # Identifies the LandPatch
        self.treestat = treestat  # Variable identifying its health status
        self.burning = burning
        self.firefighters = {}
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
    def __init__(self, patch_id, treestat, burning=False, graph_info=None):
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
        new_patch = RockPatch(self.patch_id, 0, self.get_neighbours(), graph_info=self.graph_info)
        self.graph_info.update_patch(new_patch)
        return new_patch
    
class RockPatch(LandPatch):
    def __init__(self, patch_id, treestat, forrest_prob=1, graph_info=None):
        super().__init__(patch_id, treestat, False, graph_info)
        self.forrest_prob = forrest_prob

        if self.graph_info:
            self.update_color()
        
    def __repr__(self) -> str:
        """
        Return a string representation of the RockPatch.
        """
        return f"RockPatch {self.patch_id}"
    
    def get_color(self) -> ValueError:
        """
        Returns a error, since RockPatch has no color.
        """
        return ValueError('RockPatch has no color')
    
    def update_color(self) -> None:
        """
        Removes the color from color_map.
        Note: This must only run once, when the patch is created.
        """
        del self.graph_info.color_map[self.patch_id]
    
    def mutate(self) -> Union['TreePatch', 'RockPatch']:
        """
        Mutates the patch into a TreePatch or RockPatch.
        """
        new_patch = TreePatch(self.patch_id, 40, self.get_neighbours, graph_info=self.graph_info)
        self.graph_info.update_patch(new_patch)

        return new_patch
        
