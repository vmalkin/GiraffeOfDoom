import mgr_database
import mgr_plotter
import time

now = time.time()

data =[
    ('gp01', now + 1, 20, 100, 34),
    ('gp01', now + 2, 20, 100, 33),
    ('gp01', now + 3, 21, 101, 32),
    ('gp01', now + 4, 21, 102, 31),
    ('gp01', now + 5, 23, 102, 32),
    ('gp01', now + 6, 24, 103, 29),
    ('gp01', now + 7, 24, 105, 26)
]

mgr_plotter.basicplot(data)