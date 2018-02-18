#osha.py

import string
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import graphviz 
from copy import deepcopy
from sklearn.metrics import *

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
	accumulatedStats = [0] * 9
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
		output = i + 1
		stats = decisionTree(trainingX, trainingY, testingX, testingY, output)
		for i in range(len(stats)):
			accumulatedStats[i] += stats[i]

	for i in range(len(accumulatedStats)):
		accumulatedStats[i] /= k

	avgPrec = 0
	avgRec = 0
	avgF1 = 0

	print("**** AVERAGES ****")
	for i in range(len(accumulatedStats)):
		osha = ["NonCompliant", "Compliant", "Safe"]
		if i < 3:
			print("Average precision for "+osha[i%3]+" is "+str(accumulatedStats[i]))
			avgPrec += accumulatedStats[i]
		elif i < 6:
			print("Average recall for "+osha[i%3]+" is "+str(accumulatedStats[i]))
			avgRec += accumulatedStats[i]
		else:
			print("Average F1 for "+osha[i%3]+" is "+str(accumulatedStats[i]))
			avgF1 += accumulatedStats[i]
	avgPrec /= 3
	avgRec /= 3
	avgF1 /= 3
	print("\nTotal average precision is", avgPrec)
	print("Total average recall is", avgRec)
	print("Total average F1 is", avgF1)


def decisionTree(trainingX, trainingY, testingX, testingY, output):
	
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(trainingX, trainingY)
	prediction = clf.predict(testingX)
	if not len(testingY) == len(prediction):
		print("Somebody fucked up. Yikes.")
	print("**** STATS FOR ITERATION " + str(output) + " ****")
	print(["NonCompliant", "Compliant", "Safe"])
	stats = calculateStats(testingY, prediction)
	#create visual graph
	dot_data = tree.export_graphviz(clf, out_file=None) 
	graph = graphviz.Source(dot_data) 
	graph.render("visualization k = " + str(output))
	return stats

def calculateStats(testingY, prediction):
	prec = precision_score(testingY, prediction, average=None)
	rec = recall_score(testingY, prediction, average=None)
	f1 = [2 * ((prec[i] * rec[i]) / (prec[i] + rec[i])) for i in range(len(prec))]
	print("PRECISION")
	print(prec)
	print("RECALL")
	print(rec)
	print("F1")
	print(np.asarray(f1))	
	return prec.tolist() + rec.tolist() + f1



	
	 

if __name__ == '__main__':
	main()