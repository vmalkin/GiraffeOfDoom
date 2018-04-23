class Grapher():
    def __init__(self):
        self._MAG_RUNNINGAVG_COUNT = 6  # The number of readings "wide" the averaging window is. EVEN NUMBER
        self._NOISE_SPIKE = 2  # Sensor chip flips at this reading
        self._FIELD_CORRECTION = -1  # if the field is increasing in strength, the values should go up, and vica versa

    def wrapper(self):
        pass