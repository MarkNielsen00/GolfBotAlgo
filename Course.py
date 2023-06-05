import Robot
import Node

class Course(object):

    def __init__(self, x_rows: int, y_columns: int, robot: Robot):
        self.x_rows = x_rows
        self.y_columns = y_columns
        self.robot = robot
        self.map = [list() for _ in range(x_rows)]
        self.ball_placements = list()
    def map_course(self):
        print("Mappping the course")

        # Create entire field
        for x in range(self.x_rows):
            for y in range(self.y_columns):
                self.map[x-1].append(Node.Node([x,y], 0, 0))

        # Create vertices
        self.setup_vertices()

        # Setting up rest of field
        self.get_ball_placements()
        self.set_ball_placements()
        self.print_tui_state()
        self.bfs()
        return None

    def setup_vertices(self):
        for x in range(self.x_rows):
            for y in range(self.y_columns):
                node = self.get_node(x,y)
                # Adding to the left
                if (x > 0):
                    node.vertices.append(self.get_node(x-2, y))
                    if(y > 0):
                        node.vertices.append(self.get_node(x - 2, y-1))
                    if (y < self.y_columns-1):
                        node.vertices.append(self.get_node(x - 2, y+1))
                # Adding right
                if (x < self.x_rows-1):
                    node.vertices.append(self.get_node(x, y))
                    if (y > 0):
                        node.vertices.append(self.get_node(x, y-1))
                    if (y < self.y_columns-1):
                        node.vertices.append(self.get_node(x, y+1))
                # Adding up/down
                if (y > 0):
                    node.vertices.append(self.get_node(x - 1, y-1))
                if (y < self.y_columns-1):
                    node.vertices.append(self.get_node(x - 1, y+1))

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
        self.get_node(self.robot.pos[0]-1, self.robot.pos[1]).is_explored = 1
        while(ball_found == 0):
            while(len(frontier) > 0):
                # Add all nodes
                nodes_to_add = frontier.pop().vertices
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
            print("Layer Complete")
            for i in range(len(layered_nodes[layer])):
                frontier.append(layered_nodes[layer][i])
            layer += 1

        # Find the path to the node
        layer -= 2
        print("...")
        print("The Path is")
        path.append(closest_ball_node)
        next_in_path = closest_ball_node
        #print("their neighbours are: " + str(next_in_path.vertices))
        robot_node = self.get_node(self.robot.pos[0], self.robot.pos[1])
        for i in range(layer):
            print("For layer number: "+str(layer-i))
            for q in range(len(layered_nodes[layer-i])):
                if (layered_nodes[layer-i][q] in next_in_path.vertices):
                    new_next_in_path = layered_nodes[layer - i][q]
                    #new_next_in_path = self.get_node(next_in_path.coordinates[0], next_in_path.coordinates[1])
                    path.append(new_next_in_path)
                    print("Next in path is: ["+str(new_next_in_path.coordinates[0])+", "+str(next_in_path.coordinates[1])+"]")
                    #print("The node is" + str(new_next_in_path))
                    #print("their neighbours are: " + str(new_next_in_path.vertices))
                    break
            next_in_path = new_next_in_path
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

        for b in range(len(self.ball_placements)):
            self.get_node(self.ball_placements[b][0], self.ball_placements[b][1]).has_ball = 1
            #print("Got ball: "+self.get_node(self.ball_placements[b][0], self.ball_placements[b][1]))

    def get_ball_placements(self):
        self.ball_placements.clear()

        # Dummy data
        self.ball_placements.append([0, 0])
        self.ball_placements.append([2, 3])
        self.ball_placements.append([6, 4])