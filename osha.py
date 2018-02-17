#osha.py

import string
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import graphviz 

def main():
	decisionTree()

def decisionTree():
	X = []
	Y = []
	data = open('HW3_Data.txt')
	for line in data:
		example = line.split()
		example.pop(0)
		Y.append(example.pop(-1))
		if example[2] == "Office":
			example[2] = 0
		elif example[2] == "Warehouse":
			example[2] = 1
		X.append(example)
	X.pop(0)
	Y.pop(0)

	for i in range (len(Y)):
		if Y[i] == "Compliant":
			Y[i] = 1
		elif Y[i] == "Safe":
			Y[i] = 2
		else:
			Y[i] = 0

	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(X, Y)

	print(clf.predict([[53.76,9,0],[35.87,35,0]]))

	#create visual graph
	dot_data = tree.export_graphviz(clf, out_file=None) 
	graph = graphviz.Source(dot_data) 
	graph.render("osha")

	#now we need to do predictions and such?

	
	 

if __name__ == '__main__':
	main()