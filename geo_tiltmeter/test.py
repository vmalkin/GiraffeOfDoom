def marker_list(size):
    returnlist = []
    m = ["$0$","$1$","$2$","$3$","$4$","$5$","$6$","$7$", "$8$","$9$"]
    for i in range(0, size):
        j = int((i / size) * 10)
        returnlist.append(m[j])
    return returnlist

size = 200
a = marker_list(size)
print(a)

print(f'{size} {len(a)}')