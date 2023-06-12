import Robot
import Node
import openCV
from DIRECTION import DIRECTION

class Course(object):
    def __init__(self, x_rows: int, y_columns: int, robot: Robot):
        self.x_rows = x_rows
        self.y_columns = y_columns
        self.robot = robot
        self.map = [list() for _ in range(x_rows)]
        self.ball_placements = list()
        self.vip_ball = list()
        
        self.white_balls = list()
        
        self.small_goal_placement = [0, 0]
        self.large_goal_placement = [0, 0]

        self.path_direction = DIRECTION.NORTH
    def map_course(self):
        print("Mapping the course")

        # Create entire field
        for x in range(self.x_rows):
            for y in range(self.y_columns):
                self.map[x].append(Node.Node([x,y], 0, 0))

        # Create edges
        self.setup_edges()
        
        
        # Retrieving coordinates from openCV
        self.get_current_white_placements()
        
        # DEBUG: Testing of coordinates for orange and white
        for i in self.white_balls:
            print("COORDINATE (WHITE): " + str(i))
            
        for i in self.vip_ball:
            print("COORDINATE (VIP): " + str(i))

        
        # Setting up rest of field
        self.get_ball_placements()
        self.set_ball_placements()
        self.print_tui_state()
        self.bfs()
        return None

    def setup_edges(self):
        for x in range(self.x_rows):
            for y in range(self.y_columns):
                node = self.get_node(x,y)
                # Adding to the left
                if (x > 0):
                    node.edges.append(self.get_node(x - 1, y))
                    #if(y > 0):
                        #node.edges.append(self.get_node(x - 1, y-1))
                    #if (y < self.y_columns-1):
                        #node.edges.append(self.get_node(x - 1, y+1))
                # Adding right
                if (x < self.x_rows-1):
                    node.edges.append(self.get_node(x+1, y))
                    #if (y > 0):
                        #node.edges.append(self.get_node(x+1, y-1))
                    #if (y < self.y_columns-1):
                        #node.edges.append(self.get_node(x+1, y+1))
                # Adding up/down
                if (y > 0):
                    node.edges.append(self.get_node(x, y-1))
                if (y < self.y_columns-1):
                    node.edges.append(self.get_node(x, y+1))

    def bfs(self):
        explored_nodes = list()
        layered_nodes = list()
        frontier = list()
        ball_found = 0
        layer = 0
        closest_ball_node = None
        path = list()

        # Add robots node to frontier
        layered_nodes.append(list())
        frontier.append(self.get_node(self.robot.pos[0], self.robot.pos[1]))
        print("Started [" + str(self.robot.pos[0]) + ":" + str(self.robot.pos[1]) + "]")

        # Check frontier for balls
        self.get_node(self.robot.pos[0], self.robot.pos[1]).is_explored = 1
        while(ball_found == 0):
            while(len(frontier) > 0):
                # Add all nodes
                nodes_to_add = frontier.pop().edges
                layered_nodes.append(list())
                for i in range(len(nodes_to_add)):
                    if (nodes_to_add[i].is_explored == 0):
                        layered_nodes[layer].append(nodes_to_add[i])
                        nodes_to_add[i].is_explored = 1
                        print("Added ["+str(nodes_to_add[i].coordinates[0])+":"+str(nodes_to_add[i].coordinates[1])+"]")
                    if (nodes_to_add[i].has_ball == 1):
                        ball_found = 1
                        closest_ball_node = nodes_to_add[i]
                        print("Ball has been found: [" + str(nodes_to_add[i].coordinates[0]) +":"+ str(nodes_to_add[i].coordinates[1])+"]")
                        print("On layer: "+str(layer))
            #print("Layer Complete")
            for i in range(len(layered_nodes[layer])):
                frontier.append(layered_nodes[layer][i])
            layer += 1

        # Find the path to the node
        layer -= 1
        print("...")
        print("The Path is")
        path.append(closest_ball_node)
        next_in_path = closest_ball_node
        new_next_in_path = next_in_path
        #print("their neighbours are: " + str(next_in_path.edges))
        robot_node = self.get_node(self.robot.pos[0], self.robot.pos[1])
        for i in range(layer):
            #print("For layer number: "+str(layer-i))
            for k in range(len(layered_nodes[layer-i])):
                if (layered_nodes[layer-i][k] in next_in_path.edges):
                    new_next_in_path = layered_nodes[layer - i][k]
                    path.append(new_next_in_path)
                    print("Next in path is: ["+str(new_next_in_path.coordinates[0])+", "+str(new_next_in_path.coordinates[1])+"]")
                    break
            next_in_path = new_next_in_path

        for k in range(len(layered_nodes[0])):
            if (layered_nodes[0][k] in next_in_path.edges):
                new_next_in_path = layered_nodes[0][k]
                path.append(new_next_in_path)
                print("Next step is: ["+str(new_next_in_path.coordinates[0])+", "+str(new_next_in_path.coordinates[1])+"]")
                break
        self.path_direction = self.find_direction(new_next_in_path, self.get_node(self.robot.pos[0], self.robot.pos[1]))
        print(self.path_direction)
        return None

    def print_tui_state(self):
        print("")
        for y in range(self.y_columns):
            for x in range(self.x_rows):
                if (self.robot.pos[0] == x and self.robot.pos[1] == y):# & self.robot.pos[1] == y):
                    print(" ▲ ", end="")
                else:
                    if (self.get_node(x,y).has_ball == 0):
                        print(" □ ", end="")
                    else:
                        print(" ⦿ ", end="")
            print("")
        return None

    def get_node(self,x,y):
        return self.map[x][y]
    
    
    def set_ball_placements(self):
        for y in range(self.y_columns):
            for x in range(self.x_rows):
                self.get_node(x,y).has_ball = 0
                
        balls: list(int, int)
        for balls in self.white_balls:
            self.get_node(balls[0], balls[1]).has_ball = 1
            #print("Got ball: "+self.get_node(self.ball_placements[b][0], self.ball_placements[b][1]))
            
        '''for b in self.white_balls:
            self.get_node(b[0], b[1]).has_ball = 1
            #print("Got ball: "+self.get_node(self.ball_placements[b][0], self.ball_placements[b][1]))'''


    def find_direction(self, next_path_node: Node, robot_node: Node):
        if (next_path_node.coordinates[0] > robot_node.coordinates[0]):
            return DIRECTION.EAST
        if (next_path_node.coordinates[0] < robot_node.coordinates[0]):
            return DIRECTION.WEST
        if (next_path_node.coordinates[1] < robot_node.coordinates[1]):
            return DIRECTION.NORTH
        if (next_path_node.coordinates[1] > robot_node.coordinates[1]):
            return DIRECTION.SOUTH

    def get_ball_placements(self):
        self.ball_placements.clear()

        # Dummy data
        '''self.ball_placements.append([0, 0])
        self.ball_placements.append([2, 3])
        self.ball_placements.append([6, 4])'''
        

    # Gets the placement of the white balls
    def get_current_white_placements(self):
        white_coordinate: list(int, int)
        for white_coordinate in openCV.openCV.get_white_coordinates():

            # Scaling of the coordinates to work with algorithm
            x_scaled_coordinate = round((white_coordinate[0] / 600) * self.x_rows) - round(((white_coordinate[0] / 600) * self.x_rows) * 0.1)
            y_scaled_coordinate = round((white_coordinate[1] / 450) * self.y_columns)  - round(((white_coordinate[1] / 450) * self.y_columns) * 0.1)
    
            self.white_balls.append( (x_scaled_coordinate, y_scaled_coordinate) )
        
        #openCV.openCV.refresh()
        
        return self.white_balls
        
    # Gets the placement of the orange balls
    def get_current_vip_ball_placement(self):
        vip_coordinate: list(int, int)
        for vip_coordinate in openCV.openCV.get_white_coordinates():
            
            # Scaling of the coordinates to work with algorithm
            x_scaled_coordinate = round((vip_coordinate[0] / 600) * self.x_rows)
            y_scaled_coordinate = round((vip_coordinate[1] / 450) * self.y_columns)    
    
            self.vip_ball.append( (x_scaled_coordinate, y_scaled_coordinate) )
        
        #openCV.openCV.refresh()
        
        return self.vip_ball
    
        