from abc import abstractmethod, ABC
from typing import List, Union
import random
# land_representation.py


class LandPatch(ABC):
    """
    Base class for patches, TreePatch and RockPatch.

    Attributes:
    patch_id (int): Identifies the LandPatch.
    treestat (int): Variable identifying its health status.
    burning (bool): Variable identifying if the patch is burning.
    graph_info (GraphInfo): Stores information about the graph.

    Methods:
    get_id: Returns the ID of the patch.
    is_burning: Returns True if the patch is burning.
    get_treestat: Returns the treestat of the patch.
    get_neighbours_ids: Returns a list of IDs of neighbouring patches.
    get_neighbours: Returns a list the neighbouring patches objects.
    """
    def __init__(
            self, patch_id: int, treestat: int, 
            burning: bool, graph_info = None
            ):
        self._patch_id = patch_id
        self._treestat = treestat
        self._burning = burning 
        self._graph_info = graph_info

    def get_id(self) -> int: #Used by firefighter, simulation and graph_info
        """
        Return the ID of the patch.
        """
        return self._patch_id
    
    def is_burning(self) -> bool: #Used by firefighter and simulation
        """
        Return True if the patch is burning.
        """
        return self._burning
    
    def get_treestat(self) -> int: #Used by simulation
        """
        Return the treestat of the patch.
        """
        return self._treestat

    def get_neighbours_ids(self) -> List[int]: 
        """
        Return a list of IDs of neighbouring patches.
        """
        return self._graph_info.get_neighbours_ids(self.get_id())
    
    def get_neighbours(self) -> List[Union['TreePatch', 'RockPatch']]: #used by firefighters
        """
        Return a list the neighbouring patches objects.
        """
        res = []
        neighbours_id = self.get_neighbours_ids()
        for i in neighbours_id:
            res.append(self._graph_info.get_patch(i))

        return res
    
    @abstractmethod
    def _update_color(self):
        raise NotImplementedError
    
    @abstractmethod
    def _mutate(self):
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

    Methods:
    get_color: Returns a color for the TreePatch.
    reduce_firestat: Reduces the firestat of the patch.
    updateland: Initiates the evolution of the patch.
    """
    def __init__(
            self, patch_id: int, treestat: int, 
            burning: bool=False, graph_info=None
            ):
        super().__init__(patch_id, treestat, burning, graph_info)

        if self._burning:
            self._firestat = 10
    
        if self._graph_info:
            self._update_color()

    def __repr__(self) -> str:
        """
        Return a string representation of the TreePatch.
        """
        return f'Treepatch {self._patch_id}'
    
    def get_color(self) -> int: #Used when initializing color_map
        """
        Return a color for the TreePatch.
        """
        if self.is_burning():
            color = -int(self._firestat * 2.56)  #int is important. Otherwise visualiser fucks up the color
            return color
        else:
            return self._treestat
        
    def _update_color(self) -> None:
        """
        Updates the color of the patch in the color_map
        """
        self._graph_info.update_color(self._patch_id, self.get_color())

    def reduce_firestat(self, amount): #used by firefighter
        """
        reduces firestat
        """
        assert amount > 0
        self._firestat += -amount
        if self._firestat < 0:
            self._burning = False
            self._update_color()
        
    def _ignite(self) -> None:
        """
        Ignites the patch.
        Changing the state of the patch.
        """
        self._burning = True
        self._firestat = 10
        self._update_color()

    def _spread_fire(self) -> None:
        """
        Spread fire to neighbouring patches based on spread rate
        """
        if self._burning:
            neighbours = self.get_neighbours()
            for neighbour in neighbours:
                if not neighbour._burning and neighbour._treestat > 0:
                    if random.randint(1, 100) < self._graph_info.options.get("fire_spread_rate"):  #30 by defualt
                        neighbour._ignite()

    def _evolve_firestat(self) -> None:
        """
        Evolves the firestat of the patch.
        """
        self._firestat += self._firestat * 0.1 + 10 #10 base rate + 0.1 * firestat

        if self._firestat > 100:
            self._firestat = 100
        else:
            self._update_color()

    def _evolve_treestat(self) -> None: 
        """
        Evolves the treestat of the patch.
        """
        if self._burning:
            self._treestat -= self._graph_info.options.get("burn_rate") #20 by default
            if self._treestat <= 0:
                self._mutate()
            else:
                self._spread_fire()

        else:
            self._treestat += self._graph_info.options.get("growth_rate") #10 by default
            if self._treestat >= 256:
                self._treestat = 256
            self._update_color()

    def _spread_forrest(self) -> None:
        """
        Spreads forrest to neighbouring patches 
        with variable probability based on treestat.
        """
        neighbours = self.get_neighbours()
        for neighbour in neighbours:
            if isinstance(neighbour, RockPatch):
                probability = int(5 + 20 * (self._treestat / 256))   #variable probability 5-20%
                random_num = random.randint(0, 100)
                if random_num < probability:
                    neighbour._mutate()


    def updateland(self) -> None:  #used in simulation
        """
        Initiates the evolution of the patch.
        """
        if self.is_burning():
            self._evolve_firestat()

        self._evolve_treestat()
        self._spread_forrest()
        
    def _mutate(self) -> 'RockPatch':
        """
        Mutates the patch into a RockPatch.
        """
        self._burning = False #for firefigthers functionallity, since they store target patches
        new_patch = RockPatch(self._patch_id, 0, graph_info=self._graph_info)
        self._graph_info.update_patch(new_patch)
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

    Methods:
    random_forrest: Calculates probability of new forrest and 
    mutates the patch if the probability is met.
    """
    def __init__(self, patch_id: int, treestat: int, graph_info=None):
        super().__init__(patch_id, treestat, False, graph_info) #burning = False

        if self._graph_info:
            self._update_color()
        
    def __repr__(self) -> str:
        """
        Return a string representation of the RockPatch.
        """
        return f"RockPatch {self._patch_id}"
    
    def _update_color(self) -> None:
        """
        Removes the color from color_map.
        Note: This only run once, when the patch is created.
        """
        self._graph_info.remove_color(self._patch_id)
    
    def random_forrest(self) -> TreePatch: #used from simulation class
        """
        Calculates probability of new forrest 
        and mutates the patch if the probability is met.
        """
        probability = self._graph_info.options.get("new_forrest_probability")
        random_num = random.randint(0, 10000)  #Making the probability act as permille.
        if random_num < probability:  #Newforrest
            print(f'Random forrest appeared at {self}!') #For testing
            self._mutate()
    
    def _mutate(self) -> 'TreePatch':
        """
        Mutates the patch into a TreePatch or RockPatch.
        """
        new_patch = TreePatch(self._patch_id, 40, graph_info=self._graph_info)
        self._graph_info.update_patch(new_patch)

        return new_patch
        
