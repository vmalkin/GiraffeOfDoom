from threading import Thread
import time

class MyThread(Thread):
    def __init__(self):
        Thread.__init__(self, name="My Thread")

    def run(self):
        counter = 0
        while True:
            counter = counter + 1
            print("Thread Counter: " + str(counter))
            time.sleep(5)

if __name__ == "__main__":
    process = MyThread()
    process.start()
    counter = 0
    while True:
        counter = counter + 1
        print("Main Counter: " + str(counter))
        time.sleep(7)
