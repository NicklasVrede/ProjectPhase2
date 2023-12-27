from typing import Dict
from graph_forrest import GraphInfo
from land_representation import RockPatch
import random
# to do: fix entire module to fit rest.
class Simulation:
    """
    Simulation class.

    Attributes:
    graphinfo (GraphInfo): Stores information about the graph.
    history (Dict[int, Dict[str, int]]): A dictionary of simulation history.
    """
    def __init__(self, graphinfo: 'GraphInfo', options: Dict[str, int] = dict()):
        self.graphinfo = graphinfo
        self.history = {}  # Store simulation history
        # Initialize other simulation-specific attributes

    def evolve(self):
        """
        Evolves the graph for a single iteration.

        """
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
        self.activate_firefighters()
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

  
        
    def get_history(self):
        """
        Returns the simulation history.
        """
        return self.history

    def activate_firefighters(self):
        """
        Activates firefighters.
        """
        for fighter in list(self.graphinfo.firefighters.values()):
            fighter.move()
            
    def spread_fire(self):
        """
        Spreads fire to neighbouring patches.
        """
        patches = self.graphinfo.get_patches()
        for patch in patches.values():
            if patch.treestat < 0:
                patch.spread_fire()

