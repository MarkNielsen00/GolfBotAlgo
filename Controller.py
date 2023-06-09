import Course
import Robot
class Controller(object):

    def run(self):
        print("Running Algorithm")

        # Setup state
        robot = Robot.Robot(0, [6,8])
        course = Course.Course(8, 10, robot)
        course.map_course()

        finished = 0
        while(finished == 0):
            course.map_course()

        return None
def run():
    controller = Controller()
    controller.run()
    return None