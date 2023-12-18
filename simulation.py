from land_representation import GraphInfo
from visualiser_random_forest_graph import Visualiser
import random
# to do: fix entire module to fit rest.
class Simulation:
    def __init__(self, graphinfo, options):
        self.graphinfo = graphinfo
        self.color_map = graphinfo.color_map
        self.treegrowth = 1 + options.get("treegrowth") * 0.01
        self.firegrowth = 1 + options.get("firegrowth") * 0.01
        self.newforrest = options.get("newforrest")
        self.history = {}  # Store simulation history
        # Initialize other simulation-specific attributes

    def evolve(self):
        # Update history
        Tree_population = 0
        Rock_potulation = 0
        Fire_population = 0

        for i in self.graphinfo.patches:
            patch = self.graphinfo.patches.get(i)
            if patch.treestat is 0: 
                Rock_potulation += 1
            elif patch.healthstat > 0:
                Tree_population += 1
            else:
                Fire_population += 1

        self.history[len(self.history)] = {"Tree_population" : Tree_population,   #len scales bad, but we dont care
                                            "Rock_population" : Rock_potulation,
                                            "Fire_population" : Fire_population}

        # Update the simulation for a single iteration
        patches = self.graphinfo.patches
        for i in patches:
            patch = patches.get(i)
            if patch.healthstat is None:
                random_num = random.randint(0, 10000)  #Making the probability act as permille.
                probability = self.newforrest
                if random_num < probability:  #Newforrest
                    print(f'{random_num} < {probability} = {random_num < probability}')
                    print(f'New forrest appeared: ({patch.patch_id})')
                    patch.healthstat = 40
                else:
                    continue #If we try to update color we crash, since there

            elif 256 > patch.healthstat > 0:
                patch.healthstat = int(patch.healthstat * self.treegrowth)
                if patch.healthstat > 256:
                    patch.healthstat = 256

            elif patch.healthstat < 0:
                patch.healthstat = int(patch.healthstat * self.firegrowth)
                if patch.healthstat < -256:   #Fire burns out.
                    patch.healthstat = None
                    print(f'Fire burned out: ({patch.patch_id})')


            self.graphinfo.update_patch_color(patch)
        
        self.extinguish_fire()
        self.move_firefighters()
        self.spread_fire()
        self.spread_trees()

    def get_history(self):
        return self.history

    def move_firefighters(self):
        for fighter in list(self.graphinfo.firefighters.keys()):
            fighter_position = self.graphinfo.fighter_positions.get(fighter)
            pos_patch = self.graphinfo.patches.get(fighter_position)

            if pos_patch.healthstat is not None and pos_patch.healthstat < 0:  #if we dont check for None we crash
                continue #If firefighter is at fire, he will not move.

            neighbors = self.graphinfo.neighbour_register.get(fighter_position)
            move_pool = []
            for neighbor in neighbors:
                if neighbor.healthstat is not None and neighbor.healthstat < 0: #if neighbor is on fire
                    move_pool.append(neighbor)

            if not move_pool: #if no fire
                move_pool = neighbors
    
            new_position = random.choice(move_pool).patch_id   #id not object!

            self.graphinfo.fighter_positions[fighter] = new_position

    def extinguish_fire(self):
        for fighter in list(self.graphinfo.firefighters.keys()):
            fighter_position = self.graphinfo.fighter_positions.get(fighter)
            pos_patch = self.graphinfo.patches.get(fighter_position)

            if pos_patch.healthstat is None or pos_patch.healthstat > 0:
                continue #if patch is stone or tree, we do nothing

            if pos_patch.healthstat < 0:
                pos_patch.healthstat += 50  #flat amount, becuase that makes most sence
                
                if pos_patch.healthstat > 0:
                    pos_patch.healthstat = None
                    self.graphinfo.update_patch_color(pos_patch)
                    print(f'Firefighter {fighter} extinguished fire at: {fighter_position}')
            
    def spread_fire(self):
        for patch in self.graphinfo.patches.values():
            if patch.healthstat is not None and patch.healthstat < 0:  #find fires
                neighbors = self.graphinfo.neighbour_register.get(patch.patch_id)
                for neighbor in neighbors:
                    if neighbor.healthstat is not None and neighbor.healthstat > 0: #if neighbor is tree
                        probability = int(10 + 25 * (abs(patch.healthstat) / 250))   #variable probability
                        random_num = random.randint(0, 100)
                        if random_num < probability:
                            neighbor.healthstat = -50
                            self.graphinfo.update_patch_color(neighbor)
                            print(f'Fire spread from {patch.patch_id} to {neighbor.patch_id}. Probability: {random_num} < {probability}')
                            
    def spread_trees(self):
        for patch in self.graphinfo.patches.values():
            if patch.healthstat is not None and patch.healthstat > 0:  #find trees
                neighbors = self.graphinfo.neighbour_register.get(patch.patch_id)
                for neighbor in neighbors:
                    if neighbor.healthstat is None:  #if neighbor is stone
                        probability = int(2 + 25 * (abs(patch.healthstat) / 250))   #variable probability
                        random_num = random.randint(0, 100)
                        if random_num < probability:
                            neighbor.healthstat = 40
                            self.graphinfo.update_patch_color(neighbor)
                            print(f'Tree spread from {patch.patch_id} to {neighbor.patch_id}. Probability: {random_num} < {probability}')
                        continue    

                    elif neighbor.healthstat > 0: #if neighbor is tree
                        variable_growth = (1 + 0.1 * (patch.healthstat) / 250)
                        neighbor.healthstat= int(neighbor.healthstat * variable_growth)
                        if neighbor.healthstat > 256:
                            neighbor.healthstat = 256
                        self.graphinfo.update_patch_color(neighbor)


    def run_simulation(self):
        # Run the entire simulation for the specified number of iterations
        pass

    def get_simulation_results(self):
        # Collect and return data for reporting purposes
        pass