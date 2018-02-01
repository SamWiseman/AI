#authors: Leila Awad and Sam Wiseman

import sys
from random import *
from statistics import *
from math import *
from queue import *

#emma says: use the edge weights and the heuristic he gave us in the 
#text file to find the mallest "cost" 
#each cost is the weights of the path's edges + the node's heuristic
def main(): 
	searchType = input("Would you like to use baseline or heuristic search?\n")
	accumulatedVisits = []
	accumulatedEnergy = []
	numTrials = 100
	for i in range(numTrials):
		print("----------------------NEW TRIAL----------------------")
		floor = makeFloor()
		heatMiser = HeatMiser(floor)
		currentOffice = randrange(0, 12)
		print("HeatMiser is starting at office " + str(currentOffice + 1) + ".")
		visits = 0
		energy = 0
		trips = 0
		goodConditions = False
		#start loop while not goodConditions:
		while not goodConditions: 
			officeInNeed = heatMiser.findOfficeInNeed()
			if searchType == "baseline":
				searchTuple = heatMiser.breadthFirstSearch(currentOffice, officeInNeed)
			elif searchType == "heuristic":
				searchTuple = heatMiser.heuristicSearch(currentOffice, officeInNeed)
			else:
				print("Invalid search type. Please type 'baseline' or 'heuristic' when prompted.")
				return False
			distanceTraveled = searchTuple[0]
			energyConsumed = searchTuple[1]
			visits += distanceTraveled
			energy += energyConsumed
			trips += 1
			currentOffice = officeInNeed
			heatMiser.adjustOffice(currentOffice)
			goodConditions = heatMiser.checkConditions()
		print("-------------------------------------")
		for office in heatMiser.floor:
			print("Office", office.getId(), "is at", office.getTemp(), "degrees and",\
			 office.getHum(), "percent humidity.")
		#print("HeatMiser made", trips, "trips.")
		heatMiser.reportFinalConditions(visits, energy)
		accumulatedVisits.append(visits)
		accumulatedEnergy.append(energy)
	#at end of 100 sims: calculate avg num visits
	print("------------------------TRIALS FINISHED------------------------")
	avgVisits = format(mean(accumulatedVisits), '.2f')
	visitsDev = format(stdev(accumulatedVisits), '.2f')
	avgEnergy = format(mean(accumulatedEnergy), '.2f')
	energyDev = format(stdev(accumulatedEnergy), '.2f')
	print("Average number of visits across the trials was", avgVisits, "+/-", visitsDev, ".")
	print("Average energy consumed across the trials was", avgEnergy, "+/-", energyDev, ".")

#the heatmiser class can always access the average temp and humidity and their standard devs
#it possesses the floor matrix and accesses offices based on a given index number 
class HeatMiser:
	def __init__(self, floor):
		self.floor = floor
		self.temps = [office.getTemp() for office in floor]
		self.hums = [office.getHum() for office in floor]
		self.avgTemp = 0
		self.tempDev = 0
		self.avgHum = 0
		self.humDev = 0
		self.updateTempStats(True)
		self.updateHumStats(True)

	def updateTempStats(self, mute=False):
		self.temps = [office.getTemp() for office in self.floor]
		self.avgTemp = mean(self.temps)
		self.tempDev = stdev(self.temps)
		if not mute:
			self.reportAverages()

	def updateHumStats(self, mute=False):
		self.hums = [office.getHum() for office in self.floor]
		self.avgHum = mean(self.hums)
		self.humDev = stdev(self.hums)
		if not mute:
			self.reportAverages()

	def reportCurrentConditions(self, office):
		temperature = office.getTemp()
		humidity = office.getHum()
		print("Office", office.getId(),"is", temperature, "degrees and",\
		 humidity, "percent humidity.")

	def findOfficeInNeed(self):
		floor = self.floor
		returnOffice = -1
		desiredTemp = 72
		desiredHum = 47
		biggestDifference = 0
		for i in range(len(floor)):
			office = floor[i]
			temp = office.getTemp()
			hum = office.getHum()
			officeDifference = max(abs(desiredTemp - temp), abs(desiredHum - hum))
			if officeDifference > biggestDifference:
				biggestDifference = officeDifference
				returnOffice = i
		print("Office", returnOffice + 1, "needs to be adjusted. Off we go!")
		return returnOffice

	def adjustOffice(self, officeNum):
		office = self.floor[officeNum]
		self.reportCurrentConditions(office)
		desiredTemp = 72
		desiredHum = 47
		office.setTemp(72.5) if self.avgTemp < desiredTemp else office.setTemp(72)
		office.setHum(47.5) if self.avgHum < desiredHum else office.setHum(47)
		print("HeatMiser changed office", office.getId(), "to", office.getTemp(),\
			"degrees and", office.getHum(), "percent humidity.")
		self.updateTempStats(False)
		self.updateHumStats(True)

	def checkConditions(self):
		idealTemp = 72
		idealHum = 47
		avgTempDist = self.avgTemp - idealTemp
		avgHumDist = self.avgHum - idealHum
		if 0 <= avgTempDist < 1 and 0 <= avgHumDist < 1 \
		and self.tempDev < 1.5 and self.humDev < 1.75:
			return True
		else: 
			return False

	def reportAverages(self):
		print("The floor's average temperature is", format(self.avgTemp, '.2f'),\
		 "+/-", format(self.tempDev, '.2f'), "degrees.")
		print("The floor's average humidity is", format(self.avgHum, '.2f'),\
			"+/-", format(self.humDev, '.2f'), "percent.")

	def reportFinalConditions(self, visits, energy):
		print("The floor's final average temperature is", format(self.avgTemp, '.2f'),\
		 "+/-", format(self.tempDev, '.2f'), "degrees.")
		print("The floor's final average humidity is", format(self.avgHum, '.2f'),\
			"+/-", format(self.humDev, '.2f'), "percent.")
		print("HeatMiser made a total of", visits, "visits.")
		print("HeatMiser consumed a total of", energy, "units of energy.")

	#heatMiser doesn't necessarily take the lowest-energy path. however, it takes the path
	#of least visits and given two paths of equal length, it takes the lower-energy one 
	#because of the way the edges are stored in its memory
	def breadthFirstSearch(self, initial, destination):
		floor = self.floor
		for office in floor:
			office.setVisited(False)
			office.setDistance(0)
			office.setEnergyNeeded(0)
		print("HeatMiser is moving from office " + str(floor[initial].id) + \
			" to office " + str(floor[destination].id) + ".")
		officeQueue = Queue()
		officeQueue.put(floor[initial])
		done = False
		distanceTraveled = 0
		energyConsumed = 0
		while not done:
			currentOffice = officeQueue.get()
			currentOffice.setVisited(True)
			if currentOffice.getId() == destination + 1:
				done = True
				distanceTraveled = currentOffice.getDistance()
				energyConsumed = currentOffice.getEnergyNeeded()
				print("HeatMiser traversed", distanceTraveled, "office(s)"\
					+ ", spending", energyConsumed, "units of energy.")
				return (distanceTraveled, energyConsumed)
			for neighborTuple in currentOffice.neighbors:
				neighborNum = neighborTuple[0]
				neighborEnergy = neighborTuple[1]
				neighbor = floor[neighborNum - 1]
				if not neighbor.getVisited():
					officeQueue.put(neighbor)
					neighbor.setVisited(True)
					neighbor.setDistance(currentOffice.getDistance() + 1)
					neighbor.setEnergyNeeded(currentOffice.getEnergyNeeded() + neighborEnergy)
			if officeQueue.empty():
				print("Couldn't find office!")
				done = True
		return (distanceTraveled, energyConsumed)

	def heuristicSearch(self, initial, destination): 
		floor = self.floor
		for office in floor:
			office.setVisited(False)
			office.setDistance(0)
			office.setEnergyNeeded(0)
		heuristicTable = []
		with open("HeatMiserHeuristicMod.txt") as file:
			for line in file:
				heuristicTable.append(line.split())
		if (initial == destination):
			return (0, 0)
		heuristicTable.pop(0)
		straightLineDistance = 0
		energyConsumed = 0
		visits = 0
		currentOffice = floor[initial]
		done = False
		while not done:
			neighbors = currentOffice.getNeighbors()
			currentOffice.setVisited(True)
			shortest = (-1, -1, -1) #(straight line distance, office index, energy to get there)
			for neighborTuple in neighbors:
				#look up straightline distance and power consumption
				neighborNum = neighborTuple[0]
				neighborEnergy = neighborTuple[1]
				neighbor = floor[neighborNum - 1]
				tableIndex = ((neighborNum - 1)* 12) + destination
				straightLineDistance = int(heuristicTable[tableIndex][2])
				print(straightLineDistance)
				#sum cumulative energy spent with straight line distance for neighbor to destination
				energyRequired = currentOffice.getEnergyNeeded() + neighborEnergy
				utility = energyRequired + straightLineDistance
				if shortest[0] == -1 or utility < shortest[0]:
					shortest = (utility, neighbor.getId()-1, energyRequired)
			#in theory, shortest[0] is the best next choice office to go to
			currentOffice = floor[shortest[1]]
			currentOffice.setEnergyNeeded(shortest[2])
			visits += 1
			if currentOffice.getId() == destination + 1:
				done = True
		return (visits, currentOffice.getEnergyNeeded())


class Office:
	def __init__(self, temp, hum, neighbors, id):
		self.temp = temp
		self.hum = hum
		self.neighbors = neighbors
		self.visited = False
		self.id = id
		self.distance = 0
		self.energyNeeded = 0

	def getTemp(self):
		return self.temp

	def getHum(self):
		return self.hum

	def getNeighbors(self):
		return self.neighbors

	def getVisited(self):
		return self.visited

	def setTemp(self, temp):
		self.temp = temp

	def setHum(self, hum):
		self.hum = hum

	def setVisited(self, visited):
		self.visited = visited

	def getId(self):
		return self.id

	def getDistance(self):
		return self.distance

	def setDistance(self, distance):
		self.distance = distance

	def getEnergyNeeded(self):
		return self.energyNeeded

	def setEnergyNeeded(self, energy):
		self.energyNeeded = energy

#create a simulation floor of given size (12 for this assignment)
def makeFloor():
	tempList = []
	humList = []
	for i in range(12):
		tempList.append(randrange(65, 76))
		humList.append(randrange(45, 56))
	office1 = Office(tempList[0], humList[0], [(2,13),(3,15)], 1)
	office2 = Office(tempList[1], humList[1], [(4,7),(1,13)], 2)
	office3 = Office(tempList[2], humList[2], [(1,15),(7,23)], 3)
	office4 = Office(tempList[3], humList[3], [(5,6),(2,7),(6,10),(9,16)], 4)
	office5 = Office(tempList[4], humList[4], [(8,4),(4,6)], 5)
	office6 = Office(tempList[5], humList[5], [(7,9),(4,10)], 6)
	office7 = Office(tempList[6], humList[6], [(6,9),(10,17),(3,23)], 7)
	office8 = Office(tempList[7], humList[7], [(5,4),(9,5)], 8)
	office9 = Office(tempList[8], humList[8], [(8,5),(10,8),(4,16)], 9)
	office10 = Office(tempList[9], humList[9], [(11,2),(9,8),(7, 17)], 10)
	office11 = Office(tempList[10], humList[10], [(10,2),(12,19)], 11)
	office12 = Office(tempList[11], humList[11], [(11,19)], 12)
	floor = [office1, office2, office3, office4, office5, office6, office7,\
	office8, office9, office10, office11, office12]
	for office in floor: 
		print("The initial state of office", office.id, "is", \
			office.getTemp(), "degrees and", office.getHum(), "percent humidity.")
	return floor

if __name__ == "__main__":
	main()