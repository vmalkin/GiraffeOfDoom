import mgr_plot_detrended

data = [4,2,3,7,5,6,11,10,11,12,7,7,8,7,7,5,5,2,6,4,6,10,7,8,12,9,11,8,8,4,4,4,2,1,2,1,2,1,2,2,3,4,3]
# data = [1,1,1,1,1,1,1,1,1,1,5,5,5,5,5,5,5,5,5,5,1,1,1,1,1,1,1,1,1,1]

print("Original data length: ", len(data))
f = mgr_detrended_v2.wrapper(data)

for i in range(0, len(data)):
    print(data[i], f[i])
