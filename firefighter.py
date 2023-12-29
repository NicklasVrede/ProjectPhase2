from typing import List, Dict, Tuple, Set, Union
from land_rep import TreePatch, RockPatch
import random
import time


class Firefighter:
    """
    Firefighter class.

    Attributes:
    id (int): Identifies the Firefighter.
    power (int): Variable identifying fireextinguishing power.
    position (int): Variable identifying its position.
    brain (bool): Variable identifying if the firefighter is smart.
    graph_info (GraphInfo): Stores information about the graph.
    path (list): List of patch ids to representing a path.
    target (object): Target patch object on fire.
    """
    def __init__(self, id: int, skill_level: int, position: int):
        self._id = id
        self._position = position  # Identifies the Firefighter's position patch id
        self._brain = False
        self._graph_info = None
        self._initialise_skill(skill_level)

    def _initialise_skill(self, skill_level):
        """
        Initialises the skill level of the firefighter.
        """
        if skill_level == 1:
            self._power = 25  # Default value
        if skill_level == 2:
            self._power = 35
        elif skill_level == 3:
            self._power = 35
            self._brain = True
            self._path = []

    def __repr__(self) -> str:
        """
        Returns the representation of a firefighter.    
        """
        return f"Firefighter {self._id} at {self._get_pos_object()}"
    
    def _get_pos_object(self) -> TreePatch:
        """
        Returns the patch object of the firefighter's position.
        """
        return self._graph_info.patches.get(self._position)
    
    def get_position(self) -> int:
        """
        Returns the position of the firefighter.
        """
        return self._position
    
    def _get_neighbours(self) -> List[Union[TreePatch, RockPatch]]:
        """
        Returns a list of neighbouring patches.
        """
        neighbours_ids = self._get_pos_object().get_neighbours_ids()
        res = []
        for i in neighbours_ids:
            res.append(self._graph_info.patches.get(i))
        return res
    
    def _extinguish_fire(self, patch: Union[TreePatch, RockPatch]):
        """
        Extinguishes fire at a patch.
        """
        patch.firestat -= self._power
        if patch.firestat < 0:
            patch.burning = False
            patch.update_color()

    def move(self):
        """
        Moves the firefighter based on the brain variable.
        """
        position = self._get_pos_object()
        if position.burning:
            return self._extinguish_fire(position) #If firefighter is at fire, he will fight the fire and not move.

        move_pool = []
        neighbours = self._get_neighbours()
        for neighbour in neighbours:
            if neighbour.burning:
                move_pool.append(neighbour)

        if not move_pool: #if no fire
            if self._brain:
                return self._smart_move(position)
            else:
                move_pool = neighbours

        if self._brain:
            self._path = [] #if neighbour is fire, we reset the path.
            
        new_position = random.choice(move_pool)
        self._position = new_position.patch_id
        if new_position.burning:
            self._extinguish_fire(new_position)  #fight fire at new position

    def _smart_move(self, position: Union[TreePatch, RockPatch]):
        """
        Intelligent move function for firefighters with brain.

        Parameters:
        position (object): patch object for the current position of the firefighter.
        """
        all_fires = []
        for patch in list(self._graph_info.patches.values()):
            if patch.burning:
                all_fires.append(patch)
        
        if not all_fires:
            return None #If no fire, firefighter stand still
        
        #check if any fires are closer than target:
        if self._path and self._target.burning:
            for fire in all_fires:
                distance = self._find_least_steps(position, fire)
                if distance < len(self._path):
                    self._path = []  #Reset path
                    break
            
            if self._path:  #More if path is not reset
                self._position = self._path.pop(0)
                return None #important we dont continue.


        #find closest fire:
        closest_fire = None
        closest_distance = None
        for fire in all_fires:
            distance = self._find_least_steps(position, fire)
            if closest_fire == None or distance < closest_distance:
                closest_fire = fire
                closest_distance = distance

        #Now we have the closest fire. And the shortest distance to it.
        #We need to find the shortest path to it:
        shortest_path, target = self._find_path(closest_fire, closest_distance)

        #Now we have the shortest path to the closest fire.
        #We add this path to the firefighter.
        self._path = shortest_path
        self._target = target
        #print(f'Firefighter at {position} moving to {closest_fire} with path {self._path}')

    def _find_least_steps(self, position: Union[TreePatch, RockPatch], target: TreePatch):
        """
        Returns the least steps to a target patch

        Parameters:
        position (object): patch object for the current position of the firefighter.
        target (object): patch object for the target patch.

        Returns:
        int: least steps to target patch
        """
        def add_neigbours(to_check, checked):
            res = to_check.copy()
            for patch in to_check:
                if patch in checked:
                    continue
                res.update(patch.get_neighbours())
            return res

        steps = -1
        to_check = {position}
        checked = set()

        while target not in checked:
            previouse_to_check = to_check.copy()
            to_check = add_neigbours(to_check, checked)
            checked = checked.union(previouse_to_check)
            steps += 1

        return steps
    

    def _find_path(self, closest_fire:TreePatch, distance:int):
        """
        Returns a short path to a target patch

        Parameters:
        closest_fire (object): the closest fire patch object.
        distance (int): the max distance for the path.

        Returns:
        path (List[int]): least steps to target patch
        """
        dead_ends = {} #dict with dead ends as values and steps as keys.
        for i in range(1,distance+2):
            dead_ends[i] = set()   #set default empty sets sets.
        def_position = self._get_pos_object()
        current_position = def_position
        target = closest_fire

        steps = 0
        path = []

        while True:
            steps += 1
            #Check if we have reached the max distance
            if steps > distance:
                dead_ends[steps].add(current_position)
                current_position = def_position
                path, steps = [], 0
                continue
            
            #find neighbours to check:
            neighbours = current_position.get_neighbours()
            neighbours_to_check = []
            for neighbour in neighbours:
                if neighbour not in dead_ends.get(steps) and neighbour.patch_id not in path and neighbour is not def_position: #Avoid dead ends and backtracking
                    neighbours_to_check.append(neighbour)

            #check for dead end:
            if not neighbours_to_check:
                dead_ends[steps].add(current_position)
                current_position = def_position
                path, steps = [], 0
                continue
            
            #Pick random neighbour:
            current_position = random.choice(neighbours_to_check)
            path.append(current_position.patch_id)

            #check if we have reached the target:
            if current_position.patch_id == target.patch_id:
                return path, target