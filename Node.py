import Node
class Node(object):
    def __init__(self, coordinates, has_ball: int, is_goal: int):
        self.vertices = list()
        self.coordinates = coordinates
        # 0 = No ball, 1 = Has ball, 2 = Has orange ball
        self.has_ball = has_ball
        # 0 = No goal, 1 = big goal, 2 = small goal
        self.is_goal = is_goal
        self.is_explored = 0