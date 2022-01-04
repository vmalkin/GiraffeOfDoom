import mgr_detrended_v2

data = [4,2,3,7,5,6,11,10,11,12,7,7,8,7,7,5,5,2,6,4,6,10,7,8,12,9,11,8,8,4,4,4,2]

f = mgr_detrended_v2.wrapper(data, None)

for item in f:
    print(item)


