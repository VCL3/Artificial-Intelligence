# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC
# Berkeley.  The core projects and autograders were primarily created
# by John DeNero (denero@cs.berkeley.edu) and Dan Klein
# (klein@cs.berkeley.edu).  Student side autograding was added by Brad
# Miller, Nick Hay, and Pieter Abbeel (pabbeel@cs.berkeley.edu).

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""
import util

class Node:
    """
    This class outlines a search node that stores all the searching 
    information, which contains:
    current state
    parent node
    action taken to get to the state
    step cost
    total path cost  
    """
    def __init__(self, currentState, parentNode = None, actionTaken = None, stepCost = 1):
        self.currentState = currentState
        self.parentNode = parentNode
        self.actionTaken = actionTaken
        self.stepCost = stepCost
        if parentNode == None:
            self.totalPathCost = 0
        else:
            self.totalPathCost = parentNode.getTotalPathCost() + stepCost

    def getState(self):
        return self.currentState

    def getAction(self):
        if self.parentNode == None:
            return []
        else:
            return self.parentNode.getAction() + [self.actionTaken]

    def getTotalPathCost(self):
        return self.totalPathCost

    def getParentNode(self):
        return self.parentNode
        
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't
    implement any of the methods (in object-oriented terminology: an
    abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of
        actions.  The sequence must be composed of legal moves

        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this
    for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    """
    #DFS initialize the frontier with a stack using the initial state of the problem
    frontier = util.Stack()

    #Create the first node representing the initial state
    node = Node(problem.getStartState())
    
    #Add the first node into the frontier to start
    frontier.push(node)
    
    #For explored, use Pacman position as the key with a value True
    #initialize a dictionary of states already explored 
    explored = dict()

    #While loop to search for the correct path using DFS and return the list of actions taken by the agent
    while (not frontier.isEmpty()):
        currentNode = frontier.pop()
        if problem.isGoalState(currentNode.getState()):
            return currentNode.getAction()
        explored[getKey(currentNode.getState())] = True
        successor = problem.getSuccessors(currentNode.getState())
        for successorState in successor:
            if (not explored.has_key(getKey(successorState[0]))):
                explored[getKey(successorState[0])] = False
            if (not explored[getKey(successorState[0])]):
                newNode = Node(successorState[0], currentNode, successorState[1], successorState[2]) 
                frontier.push(newNode)

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    #BFS initialize the frontier with a queue using the initial state of the problem
    frontier = util.Queue()

    #Create a new node representing the initial state
    node = Node(problem.getStartState())
    
    #Add the node to the frontier to start
    frontier.push(node)
    
    #For explored, use Pacman position as the key with a value True
    #initialize a dictionary of states already explored 
    explored = dict()
    considering = dict()
    considering[getKey(node.getState())] = True

    #While loop using BFS to search for the correct path and return the list of actions taken
    while (not frontier.isEmpty()):
        currentNode = frontier.pop()
        if problem.isGoalState(currentNode.getState()):  
            return currentNode.getAction()
        explored[getKey(currentNode.getState())] = True
        del considering[getKey(currentNode.getState())]
        successor = problem.getSuccessors(currentNode.getState())
        for successorState in successor:
            if (not explored.has_key(getKey(successorState[0]))):
                explored[getKey(successorState[0])] = False
            if (not explored[getKey(successorState[0])]) and (not considering.has_key(getKey(successorState[0]))):
                newNode = Node(successorState[0], currentNode, successorState[1], successorState[2]) 
                frontier.push(newNode)
                considering[getKey(successorState[0])] = True

    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "

    #UCS initialize the frontier with a priority queue using the initial state of the problem
    frontier = util.PriorityQueue()

    #Create the first node representing the initial state
    node = Node(problem.getStartState())
    
    #Add the first node into the frontier to start
    frontier.push(node, 0)
    
    #For explored, use Pacman position as the key with a value True
    #initialize a dictionary of states already explored 
    explored = dict()

    #For considering, use Pacman position as the key with a value pathCost
    #initialize a dictionary of states been considered  
    considering = dict()
    considering[getKey(node.getState())] = 0

    #While loop to search for the correct path using UCS and return the list of actions taken by the agent
    while (not frontier.isEmpty()):
        currentNode = frontier.pop()
        if explored.has_key(getKey(currentNode.getState())):
            continue
        explored[getKey(currentNode.getState())] = True
        del considering[getKey(currentNode.getState())]
        if problem.isGoalState(currentNode.getState()):
            return currentNode.getAction()
        successor = problem.getSuccessors(currentNode.getState())
        for successorState in successor:
            pathCost = currentNode.getTotalPathCost() + successorState[2]
            if ((not explored.has_key(getKey(successorState[0]))) and (not considering.has_key(getKey(successorState[0])))):
                considering[getKey(successorState[0])] = pathCost
                newNode = Node(successorState[0], currentNode, successorState[1], successorState[2]) 
                frontier.push(newNode, pathCost)
            elif ((considering.has_key(getKey(successorState[0]))) and (pathCost < considering[getKey(successorState[0])])):
                considering[getKey(successorState[0])] = pathCost
                newNode = Node(successorState[0], currentNode, successorState[1], successorState[2]) 
                frontier.push(newNode, pathCost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to
    the nearest goal in the provided SearchProblem.  This heuristic is
    trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."

    #UCS initialize the frontier with a priority queue using the initial state of the problem
    frontier = util.PriorityQueue()

    #Create the first node representing the initial state
    node = Node(problem.getStartState())
    
    #Add the first node into the frontier to start
    frontier.push(node, 0 + heuristic(node.getState(), problem))
    
    #For explored, use Pacman position as the key with a value True
    #initialize a dictionary of states already explored 
    explored = dict()

    #For considering, use Pacman position as the key with a value pathCost
    #initialize a dictionary of states been considered  
    considering = dict()
    considering[getKey(node.getState())] =  0 + heuristic(node.getState(), problem)

    #While loop to search for the correct path using UCS and return the list of actions taken by the agent
    while (not frontier.isEmpty()):
        currentNode = frontier.pop()
        if explored.has_key(getKey(currentNode.getState())):
            continue
        explored[getKey(currentNode.getState())] = True
        del considering[getKey(currentNode.getState())]
        if problem.isGoalState(currentNode.getState()):
            return currentNode.getAction()
        successor = problem.getSuccessors(currentNode.getState())
        for successorState in successor:
            pathCost = currentNode.getTotalPathCost() + successorState[2]
            h = heuristic(successorState[0], problem)
            if ((not explored.has_key(getKey(successorState[0]))) and (not considering.has_key(getKey(successorState[0])))):
                considering[getKey(successorState[0])] = pathCost + h
                newNode = Node(successorState[0], currentNode, successorState[1], successorState[2]) 
                frontier.push(newNode, pathCost + h)
            elif ( (considering.has_key(getKey(successorState[0]))) and (pathCost + h < considering[getKey(successorState[0])])):
                considering[getKey(successorState[0])] = pathCost + h
                newNode = Node(successorState[0], currentNode, successorState[1], successorState[2]) 
                frontier.push(newNode, pathCost + h)
    util.raiseNotDefined()

def getKey(state):
    if type(state) is list:
        toReturn = []
        for i in state:
            toReturn.append(tuple(i))
        return tuple(toReturn)
    else:
        return state

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
