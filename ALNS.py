# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:28:19 2022

@author: Original template by Rolf van Lieshout
"""
from Solution import Solution
import random, time

class Parameters: 
    """
    Class that holds all the parameters for ALNS
    """
    nIterations = 10  #number of iterations of the ALNS
    minSizeNBH = 1      #minimum neighborhood size
    maxSizeNBH = 45     #maximum neighborhood size
    randomSeed = 1      #value of the random seed
    #can add parameters such as cooling rate etc.
    
class ALNS:
    """
    Class that models the ALNS algorithm. 

    Parameters
    ----------
    problem : PDPTW
        The problem instance that we want to solve.
    nDestroyOps : int
        number of destroy operators.
    nRepairOps : int
        number of repair operators.
    randomGen : Random
        random number generator
    currentSolution : Solution
        The current solution in the ALNS algorithm
    bestSolution : Solution
        The best solution currently found
    bestDistance : int
        Distance of the best solution

    """
    def __init__(self,problem,nDestroyOps,nRepairOps):
        self.problem = problem
        self.nDestroyOps = nDestroyOps
        self.nRepairOps = nRepairOps
        self.randomGen = random.Random(Parameters.randomSeed) #used for reproducibility
        
    
    def constructInitialSolution(self):
        """
        Method that constructs an initial solution using random insertion
        """
        self.currentSolution = Solution(self.problem,list(),list(),list(self.problem.requests.copy()))
        self.currentSolution.executeRandomInsertion(self.randomGen)
        self.currentSolution.computeDistance()
        self.bestSolution = self.currentSolution.copy()
        self.bestDistance = self.currentSolution.distance
        print("Created initial solution with distance: "+str(self.bestDistance))
        
    def execute(self):
        """
        Method that executes the ALNS
        """
        starttime = time.time() # get the start time
        self.constructInitialSolution()
        for i in range(Parameters.nIterations):
            #copy the current solution
            self.tempSolution = self.currentSolution.copy()
            #decide on the size of the neighbourhood
            sizeNBH = self.randomGen.randint(Parameters.minSizeNBH,Parameters.maxSizeNBH)
            #decide on the destroy and repair operator numbers
            destroyOpNr = self.determineDestroyOpNr()
            repairOpNr = self.determineRepairOpNr()
            #execute the destroy and the repair and evaluate the result
            self.destroyAndRepair(destroyOpNr, repairOpNr, sizeNBH);
            self.tempSolution.computeDistance()
            print("Iteration "+str(i)+": Found solution with distance: "+str(self.tempSolution.distance))
            #self.tempSolution.print()
            #determine if the new solution is accepted
            self.checkIfAcceptNewSol()
            #update the ALNS weights
            self.updateWeights()
        endtime = time.time() # get the end time
        cpuTime = round(endtime-starttime)
        print("Terminated. Final distance: "+str(self.bestSolution.distance)+", cpuTime: "+str(cpuTime)+" seconds")
    
    def checkIfAcceptNewSol(self):
        """
        Method that checks if we accept the newly found solution
        """
        #if we found a global best solution, we always accept
        if self.tempSolution.distance<self.bestDistance:
            self.bestDistance = self.tempSolution.distance
            self.bestSolution = self.tempSolution.copy()
            self.currentSolution = self.tempSolution.copy()
            print("Found new global best solution.")
        
        #currently, we only accept better solutions, no simulated annealing
        if self.tempSolution.distance<self.currentSolution.distance:
            self.currentSolution = self.tempSolution.copy()
    
    def updateWeights(self):
        """
        Method that updates the weights of the destroy and repair operators
        """
        pass
    
    def determineDestroyOpNr(self):
        """
        Method that determines the destroy operator that will be applied. 
        Currently we just pick a random one with equal probabilities. 
        Could be extended with weights
        """
        return self.randomGen.randint(1, self.nDestroyOps)
    
    def determineRepairOpNr(self):
        """
        Method that determines the repair operator that will be applied. 
        Currently we just pick a random one with equal probabilities. 
        Could be extended with weights
        """
        return self.randomGen.randint(1, self.nRepairOps)
    
    def destroyAndRepair(self,destroyHeuristicNr,repairHeuristicNr,sizeNBH):
        """
        Method that performs the destroy and repair. More destroy and/or
        repair methods can be added

        Parameters
        ----------
        destroyHeuristicNr : int
            number of the destroy operator.
        repairHeuristicNr : int
            number of the repair operator.
        sizeNBH : int
            size of the neighborhood.

        """
        #perform the destroy 
        if destroyHeuristicNr == 1:
            self.tempSolution.executeRandomRemoval(sizeNBH,self.randomGen)
        elif destroyHeuristicNr == 2:
            self.tempSolution.executeDestroyMethod2(sizeNBH)
        else:
            self.tempSolution.executeDestroyMethod3(sizeNBH)
        
        #perform the repair
        if repairHeuristicNr == 1:
            self.tempSolution.executeRandomInsertion(self.randomGen)
        elif repairHeuristicNr == 2:
            self.tempSolution.executeRepairMethod2()
        else:
            self.tempSolution.executeRepairMethod3()


