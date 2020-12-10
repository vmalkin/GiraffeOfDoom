from time import sleep

class State():
    def transition(self, event):
        """Events that can cause a transition out"""
        pass



class StateDrive(State):
    def __init__(self):
        # do something when in this state
        print("Driving")

    def transition(self, event):
        if event == 'obst_left':
            return StateRight()
        elif event == 'obst_right':
            return StateLeft()
        else:
            return StateDrive()

class StateRight(State):
    def __init__(self):
        # do something when in this state
        print("Turning Right")

    def transition(self, event):
        if event == 'obst_null':
            return StateDrive()
        else:
            return StateRight()

class StateLeft(State):
    def __init__(self):
        # do something when in this state
        print("Turning Left")

    def transition(self, event):
        if event == 'obst_null':
            return StateDrive()
        else:
            return StateLeft()

class Robot:
    def __init__(self):
        self.state = StateDrive()

    def transition(self, event):
        self.state = self.state.transition(event)

robby = Robot()

if __name__ == "__main__":
    while True:
        robby.transition('obst_right')
        sleep(1)
