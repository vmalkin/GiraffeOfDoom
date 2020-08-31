import matplotlib.pyplot as plt

# Create a array of marks in different subjects scored by different students
marks = [[1.63365,
1.05394,
0.642,
0.81116,
1.86754,
3.10922,
2.68027,
0.8069,
0.89013,
1.60795,
0.73464,
0.66922,
1.11647,
0.79267,
1.69789,
2.87578,
1.71079,
2.22781,
4.17875,
12,
3.77927,
2.16104,
1.72438
]]
# name of students
# names = ['Sumit', 'Ashu', 'Sonu', 'Kajal', 'Kavita', 'Naman']
# # name of subjects
hours = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,0,1,2,3,4,5,6,7,8,9]


plt.imshow(marks, cmap='Greens', interpolation="none")
plt.show()