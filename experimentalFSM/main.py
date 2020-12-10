class State():
    def on_event(self):
        """Events that can cause a transition out"""
        pass

    def __str__(self):
        return self.__class__.__name__


class StateDrive(State):
    def on_event(self, event):
        if event == 'obst_left':
            return StateRight()
        if event == 'obst_right':
            return StateLeft()

class StateRight(State):
    def on_event(self, event):
        if event == 'obst_null':
            return StateDrive()

class StateLeft(State):
    def on_event(self, event):
        if event == 'obst_null':
            return StateDrive()



