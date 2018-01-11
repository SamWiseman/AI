#HeatMiser.py
from random import *
from statistics import *

def main(): #need to run simulation 100x
	numOffices = 12
	floor = makeFloor(numOffices)
	heatMiser = HeatMiser(floor)
	#while true - visit offices in order
		#check office temp/hum, avg temp/hum
		#choose/initiate action or inaction
		#recalculate avg temp/hum
		#if done
			#break loop, print stats
		#else
			#update office number
	#print stats: office temp/hum x12, avg temp/hum & stand dev, num trials


	#at end of 100 sims: calculate avg num trials

	heatMiser.raiseTemp(2)
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
		self.updateTempStats()
		self.updateHumStats()

	def raiseTemp(self, officeNum):
		self.temps[officeNum] += 1
		print("The temperature of office", officeNum+1, "has been raised by 1."\
		 " It is now", self.temps[officeNum], "degrees.")
		self.updateTempStats()

	def lowerTemp(self, officeNum):
		self.temps[officeNum] -= 1
		print("The temperature of office", officeNum+1, "has been lowered by 1."\
		 " It is now", self.temps[officeNum], "degrees.")
		self.updateTempStats()

	def raiseHum(self, officeNum): 
		self.hums[officeNum] += 1
		print("The humidity of office", officeNum+1, "has been raised by 1."\
		 " It is now", self.hums[officeNum], "percent.")
		self.updateHumStats()

	def lowerHum(self, officeNum):
		self.hums[officeNum] -= 1
		print("The humidity of office", officeNum + 1, "has been lowered by 1."\
		 " It is now", self.hums[officeNum], "percent.")
		self.updateHumStats()

	def updateTempStats(self):
		self.avgTemp = mean(self.temps)
		self.tempDev = stdev(self.temps)
		print("The floor's average temperature is", format(self.avgTemp, '.2f'),\
		 "+/-", format(self.tempDev, '.2f'), "degrees.")

	def updateHumStats(self):
		self.avgHum = mean(self.hums)
		self.humDev = stdev(self.hums)
		print("The floor's average humidity is", format(self.avgHum, '.2f'),\
			"+/-", format(self.humDev, '.2f'), "percent.")

#create a simulation floor of size 12
#index 0 is temps and index 1 is humidities, wherein each index represents in office
def makeFloor(numOffices):
	floor = [[],[]]
	for i in range(numOffices):
		floor[0].append(randrange(65, 76))
		floor[1].append(randrange(45, 56))
		print("The initial state of office", i + 1, "is:")
		print("Temperature:", floor[0][i])
		print("Humidity:", floor[1][i])
	return floor

if __name__ == "__main__":
	main()