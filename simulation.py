from land_representation import GraphInfo
from visualiser_random_forest_graph import Visualiser
import random
# to do: fix entire module to fit rest.
class Simulation:
    def __init__(self, graphinfo, options):
        self.graphinfo = graphinfo
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

        patches = self.graphinfo.get_patches()
        for i in patches:
            patch = patches.get(i)
            if patch.treestat is 0: 
                Rock_potulation += 1
            elif patch.burning:
                Fire_population += 1
            else: 
                Tree_population += 1

        self.history[len(self.history)] = {"Tree_population" : Tree_population,   #len scales bad, but we dont care
                                            "Rock_population" : Rock_potulation,
                                            "Fire_population" : Fire_population}

        # Update the simulation for a single iteration
        for i in patches:
            patch = patches.get(i)
            if patch.treestat is 0:
                random_num = random.randint(0, 10000)  #Making the probability act as permille.
                probability = self.newforrest
                if random_num < probability:  #Newforrest
                    print(f'{random_num} < {probability} = {random_num < probability}')
                    patch.mutate()

            elif 256 > patch.treestat > 0:
                patch.grow_or_burn()

                if patch.burning:
                    patch.spread_fire()

        
        self.activate_firefighters()
        self.move_firefighters()



    def get_history(self):
        return self.history

    def move_firefighters(self):
        for fighter in list(self.graphinfo.firefighters.values()):
            fighter.move()

        self.graphinfo.get_firefighter_positions()

    def activate_firefighters(self):
        for fighter in list(self.graphinfo.firefighters.values()):
            fighter.extinguish_fire()
            
    def spread_fire(self):
        patches = self.graphinfo.get_patches()
        for patch in patches.values():
            if patch.treestat < 0:
                patch.spread_fire()

    def spread_trees(self):
        patches = self.graphinfo.get_patches()
        for patch in patches.values():
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