from typing import Dict


class Simulation:
    """
    Initiates the simulation.
    storing a history of the simulation.

    Attributes:
    graphinfo (GraphInfo): Stores information about the graph.
    history (Dict[int, Dict[str, int]]): A dictionary of simulation history.
    """
    def __init__(self, graphinfo: 'GraphInfo'):
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

        patches = self.graphinfo.get_patches().values()
        for patch in patches:
            if patch.get_treestat() == 0: 
                Rock_potulation += 1
            elif patch.is_burning():
                Fire_population += 1
            else: 
                Tree_population += 1

        self.history[len(self.history)] = {"Tree_population" : Tree_population,
                                            "Rock_population" : Rock_potulation,
                                            "Fire_population" : Fire_population}
        
        # Update the simulation for a single iteration

        for patch in patches:
            if patch.get_treestat() == 0:
                patch.random_forrest()
            else:
                patch.updateland()

        self.graphinfo.activate_firefighters()
        
    def get_history(self) -> Dict[int, Dict[str, int]]:
        """
        Returns the simulation history.
        """
        return self.history
        
            

