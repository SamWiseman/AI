#osha.py

import string
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import graphviz 
from copy import deepcopy

def main():
	X = []
	Y = []
	#read file into arrays and preprocess data
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

	crossValidate(10, X, Y)

def crossValidate(k, X, Y):
	totalLength = len(Y)
	splitLength = totalLength // k
	for i in range(k):
		trainingX = deepcopy(X)
		trainingY = deepcopy(Y)
		testingXRange = trainingX[i * splitLength:] if i == k - 1\
			else trainingX[i * splitLength:(i + 1) * splitLength] 
		testingX = deepcopy(testingXRange)
		trainingX = trainingX[:i*splitLength] if i == k - 1 else \
			trainingX[:i * splitLength] + trainingX[(i + 1) * splitLength:]
		testingYRange = trainingY[i * splitLength:] if i == k - 1\
			else trainingY[i * splitLength:(i + 1) * (splitLength)]
		testingY = deepcopy(testingYRange)
		trainingY = trainingY[:i * splitLength] if i == k - 1 else \
			trainingY[:i * splitLength] + trainingY[(i + 1) * splitLength:]
		output = "visulation k = " + str(i + 1)
		decisionTree(trainingX, trainingY, testingX, testingY, output)



def decisionTree(trainingX, trainingY, testingX, testingY, output):
	
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(trainingX, trainingY)
	prediction = clf.predict(testingX)
	if not len(testingY) == len(prediction):
		print("Somebody fucked up. Yikes.")
	for i in range(len(prediction)):
		if prediction[i] == testingY[i]:
			print("Cool! They're equal.")
		else:
			print("Oh well! They are not equal.")

	#message = "We good!" if equal else "Hmmm..."
	#print(message)

	#create visual graph
	dot_data = tree.export_graphviz(clf, out_file=None) 
	graph = graphviz.Source(dot_data) 
	graph.render(output)


	
	 

if __name__ == '__main__':
	main()