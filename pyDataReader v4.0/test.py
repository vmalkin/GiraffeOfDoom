import mgr_detrended_v2

data = [4,2,3,7,5,6,11,10,10,12,7,7,8,7,7,5,5,2,6,4,6,10,7,8,12,9,11,8,8,4,4,4,2]

a = mgr_detrended_v2.calc_start(data)
b = mgr_detrended_v2.calc_middle(data)
c = mgr_detrended_v2.calc_end(data)

for item in a:
    print(item)

for item in b:
    print(item)

for item in c:
    print(item)