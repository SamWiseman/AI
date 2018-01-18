#HeatMiser.py
from random import *
from statistics import *
from math import *


#current avg: 123 +- 28
def main(): 
	accumulatedVisits = []
	numTrials = 100
	for i in range(numTrials):
		print("----------------------NEW TRIAL----------------------")
		numOffices = 12
		floor = makeFloor(numOffices)
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
		#print stats: office temp/hum x12, avg temp/hum & stand dev, num trials
		print("-------------------------------------")
		for i in range(len(floor[0])):
			print("Office", i + 1, "is at", floor[0][i], "degrees and",\
			 floor[1][i], "percent humidity.")
		heatMiser.reportFinalConditions(visits)
		accumulatedVisits.append(visits)
	#at end of 100 sims: calculate avg num trials
	avgVisits = mean(accumulatedVisits)
	visitsDev = stdev(accumulatedVisits)
	print("Average number of visits across the trials was", avgVisits, "+/-", visitsDev, ".")

#the heatmiser class can always access the average temp and humidity and their standard devs
#it possesses the floor matrix and accesses offices based on a given index number 
class HeatMiser:
	def __init__(self, floor):
		#self.floor = floor
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
		else:#elif tempDist > humDist: 
			if currentTemp >= idealTemp + 1:
				self.lowerTemp(currentOffice)
			elif currentTemp < idealTemp:
				self.raiseTemp(currentOffice)
			else:
				self.reportCurrentConditions(currentOffice)
				print("HeatMiser leaves without changing anything.")
				self.reportAverages()
		#if both temperature and humidity are "ideal..." see which avg is further from ideal and 
		#change to help that average 
		'''else: 
			avgTempDist = idealTemp - self.avgTemp
			avgHumDist = idealTemp - self.avgHum
			if abs(avgHumDist) > abs(avgTempDist):
				if avgHumDist < 0:
					self.lowerHum(currentOffice)
				elif avgHumDist > 0:
					self.raiseHum(currentOffice)
				else:
					self.reportCurrentConditions(currentOffice)
					print("HeatMiser leaves without changing anything2.")
					self.reportAverages()
			else:
				if avgTempDist < 0:
					self.lowerTemp(currentOffice)
				elif avgTempDist > 0:
					self.raiseHum(currentOffice)
				else:
					self.reportCurrentConditions(currentOffice)
					print("HeatMiser leaves without changing anything2.")
					self.reportAverages()'''
		#we can stop if the avg is within .5 of .5 + the ideal for temp and hum and stdev for both is < 1.75
		avgTempDist = self.avgTemp - idealTemp
		avgHumDist = self.avgHum - idealHum
		if 0 <= avgTempDist < 1 and 0 <= avgHumDist < 1 \
		and self.tempDev < 1.5 and self.humDev < 1.75:
			return True
		else: 
			return False

#create a simulation floor of given size (12 for this assignment)
#index 0 is temps and index 1 is humidities, wherein each index represents in office
def makeFloor(numOffices):
	floor = [[],[]]
	for i in range(numOffices):
		floor[0].append(randrange(65, 76))
		floor[1].append(randrange(45, 56))
		print("The initial state of office", i + 1, "is:")
		print("Temperature:", floor[0][i])
		print("Humidity:", floor[1][i])
	print("-------------------------------------")
	return floor

if __name__ == "__main__":
	main()