from land_representation import RockPatch
import random
# to do: fix entire module to fit rest.
class Simulation:
    def __init__(self, graphinfo, options):
        self.graphinfo = graphinfo
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
            if patch.treestat == 0: 
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
            if isinstance(patch, RockPatch):
                probability = self.graphinfo.options.get("new_forrest_probability")  #Newforrest
                random_num = random.randint(0, 10000)  #Making the probability act as permille.
                if random_num < probability:  #Newforrest
                    print(f'{random_num} < {probability} = {random_num < probability}')
                    patch.mutate()
            else:
                if patch.burning:
                    patch.spread_fire()
                    
                patch.evolve_tree()

        self.activate_firefighters()
        
    def get_history(self):
        return self.history

    def activate_firefighters(self):
        for fighter in list(self.graphinfo.firefighters.values()):
            fighter.move()
            
    def spread_fire(self):
        patches = self.graphinfo.get_patches()
        for patch in patches.values():
            if patch.treestat < 0:
                patch.spread_fire()

