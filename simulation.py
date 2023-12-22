from land_representation import RockPatch
import random
# to do: fix entire module to fit rest.
class Simulation:
    def __init__(self, graphinfo, options):
        self.graphinfo = graphinfo
        self.history = {}  # Store simulation history
        # Initialize other simulation-specific attributes

    def evolve(self):
        populations = {"Tree_population": 0, "Rock_population": 0, "Fire_population": 0}

        patches = self.graphinfo.get_patches()
        for patch in patches.values():
            if patch.treestat == 0: 
                populations["Rock_population"] += 1
            elif patch.burning:
                populations["Fire_population"] += 1
                patch.spread_fire()
            else: 
                populations["Tree_population"] += 1

            if patch.treestat > 0:
                patch.evolve_tree()
            elif random.randint(0, 10000) < self.graphinfo.options.get("newforrest"):  # New forest
                patch.mutate()

        self.history[len(self.history)] = populations
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