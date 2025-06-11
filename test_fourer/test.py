d = [0,1,2,3,4,5,6,7,8,9,10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

chunk_length = 5

h = 0
for i in range(0, len(d), chunk_length):
    if i == 0:
        pass
    else:
        print(i, d[h:i])
        h = i