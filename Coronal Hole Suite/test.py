import forecast

tree = []
tree.append("a,4,0.8")
tree.append("a,8,1")
tree.append("a,8,3")
tree.append("a,10,3.5")
tree.append("a,13,3.5")
tree.append("a,16,4.5")
tree.append("a,20,5.5")
tree.append("a,23,4.7")
tree.append("a,28,6")
tree.append("a,30,6")
tree.append("a,33,8")
tree.append("a,35,7")
tree.append("a,38,7")
tree.append("a,42,7.5")

# a and B should be 1.0842 and 0.1715
forecast.calculate_forecast(tree)
