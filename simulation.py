from land_representation import GraphInfo
from visualiser_random_forest_graph import Visualiser
import random

class Simulation:
    def __init__(self, graphinfo, options):
        self.graphinfo = graphinfo
        self.color_map = graphinfo.color_map
        self.treegrowth = 1 + options.get("treegrowth") * 0.01
        self.firegrowth = 1 + options.get("firegrowth") * 0.01
        self.newforrest = options.get("newforrest")
        # Initialize other simulation-specific attributes

    def evolve(self):
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

        for firefighter in self.graphinfo.firefighters.values():
            firefighter.move()
            firefighter.extinguish_fire()
            
    def run_simulation(self):
        # Run the entire simulation for the specified number of iterations
        pass

    def get_simulation_results(self):
        # Collect and return data for reporting purposes
        pass