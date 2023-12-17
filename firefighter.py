#firefighter.py
class Firefighter:
    def __init__(self, id, skill_level, position):
        self.id = id
        self.skill_level = skill_level
        self.position = position

    def __repr__(self):
        return "Firefighter " + str(self.id) + " at " + str(self.position)

    def extinguish_fire(self, fire_patch):
        fire.extinguish(self.skill_level)

    
