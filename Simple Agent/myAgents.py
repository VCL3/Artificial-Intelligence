"""
This file contains the agents that can be selected to control
Pacman.  To select an agent, use the '-p' option when running
pacman.py. 
"""
from random import choice
from game import Directions
from game import Agent
from game import Actions
import util
import time
import myAgents
import itertools

class RandomAgent(Agent):
	"An agent that chooses random actions"
	def getAction(self, state):
 		"The agent receives a GameState (defined in pacman.py)."
		possibleActions = state.getLegalPacmanActions()
		if "Stop" in possibleActions:
			possibleActions.pop(possibleActions.index("Stop"))
		return choice(possibleActions)
  
class ReflexAgent(Agent):
	"An agent looking for all possible legal actions and chooses actions that lead to food, chooses random actions if no immediate food actions possible"
	def getAction(self, state):
		possibleActions = state.getLegalPacmanActions()
		#remove stop from possibleActions		
		if "Stop" in possibleActions:
			possibleActions.pop(possibleActions.index("Stop"))
		num = len(possibleActions)
		position = state.getPacmanPosition()

		cx = position[0]
		cy = position[1] 
		for i in range(num):
			#find the x, y coordinates of the position of the next state
			tempx = cx
			tempy = cy
			action = possibleActions[i]
			if action == "North":
				tempy = cy + 1
			elif action == "South":
				tempy = cy - 1
			elif action == "West":
				tempx = cx - 1
			elif action == "East":
				tempx = cx + 1
			food = state.hasFood(tempx, tempy)
			if food:
				return action

		return choice(possibleActions)

class StateAgent(Agent):
	"""An agent that eats any food that is immediately accessible. If no food is directly accessible, it will try to move in one direction repeatedly until food is located or it reaches a wall"""

	def registerInitialState(self, state):
		#get last action
		self.action = state.getPacmanState().getDirection()

	def getAction(self, state):
		#keep track of the last actions
		self.registerInitialState(state)
		possibleActions = state.getLegalPacmanActions()
		if "Stop" in possibleActions:
			possibleActions.pop(possibleActions.index("Stop"))
		num = len(possibleActions)
		position = state.getPacmanPosition()
		cx = position[0]
		cy = position[1] 
		 
		for i in range(num):
			#find the x, y coordinates of the position of the next state
			tempx = cx
			tempy = cy
			action = possibleActions[i]
			if action == "North":
				tempy = cy + 1
			elif action == "South":
				tempy = cy - 1
			elif action == "West":
				tempx = cx - 1
			elif action == "East":
				tempx = cx + 1

			food = state.hasFood(tempx, tempy)
			if food:	
				return action

		#check whether the last action is valid
		if self.action in possibleActions:
			return self.action

		#if the last action is not valid, generate new random action
		return choice(possibleActions)






   

