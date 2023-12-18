from land_representation import GraphInfo
#firefighter.py
class Firefighter:
    def __init__(self, id, skill_level):
        self.id = id
        self.skill_level = skill_level

    def __repr__(self):
        return f'Firefighter {self.id}'

    def extinguish_fire(self):
        # Define the logic for extinguishing fire in a specific patch
        pass   

    #def move(self):
        #for neighbour in self.neighbours:
        #    print(f'neighbour = {neighbour}')
        #    if neighbour.healthstat < 0:
        #        print(f'Firefighter {self.id} moved to {neighbour.patch_id}')
        #        self.position = neighbour.patch_id
        #        break
        #    else:
        #       continue
    
