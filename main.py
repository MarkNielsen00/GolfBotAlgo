import threading

import Course
import Robot
import Controller
import openCV

def main():

    #Setup multithreading
    ball_positions = list()

    lock = threading.Lock()

    def openCVMultithreaded():
        global ball_positions

        with lock:
            #ball_positions
            openCV.main.main()
    def controllerMultithreaded():
        global ball_positions

        with lock:
            #ball_positions
            Controller.run()

    # Setup OpenCV an algorithm
    thread_1 = threading.Thread(target=openCVMultithreaded())
    thread_2 = threading.Thread(target=controllerMultithreaded())

    # Start Threads
    thread_1.start()
    thread_2.start()


if __name__ == '__main__':
    main()
