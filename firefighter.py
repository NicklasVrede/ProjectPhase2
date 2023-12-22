import random


class Firefighter:
    def __init__(self, id, skill_level, position, graph_info):
        self.id = id
        self.position = position  # Identifies the Firefighter's position patch id
        self.graph_info = graph_info
        self.brain = False
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


        #Now we have the closest fire. And the shortest distance to it.
        #We need to find the shortest path to it:
        shortest_path = self.find_path(closest_fire, closest_distance)

        #Now we have the shortest path to the closest fire.
        #We add this path to the firefighter.
        self.path = shortest_path
        print(f'Firefighter {self.id} found shortest path to fire {closest_fire} with distance {closest_distance}')

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

        steps = 0
        to_check = {position}
        checked = set()

        while target not in checked:
            steps += 1
            to_check = add_neigbours(to_check, checked)
            checked = to_check.difference(checked)
            #print(f'visited = {checked}')

        return steps

    def find_path(self, closest_fire, distance, steps=0, path=[], current_position=None):
        print(f'distance = {distance}, closest_fire = {closest_fire}, steps = {steps}')
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
                else: 
                    continue
                

    def extinguish_fire(self, patch):
        patch.firestat -= self.power
        if patch.firestat < 0:
            patch.burning = False
            patch.update_color()
            return print(f'Firefighter {self.id} extinguished fire at {patch}')