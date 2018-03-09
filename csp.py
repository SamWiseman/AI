#csp.py
from copy import deepcopy
import sys

def main():
	numActions = 3 if len(sys.argv) < 2 else int(sys.argv[1])
	roomList = generateGraph()
	actions = [i for i in range(numActions)]
	bruteActions = bruteForce(actions, roomList)
	mcvActions = mostConstrainingVariable(actions, roomList)
	

def runMcv(actions, roomList):
	solutions = []
	roomList.sort(key= lambda room: len(room.getNeighbors()), reverse=True)
	return mostConstrainingVariable(actions, roomList, solutions)

def mostConstrainingVariable(actions, roomList, solutions):
	print("wow that sure is constraining!")

def canAdd(action, state, roomList):
	print("yes you can")
#brute force solution: generate all 10-digit ternary numbers
#turn them into arrays and check if each is valid
def bruteForce(actions, roomList):
	allStates = []
	numVariables = len(roomList)
	domainSize = len(actions)
	#generate a ternary number representing each state
	for i in range(domainSize**numVariables):
		state = [actions[0]] * len(roomList)
		num = i
		j = -1
		while num:
			state[j] = num % domainSize
			num //= domainSize
			j -= 1
		allStates.append(state)
	goodStates = []
	for state in allStates:
		if isValid(state, roomList):
			goodStates.append(state)
	print("There are", len(goodStates), "valid solutions.")
	for i in range(len(goodStates)):
		print("\n-------------------- SOLUTION", i+1, "--------------------")
		solution = goodStates[i]
		mapping = {0:"pass", 1:"change temperature", 2:"change humidity"}
		iterations = getIterations(solution, actions)
		for i in range(len(iterations)):
			print("ITERATION", i+1)
			iteration = iterations[i]
			for i in range(len(roomList)):
				print("Heatmiser should", mapping.get(iteration[i]), "in room", roomList[i].getName())

#goes through state, gets a color. gets the corresponding room in roomlist. 
#makes sure none of the neighbors of that room have the same color in state
def isValid(state, roomList):
	stateRooms = deepcopy(roomList)
	for i in range(len(state)):
		action = state[i]
		room = stateRooms[i]
		room.setAction(action)
	for i in range(len(stateRooms)):
		room = stateRooms[i]
		action = state[i]
		neighbors = room.getNeighbors()
		neighborActions = [neighbor.getAction() for neighbor in neighbors]
		if action in neighborActions:
			return False
	print("The state", state, "is valid! Rejoice!")
	return True

#gets "equivalent" iterations for a state that will allow us to perform every action in every room
def getIterations(state, actions):
	iterations = []
	for i in range(len(actions)):
		iterations.append(deepcopy(state))
		iteration = []
		for i in range(len(state)):
			action = state[i]
			state[i] = (action+1) % 3
	return iterations
	
def validChild(room, action):
	conflicts = [neighbor.getAction() for neighbor in room.getNeighbors()]
	return action not in conflicts
	
def generateGraph():
	w1 = Room("Warehouse 1")
	w2 = Room("Warehouse 2")
	w3 = Room("Warehouse 3")
	w4 = Room("Warehouse 4")
	o1 = Room("Office 1")
	o2 = Room("Office 2")
	o3 = Room("Office 3")
	o4 = Room("Office 4")
	o5 = Room("Office 5")
	o6 = Room("Office 6")
	w1.addNeighbors([w2, o2, o4, o5, o1])
	w2.addNeighbors([w1, o2, o3, w3])
	w3.addNeighbors([w2, o3, w4])
	w4.addNeighbors([w3, o4, o5, o6])
	o1.addNeighbors([w1, o6])
	o2.addNeighbors([w1, w2, o3, o4])
	o3.addNeighbors([w2, o2, o4, w3])
	o4.addNeighbors([w1, o2, o3, w4, o5])
	o5.addNeighbors([w1, o4, w4, o6])
	o6.addNeighbors([o1, o5, w4])
	#list of variables such that each room is adjacent to the previous
	return [w1, o1, o6, o5, o4, o2, o3, w2, w3, w4]

class Room:
	def __init__(self, name):
		self.name = name
		self.neighbors = []
		self.action = None

	def addNeighbors(self, nbrs):
		self.neighbors = nbrs

	def getNeighbors(self):
		return self.neighbors

	def getName(self):
		return self.name

	def getAction(self):
		return self.action

	def setAction(self, action):
		self.action = action

'''class State:
	def __init__(self, actions, children):
		self.actions = actions
		self.children = children

	def getChildren(self):
		return self.children

	def getActions(self):
		return self.actions

	def setChildren(self, children):
		self.children = children

	def addChild(self, child):
		self.children.append(child)

	def setActions(self, actions):
		self.actions = actions

	def setAction(self, index, action):
		self.actions[index] = action

	def printState(self):
		print("State actions:", self.actions)
		print("State has", len(self.children), "children.")'''

if __name__ == '__main__':
	main()