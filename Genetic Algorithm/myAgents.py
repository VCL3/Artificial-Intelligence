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

class ListAgent(Agent):
  """
  Used by GA to test out a list of actions.
  """
  def __init__(self, actions = []):
    self.actionIndex = 0
    self.actions = actions

  def getAction(self, state):
    i = self.actionIndex
    self.actionIndex += 1
    if i < len(self.actions):
      return self.actions[i]
    else:
      return None
