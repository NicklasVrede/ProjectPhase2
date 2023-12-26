import random
import time


class Firefighter:
    def __init__(self, id, skill_level, position):
        self.id = id
        self.position = position  # Identifies the Firefighter's position patch id
        self.brain = False
        self.graph_info = None
        self.initiate_skill(skill_level)

    def initiate_skill(self, skill_level):
        if skill_level == "low":
            self.power = 20  # Default value
        if skill_level == "medium":
            self.power = 25
        elif skill_level == "high":
            self.power = 30
            self.brain = True
            self.path = []

    def __repr__(self) -> str:
        return f"Firefighter {self.id} at {self.get_pos_object()}, with power: {self.power}"
    
    def get_pos_object(self):
        return self.graph_info.patches.get(self.position)
    
    def get_neighbours(self):
        neighbours_ids = self.get_pos_object().get_neighbours_ids()
        res = []
        for i in neighbours_ids:
            res.append(self.graph_info.patches.get(i))
        return res
    
    def extinguish_fire(self, patch):
        patch.firestat -= self.power
        if patch.firestat < 0:
            patch.burning = False
            patch.update_color()
            return print(f'Firefighter {self.id} extinguished fire at {patch}')

    def move(self):
        position = self.get_pos_object()
        if position.burning:
            return self.extinguish_fire(position) #If firefighter is at fire, he will fight the fire.

        move_pool = []
        neighbours = self.get_neighbours()
        for neighbour in neighbours:
            if neighbour.burning:
                move_pool.append(neighbour)

        if not move_pool: #if no fire
            if self.brain:
                return self.smart_move(position)
            else:
                move_pool = neighbours

        if self.brain:
            self.path = [] #if neighbour is fire, we reset the path.
            
        new_position = random.choice(move_pool)
        self.position = new_position.patch_id

    def smart_move(self, position):
        print("smart move")
        if self.path:
            self.position = self.path.pop(0)
            return print(f'Firefighter {self.id} moved to {self.get_pos_object()}')

        all_fires = []
        for patch in list(self.graph_info.patches.values()):
            if patch.burning:
                all_fires.append(patch)
        
        if not all_fires:
            return print(f'Firefighter {self.id} could not find any fire')

        #find closest fire:
        closest_fire = None
        closest_distance = None
        for fire in all_fires:
            distance = self.find_least_steps(position, fire)
            if closest_fire == None or distance < closest_distance:
                closest_fire = fire
                closest_distance = distance

        print(f'Firefighter {self.id} found closest fire at {closest_fire} with distance {closest_distance}')

        #Now we have the closest fire. And the shortest distance to it.
        #We need to find the shortest path to it:
        shortest_path = self.find_path(closest_fire, closest_distance)

        #Now we have the shortest path to the closest fire.
        #We add this path to the firefighter.
        self.path = shortest_path
        print(f'Firefighter {self.id} is using the path {shortest_path}')

    def find_least_steps(self, position, target):
        """
        Returns the least steps to a target patch

        Parameters:
        patch (object): patch object
        target_id (int): target patch id

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
    
    def find_path(self, closest_fire, distance, steps=0, path=None, current_position=None):
        print(f'distance = {distance}, closest_fire = {closest_fire}, steps = {steps}')
        if path is None:
            path = []
        steps += 1
        if current_position is None:
            current_position = self.get_pos_object()

        if steps > distance:
            return None
        
        path.append(current_position) #add current position to path

        if current_position == closest_fire:
            return path
        
        print(f'path = {path}')
        neighbours = current_position.get_neighbours()
        for neighbour in neighbours:
            if neighbour not in path:
                new_path = self.find_path(closest_fire, distance, steps, path.copy(), neighbour)
                if new_path:
                    return new_path

    def find_path(self, closest_fire, distance):
        """
        Returns the shortest path to a target patch

        Parameters:
        patch (object): patch object
        target_id (int): target patch id

        Returns:
        path: least steps to target patch
        """
        dead_ends = {} #dict with dead ends as values and steps as keys.
        for i in range(1,distance+2):
            dead_ends[i] = set()   #set default empty sets sets.
        print(f'dead_ends = {dead_ends}')
        def_position = self.get_pos_object()
        current_position = def_position
        target = closest_fire

        steps = 0
        path = []

        while True:
            steps += 1
            time.sleep(1)
            #Check if we have reached the max distance
            if steps > distance:
                dead_ends[steps].add(current_position)
                current_position = def_position
                print(f'Max distance reached, adding {current_position} to dead_ends')
                path, steps = [], 0
                continue
            
            #find neighbours to check:
            neighbours = current_position.get_neighbours()
            neighbours_to_check = []
            for neighbour in neighbours:
                if neighbour not in dead_ends.get(steps) and neighbour.patch_id not in set(path) and neighbour is not def_position: #Avoid dead ends and backtracking
                    neighbours_to_check.append(neighbour)
            print(f'neighbours_to_check = {neighbours_to_check}')

            #check for dead end:
            if not neighbours_to_check:
                dead_ends[steps].add(current_position)
                print(f'No neighbours, adding {current_position} to dead_ends')
                current_position = def_position
                path, steps = [], 0
                continue
            
            #Pick random neighbour:
            current_position = random.choice(neighbours_to_check)
            path.append(current_position.patch_id)
            print(f'path = {path}')

            #check if we have reached the target:
            if current_position.patch_id == target.patch_id:
                print(f'Found fire at {current_position}')
                return path

                
    
            

            
