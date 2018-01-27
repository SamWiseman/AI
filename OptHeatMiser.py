#authors: Leila Awad and Sam Wiseman

from random import *
from statistics import *
from math import *
from queue import *

def main(): 
	accumulatedVisits = []
	numTrials = 100
	for i in range(numTrials):
		print("----------------------NEW TRIAL----------------------")
		floor = makeFloor()
		initialOffice = randrange(0, 12)
		breadthFirstSearch(floor, initialOffice)
		heatMiser = HeatMiser(floor)
		visits = 0
		currentOffice = 0
		goodConditions = False
		while not goodConditions:
			visits += 1
			currentTemp = floor[0][currentOffice]
			currentHum = floor[1][currentOffice]
			goodConditions = heatMiser.makeDecision(currentOffice, currentTemp, currentHum)
			currentOffice = (currentOffice + 1) % numOffices
		print("-------------------------------------")
		for i in range(len(floor[0])):
			print("Office", i + 1, "is at", floor[0][i], "degrees and",\
			 floor[1][i], "percent humidity.")
		heatMiser.reportFinalConditions(visits)
		accumulatedVisits.append(visits)
	#at end of 100 sims: calculate avg num visits
	avgVisits = mean(accumulatedVisits)
	visitsDev = stdev(accumulatedVisits)
	print("Average number of visits across the trials was", avgVisits, "+/-", visitsDev, ".")

#the heatmiser class can always access the average temp and humidity and their standard devs
#it possesses the floor matrix and accesses offices based on a given index number 
class HeatMiser:
	def __init__(self, floor):
		self.temps = floor[0]
		self.hums = floor[1]
		self.avgTemp = 0
		self.tempDev = 0
		self.avgHum = 0
		self.humDev = 0
		self.updateTempStats(True)
		self.updateHumStats(True)

	def raiseTemp(self, officeNum):
		self.reportCurrentConditions(officeNum)
		self.temps[officeNum] += 1
		print("HeatMiser raises the temperature of office", officeNum+1, "by 1."\
		 " It is now", self.temps[officeNum], "degrees.")
		self.updateTempStats()

	def lowerTemp(self, officeNum):
		self.reportCurrentConditions(officeNum)
		self.temps[officeNum] -= 1
		print("HeatMiser lowers the temperature of office", officeNum+1, "by 1."\
		 " It is now", self.temps[officeNum], "degrees.")
		self.updateTempStats()

	def raiseHum(self, officeNum): 
		self.reportCurrentConditions(officeNum)
		self.hums[officeNum] += 1
		print("HeatMiser raises the humidity of office", officeNum+1, "by 1."\
		 " It is now", self.hums[officeNum], "percent.")
		self.updateHumStats()

	def lowerHum(self, officeNum):
		self.reportCurrentConditions(officeNum)
		self.hums[officeNum] -= 1
		print("HeatMiser lowers the humidity of office", officeNum + 1, "by 1."\
		 " It is now", self.hums[officeNum], "percent.")
		self.updateHumStats()

	def updateTempStats(self, mute=False):
		self.avgTemp = mean(self.temps)
		self.tempDev = stdev(self.temps)
		if not mute:
			self.reportAverages()

	def updateHumStats(self, mute=False):
		self.avgHum = mean(self.hums)
		self.humDev = stdev(self.hums)
		if not mute:
			self.reportAverages()

	def reportCurrentConditions(self, officeNum):
		temperature = self.temps[officeNum]
		humidity = self.hums[officeNum]
		print("Office", officeNum + 1,"is", temperature, "degrees and",\
		 humidity, "percent humidity.")

	def reportAverages(self):
		print("The floor's average temperature is", format(self.avgTemp, '.2f'),\
		 "+/-", format(self.tempDev, '.2f'), "degrees.")
		print("The floor's average humidity is", format(self.avgHum, '.2f'),\
			"+/-", format(self.humDev, '.2f'), "percent.")

	def reportFinalConditions(self, visits):
		print("The floor's final average temperature is", format(self.avgTemp, '.2f'),\
		 "+/-", format(self.tempDev, '.2f'), "degrees.")
		print("The floor's final average humidity is", format(self.avgHum, '.2f'),\
			"+/-", format(self.humDev, '.2f'), "percent.")
		print("HeatMiser made a total of", visits, "visits.")

	def makeDecision(self, currentOffice, currentTemp, currentHum):
		idealTemp = 72
		idealHum = 47
		tempDist = abs(idealTemp - currentTemp)
		humDist = abs(idealHum - currentHum)
		if humDist > tempDist: 
			if currentHum >= idealHum + 1:
				self.lowerHum(currentOffice)
			elif currentHum < idealHum:
				self.raiseHum(currentOffice)
			else: 
				self.reportCurrentConditions(currentOffice)
				print("HeatMiser leaves without changing anything.")
				self.reportAverages()
		else:
			if currentTemp >= idealTemp + 1:
				self.lowerTemp(currentOffice)
			elif currentTemp < idealTemp:
				self.raiseTemp(currentOffice)
			else:
				self.reportCurrentConditions(currentOffice)
				print("HeatMiser leaves without changing anything.")
				self.reportAverages()
		
		#determine if goal is reached
		avgTempDist = self.avgTemp - idealTemp
		avgHumDist = self.avgHum - idealHum
		if 0 <= avgTempDist < 1 and 0 <= avgHumDist < 1 \
		and self.tempDev < 1.5 and self.humDev < 1.75:
			return True
		else: 
			return False

def breadthFirstSearch(floor, initial):
	officeQueue = Queue()
	officeQueue.put(floor[initial])
	done = False
	while not done:
		currentOffice = officeQueue.get()
		print(currentOffice.getId())
		currentOffice.setVisited(True)
		for neighborTuple in currentOffice.neighbors:
			neighborNum = neighborTuple[0]
			neighbor = floor[neighborNum - 1]
			if not neighbor.getVisited():
				officeQueue.put(neighbor)
				neighbor.setVisited(True)
		done = officeQueue.empty()
	print("Done")


class Office:
	def __init__(self, temp, hum, neighbors, id):
		self.temp = temp
		self.hum = hum
		self.neighbors = neighbors
		self.visited = False
		self.id = id

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


#create a simulation floor of given size (12 for this assignment)
#index 0 is temps and index 1 is humidities, wherein each index represents an office
def makeFloor():
	tempList = []
	humList = []
	for i in range(12):
		tempList.append(randrange(65, 76))
		humList.append(randrange(45, 56))
	office1 = Office(tempList[0], humList[0], [(2,13),(3,15)], 1)
	office2 = Office(tempList[1], humList[1], [(1,13),(4,7)], 2)
	office3 = Office(tempList[2], humList[2], [(1,15),(7,23)], 3)
	office4 = Office(tempList[3], humList[3], [(2,7),(5,6),(6,10),(9,16)], 4)
	office5 = Office(tempList[4], humList[4], [(4,6),(8,4)], 5)
	office6 = Office(tempList[5], humList[5], [(4,10),(7,9)], 6)
	office7 = Office(tempList[6], humList[6], [(3,23),(6,9),(10,17)], 7)
	office8 = Office(tempList[7], humList[7], [(5,4),(9,5)], 8)
	office9 = Office(tempList[8], humList[8], [(4,16),(8,5),(10,8)], 9)
	office10 = Office(tempList[9], humList[9], [(9,8),(11,2)], 10)
	office11 = Office(tempList[10], humList[10], [(10,2),(12,19)], 11)
	office12 = Office(tempList[11], humList[11], [(11,19)], 12)
	floor = [office1, office2, office3, office4, office5, office6, office7,\
	office8, office9, office10, office11, office12]
	return floor

if __name__ == "__main__":
	main()