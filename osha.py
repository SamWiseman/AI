#osha.py

import string
import numpy as np
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import graphviz 
from copy import deepcopy
from sklearn.metrics import *
from sklearn.cluster import KMeans
import random

def main():
	print("---------------------DECISION TREE---------------------\n")
	partOneTree()
	print("\n---------------------K-CLUSTERING---------------------\n")
	partTwoCluster()

def getBaseline(Y):
	counts = {}
	for item in Y:
		if item not in counts:
			counts[item] = 1
		else: 
			counts[item] += 1
	keys = list(counts.keys())
	values = list(counts.values())
	majority = keys[values.index(max(values))]
	X = [majority] * len(Y)
	prec = precision_score(Y, X, average=None)
	rec = recall_score(Y, X, average=None)
	f1 = 2 * ((prec[majority] * rec[majority]) / (prec[majority] + rec[majority]))
	return f1

def crossValidate(k, X, Y, fScores):
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
		stats = decisionTree(trainingX, trainingY, testingX, testingY, output, fScores)
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

def kClustering(X, k):
	kmeans = KMeans(n_clusters=k).fit(X)
	xValues = []
	yValues = []
	for sample in X:
		xValues.append(sample[0])
		yValues.append(sample[1])
	labels = kmeans.labels_
	speedByCluster = [[] for i in range(k)]
	distByCluster = [[] for i in range(k)]
	for i in range(len(labels)):
		label = labels[i]
		speed = X[i][0]
		dist = X[i][1]
		speedByCluster[label].append(speed)
		distByCluster[label].append(dist)
	for i in range(k):
		plt.scatter(speedByCluster[i], distByCluster[i])
		#plt.scatter(xValues, yValues)
	centroids = kmeans.cluster_centers_
	centroidsX = [centroid[0] for centroid in centroids]
	centroidsY = [centroid[1] for centroid in centroids]
	plt.scatter(centroidsX, centroidsY, marker="*")
	sumsSquared = kmeans.inertia_
	print("Sum of squares for k =",k,":", sumsSquared)
	output = str(k) + " clusters.png"
	plt.xlabel("Speed")
	plt.ylabel("Distance")
	plt.savefig(output)
	return sumsSquared

def decisionTree(trainingX, trainingY, testingX, testingY, output, fScores):
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(trainingX, trainingY)
	prediction = clf.predict(testingX)
	if not len(testingY) == len(prediction):
		print("Somebody fucked up. Yikes.")
	print("**** STATS FOR ITERATION " + str(output) + " ****")
	print(["NonCompliant", "Compliant", "Safe"])
	stats = calculateStats(testingY, prediction, fScores)
	'''
	dot_data = tree.export_graphviz(clf, out_file=None) 
	graph = graphviz.Source(dot_data) 
	graph.render("visualization k = " + str(output))'''
	return stats

def calculateStats(testingY, prediction, fScores):
	prec = precision_score(testingY, prediction, average=None)
	rec = recall_score(testingY, prediction, average=None)
	f1 = [2 * ((prec[i] * rec[i]) / (prec[i] + rec[i])) for i in range(len(prec))]
	print("PRECISION")
	print(prec)
	print("RECALL")
	print(rec)
	print("F1")
	print(np.asarray(f1))
	fScores.append(sum(f1)/3)	
	return prec.tolist() + rec.tolist() + f1

def partOneTree():
	X = []
	Y = []
	#read file into arrays and preprocess data
	data = open('HW3_Data.txt').readlines()
	data.pop(0)
	random.shuffle(data)
	print(data)
	for line in data:
		sample = line.split()
		sample.pop(0)
		Y.append(sample.pop(-1))
		if sample[2] == "Office":
			sample[2] = 0
		elif sample[2] == "Warehouse":
			sample[2] = 1
		X.append(sample)
	for i in range (len(Y)):
		if Y[i] == "Compliant":
			Y[i] = 1
		elif Y[i] == "Safe":
			Y[i] = 2
		else:
			Y[i] = 0
	fScores = []
	crossValidate(10, X, Y, fScores)
	majorityBaseline = getBaseline(Y)
	plt.plot(fScores)
	plt.plot([majorityBaseline] * len(fScores))
	plt.xlabel("Fold")
	plt.ylabel("F1")
	plt.savefig('BaselineComparison.png')

def partTwoCluster():
	X = []
	data = open('HW3_Data.txt').readlines()
	for i in range(1, len(data)):
		X.append([float(data[i].split()[1])] + [int(data[i].split()[2])])
	sumSquaredError = []
	minClusters = 1
	xValues = range(minClusters, 11)
	for k in xValues:
		sumSquaredError.append(kClustering(X, k))
	#to find the elbow in the graph, find the point with the greatest difference between slopes
	#the x value of this point is supposedly the ideal number of clusters
	elbowK = 0
	maxDiff = 0
	slopes = [abs(sumSquaredError[i + 1] - sumSquaredError[i]) for i in range(len(xValues) - 1)]
	for i in range(len(slopes) - 1):
		diff = abs(slopes[i + 1] - slopes[i])
		if diff > maxDiff:
			maxDiff = diff
			elbowK = 1 + i + minClusters
	print("The elbow occurs at k = " + str(elbowK) + \
		". This is the ideal k for clustering.")
	plt.gcf().clear()
	plt.plot(xValues, sumSquaredError)
	plt.xlabel("Number of clusters")
	plt.ylabel("Sum squared error")
	plt.savefig('SquaredError.png')

	 

if __name__ == '__main__':
	main()