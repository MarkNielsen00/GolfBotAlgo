import Course
import Robot
import Controller
import openCV
import sys

def main():
    
    if Course.Course.robot_stop == False:
        # OpenCV script
        openCV.main.main()
    
        # Run algorithm
        Controller.run()
        
    else:
        sys.exit(0)



if __name__ == '__main__':
    main()
