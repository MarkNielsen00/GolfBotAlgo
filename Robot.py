import math

from pybricks import ev3brick as brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

class Robot(object):
    
    '''left_motor = Motor(Port.A)
    right_motor = Motor(Port.B)'''
    
    def __init__(self, direction, pos: list[int]):
        self.direction = direction
        self.angle = 0
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
    
    # Robot turns left
    def turn_left(self):
        Robot.right_motor.run_target(speed = 500, target_angle = -90)
        
    # Robot turns right
    def turn_right(self):
        Robot.left_motor.run_target(speed = 500, target_angle = 90)

    # Robot makes a turn back
    def turn_back(self):
        Robot.right_motor.run_target(speed = 500, target_angle = 180)
        

    # Robot moves forward
    def move_forward(self):
        Robot.right_motor.run(speed = 300)
        Robot.left_motor.run(speed = 300)
        
    def find_angle(self):
        green_location = list(200,200)
        yellow_location = list(200, 250)

        self.direction = math.atan((green_location[1]-yellow_location[1])/(green_location[0]-yellow_location[0]))
