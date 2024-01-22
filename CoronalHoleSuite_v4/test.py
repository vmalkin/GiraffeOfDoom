# data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17, 18, 19 ,20, 21]
#
# step = 6
# lower = 0
# upper = step
# step_multiple = 1
# returnlist = []
# tmp = []
#
# for i in range(0, len(data)):
#     if i >= lower:
#         if i < upper:
#             tmp.append(data[i])
#
#     if i >= upper:
#         step_multiple = step_multiple + 1
#         lower = upper
#         upper = step_multiple * step
#         returnlist.append(tmp)
#         tmp = []
#         tmp.append(data[i])
#
#     if i == (len(data) - 1):
#         returnlist.append(tmp)

i = 128
i = int(i / 60) * 60
print(i)


