
class Robot(object):
    def __init__(self, direction, pos: list[int]):
        self.direction = direction
        self.pos = pos
        self.target_pos = [0,0]

    def get_direction(self):
        return None
    def find_target_ball(self):
        return None

    def plan_route(self):
        return None

    def execute_route(self):
        return None