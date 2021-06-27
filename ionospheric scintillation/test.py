import mgr_s4_count_stats

x = [3,3,3,3,4,4,5,4,3,2]
#
# print(mgr_s4_count_stats.mean(x))
# print(mgr_s4_count_stats.median(x))
# print(mgr_s4_count_stats.calc_stdev(x))



testcount = mgr_s4_count_stats.load_values("test.pkl")
print("current list is ", testcount)

testcount = mgr_s4_count_stats.append_value(testcount, 3)

print("Appended value. Mean list is ", meanlist)

print("median value of list ", mgr_s4_count_stats.calc_median(meanlist))
mgr_s4_count_stats.save_values(meanlist, "test.pkl")

