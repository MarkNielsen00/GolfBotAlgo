import Robot
import Node

class Course(object):

    def __init__(self, x_rows: int, y_columns: int, robot: Robot):
        self.x_rows = x_rows
        self.y_columns = y_columns
        self.robot = robot
        self.map = [list() for i in range(x_rows)]
        #self.map = Node
    def map_course(self):
        print("Mappping the course")
        for x in range(self.x_rows):
            for y in range(self.y_columns):
                self.map[x-1].append(Node.Node(None, [x,y], 0, 0))
        self.print_tui_state()
        return None

    def print_tui_state(self):
        print("")
        for y in range(self.y_columns):
            for x in range(self.x_rows):
                if (self.get_node(x,y).has_ball == 0):
                    print(" □ ", end="")
            print("")
        return None

    def get_node(self,x,y):
        return self.map[x][y]