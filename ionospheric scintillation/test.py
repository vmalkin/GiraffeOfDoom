import mgr_stats

test = [1,2,3,4,5,6,7,8,9,10]
values = (mgr_stats.wrapper(test, "t_mean.pkl", "t_sigma.pkl"))
print(values)