
satelliteindex = {}
sid1 = 'gps_'
sid2 = 'glonass_'
for i in range(0, 11):
    name = sid1 + str(i)
    satelliteindex[name] = i

for i in range(0, 11):
    step = 11
    name = sid2 + str(i)
    satelliteindex[name] = i + step

print(satelliteindex)