#csp.py

from copy import deepcopy

def main():
	#initialize rooms
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
	actions = [0, 1, 2]
	roomList = [w1, o1, o6, o5, o4, o2, o3, w2, w3, w4]
	bruteForce(roomList, actions)




def bruteForce(roomList, actions):
	root = State([None] * len(roomList), [])
	print("root actions:", root.getActions())
	for i in range(len(actions)):
		print("i is", i)
		child = State(deepcopy(root.actions), [])
		roomNum = 0
		action = actions[i]
		child.setAction(roomNum, actions)
		roomList[roomNum].setAction(actions)
		root.addChild(child)
	print(root)
	for child in root.getChildren():
		print("child:")
		child.printState()
	
def validChild(room, action):
	for neighbor in room.getNeighbors():
		if neighbor.getAction() == action:
			return False
	return True
		


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

class State:
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
		print("State has", len(self.children), "children.")

if __name__ == '__main__':
	main()