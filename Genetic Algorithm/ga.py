from time import sleep
from random import randrange, random, choice
import pacman
import textDisplay
import sys
from nqueens import *
from myAgents import *
import pylab

class GeneticAlgorithm(object):
    """A genetic algorithm is a model of biological evolution.  It
    maintains a population of candidate solutions.  Typically each
    candidate solution is represented as a list of 0's and 1's. In
    order to make a more general evolutionary search, we will specify
    a discrete number of possible values.  For example, to evolve
    paths through pacman mazes the possible values will be: 'North',
    'South', 'East', or 'West'.

    A fitness function must be defined to score each candidate
    solution.  Initially, a random population is created. Then a
    series of generations are executed.  Each generation, parents are
    selected from the population based on their fitness.  More highly
    fit candidate solutions are more likely to be selected to create
    children.  With some probability crossover will be done to model
    sexual reproduction.  With some probability mutations will occur.
    A generation is complete once all of the original parents have
    been replaced by children.  This process continues until the
    maximum generation is reached or when the isDone method returns
    True.
    """

    def __init__(self, length, popSize, values=[0,1]):
        """
        Constructor of the GeneticAlgorithm class, takes the length of the
        candidate solutions, the size of the population and a list of
        possible values to use in creating candidate solutions.
        Declares all of the necessary class variables here including:
           population size
           fitness of the best candidate solution ever found
           chromosome of the best candidate solution ever found
           list representing the population
           list representing the fitness values of the population
           total fitness of the population
           current generation
           maximum generation
           probability of crossover
           probability of mutation
           list of the best fitness values for each generation
           list of the average fitness values for each generation
        """
        self.popSize = popSize

        self.bestFitness = 0
        self.best = None

        self.population = []
        self.fitnessList = []
        self.fitnessSum = 0

        self.currentGeneration = 0
        self.maximumGeneration = 100

        self.probCross = 0.6
        self.probMutate = 0.1

        self.bestFitnessList = []
        self.avgFitnessList = []

        self.length = length
        self.values = values
        self.generationCounter = 0

    def initializePopulation(self):
        """
        Represent the population as a list of lists.  Each sub-list
        represents a candidate solution.  Initialize each candidate
        solution with random selections from the possible values.
        """
        for i in range(self.popSize):
            candidate = []
            for n in range(self.length):
                candidate.append(choice(self.values))
            self.population.append(candidate)
    
    def evaluatePopulation(self):
        """
        Calculates the fitness of every candidate solution in the
        population.  Calculates the total fitness, the average
        fitness, and the fitness of the best candidate solution in the
        current population. Updates the best ever candidate solution
        and score when appropriate. Maintains lists of the best and 
        average fitness over time.
        """
        currentBestFitness = 0
        self.fitnessSum = 0
        self.fitnessList = []
        for candidate in self.population:
            fitnessScore = self.fitness(candidate)
            if fitnessScore > currentBestFitness:
                currentBestFitness = fitnessScore 
                if fitnessScore > self.bestFitness:
                    self.bestFitness = fitnessScore
                    self.best = candidate
            self.fitnessList.append(fitnessScore)
            self.fitnessSum += fitnessScore
        avgFitness = (self.fitnessSum*1.0) / self.popSize
        self.avgFitnessList.append(avgFitness)
        self.bestFitnessList.append(self.bestFitness)

    def selection(self):
        """
        Implements fitness proportionate selection using a roulette
        wheel. Returns a COPY of the selected candidate solution.
        """
        spin = random() * self.fitnessSum
        partialFitness = 0
        for index in range(self.popSize):
            partialFitness += self.fitnessList[index]
            if partialFitness >= spin:
                break       
        return (self.population[index])[:]

    def crossover(self, parent1, parent2):
        """
        Given two parents, with probability self.probCross, recombine the
        genetic material of the given parents at a randomly selected
        crossover point to create and return two children.  Otherwise
        return the two parents unchanged.
        """
        spin = random()
        if spin > self.probCross:
            return parent1, parent2
        else:
            splitPos = randrange(1, self.length - 1)
            child1 = parent1[0: splitPos] + parent2[splitPos:]
            child2 = parent2[0: splitPos] + parent1[splitPos:]
            return child1, child2

    def mutation(self, child):
        """
        Given a child, with probability self.probMutate, check EVERY
        position in the child for a potential mutation.  This function
        should not return anything; rather, it should modify the
        positions in the child when there are mutations.  Select
        randomly from the possible values, excluding the current
        value.
        """
        for position in range(self.length): 
            prob = random()
            if prob <= self.probMutate:
                moves = self.values[:]
                moves.remove(child[position])
                child[position] = choice(moves)
        return child        

    def oneGeneration(self):
        """
        Execute one generation of evolution.  Use selection, crossover,
        and mutation to create a new population from the current
        population. Does not return a value.  Updates the population,
        and increments the generation counter.
        """
        newPopulation = []
        while len(newPopulation) < self.popSize:
            parent1 = self.selection()
            parent2 = self.selection()
            child1, child2 = self.crossover(parent1, parent2)
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)
            newPopulation.append(child1)
            newPopulation.append(child2)
        if len(newPopulation) > self.popSize:
            extraChild = choice(newPopulation)
            newPopulation.remove(extraChild)
        self.population = newPopulation
        self.currentGeneration += 1

    def evolve(self, maxGen, probCross=0.7, probMutate=0.001):
        """
        Run a series of generations until the maximum generation,
        maxGen, is reached or self.isDone() returns True. Returns
        two things: the best ever chromosome, and the best ever
        score.
        """
        self.probCross = probCross
        self.probMutate = probMutate
        self.maximumGeneration = maxGen

        self.initializePopulation()
        self.evaluatePopulation()

        while (self.currentGeneration < self.maximumGeneration) and (not self.isDone()):
            self.oneGeneration()
            self.evaluatePopulation()

        self.plotStats()

        return self.best, self.bestFitness    

    def fitness(self, memberOfPop):
        """
        The fitness function will change for each problem.  Therefore it
        is NOT defined here.  To use this class to solve a particular
        problem, inherit from this class and define this method.  When
        implemented should return a score where higher is better.
        """
        abstract()
    
    def isDone(self):
        """
        The stopping critera will change for each problem.  Therefore
        it is NOT defined here.  To use this class to solve a
        particular problem, inherit from this class and define this
        method. When implemented should return True or False.
        """
        abstract()

    def plotStats(self):
        """
        This function create a graph showing the average and the best fitness
        values for each generation of one run of evolution.
        """
        pylab.plot(range(self.currentGeneration + 1), self.bestFitnessList, label = 'Best')
        pylab.plot(range(self.currentGeneration+1), self.avgFitnessList, label = 'Average')
        pylab.xlabel("Generations")
        pylab.ylabel("Fitness")
        pylab.title("Sum")
        pylab.legend(loc = 'lower right')
        pylab.xlim(0, self.currentGeneration)
        pylab.ylim(0, self.bestFitness + 1)
        pylab.show()

class SumGA(GeneticAlgorithm):
    """
    An example of using the GeneticAlgorithm class to solve a particular
    problem, in this case finding strings with the maximum number of 1's.
    """
    def fitness(self, memberOfPop):
        """
        The more 1's in the memberOfPop the higher the fitness.
        """
        return sum(memberOfPop)
    
    def isDone(self):
        """
        Stop when the fitness of the the best member of the current
        population is equal to the maximum fitness.
        """
        return self.fitness(self.best) == self.length

class NQueensGA(GeneticAlgorithm):
    """
    Finds solutions to the NQueens problem.
    """
    def fitness(self, chromosome):
        board = NQueens(chromosome)
        return board.safeQueens()

    def isDone(self):
        return self.fitness(self.best) == self.length

class PacmanGA(GeneticAlgorithm):
    """
    Finds fixed length paths of actions for the maze smallOpen that
    try to maximize the Pacman's score.
    """
    def fitness(self, chromosome):
        args['pacman'] = ListAgent(actions = chromosome)
        games = pacman.runGames( **args )
        score = games[0].state.getScore()
        return score

    def isDone(self):
        return self.fitness(self.best) > 1000

def main():
    print "Genetic Algorithm"
    print "Select problem type"
    print "1: Sum of bits"
    print "2: N-Queens"
    print "3: Pacman"
    selection = input("Enter choice:")
    if selection == 1:
        g = SumGA(15, 50)
        g.evolve(200, 0.6, 0.1)
    elif selection == 2:
        g = NQueensGA(8, 75, range(8))
        g.evolve(200, 0.6, 0.1)
    elif selection == 3:
        global args
        args = pacman.readCommand( sys.argv[1:] )
        args['catchExceptions'] = True
        # turn graphics off during evolution
        origDisplay = args['display']
        args['display'] = textDisplay.NullGraphics()

        gameGA = PacmanGA(125, 125, ['North', 'South', 'East', 'West'])
        bestChromo, bestScore = gameGA.evolve(80, 0.3, 0.03)

        # turn graphics on to test the best path found
        args['display'] = origDisplay
        args['pacman'] = ListAgent(actions = bestChromo)
        games = pacman.runGames( **args )
        print "\nBest Chomosome found:"
        print bestChromo
        print "Best Score:", bestScore

if __name__ == "__main__":
    main()