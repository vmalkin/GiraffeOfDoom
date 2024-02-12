import mgr_database
import mgr_plotter
import time

now = time.time()

# data =[
#     ('gp01', now + 1, 20, 100, 34),
#     ('gp01', now + 2, 20, 100, 33),
#     ('gp01', now + 3, 21, 101, 32),
#     ('gp01', now + 4, 21, 102, 31),
#     ('gp01', now + 5, 23, 102, 32),
#     ('gp01', now + 6, 24, 103, 29),
#     ('gp01', now + 7, 24, 105, 26)
# ]
#
# mgr_plotter.basicplot(data)

query_result = mgr_database.db_get_24hr_gsv()
mgr_plotter.polarplot_paths(query_result)
# with open('data.csv', 'w') as d:
#     for line in query_result:
#         dp = ''
#         for e in line:
#            dp = dp + ',' + str(e)
#         d.write(dp + '\n')
# d.close()