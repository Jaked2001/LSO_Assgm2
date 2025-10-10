# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 16:28:19 2022

@author: Original template by Rolf van Lieshout
"""
from Solution import Solution
import random, time
import math
import matplotlib.pyplot as plt
import pandas as pd
import os

class Parameters: 
    """
    Class that holds all the parameters for ALNS
    """
    nIterations = 10  #number of iterations of the ALNS
    minSizeNBH = 1      #minimum neighborhood size
    maxSizeNBH = 45     #maximum neighborhood size
    randomSeed = 1      #value of the random seed
    reward = {
        "Global Best": 10,
        "Better Sol": 8,
        "Accepted": 5,
        "Rejected": 1
    }
    updateSpeed = 0.9
    
    #can add parameters such as cooling rate etc.
    startTempControl = 0.3 # this means if will accept the solotions with 10% highes cost with 50% Prob
    coolingRate = 0.2
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
        self.destroyOpsWeigths = [(i, 5) for i in range(1, self.nDestroyOps + 1)]
        self.repairOpsWeigths = [(i, 5) for i in range(1, self.nRepairOps + 1)]
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
        ###
        w = Parameters.startTempControl
        z = self.bestDistance
        self.temperature = - (w * z) / math.log(0.5) # P = e ** (-w.z)/tstart  so tstart = -(w *z) / ln(0.5)
        
        print(self.temperature)
        
        ###
        print("Created initial solution with distance: "+str(self.bestDistance))
        
    def execute(self):
        """
        Method that executes the ALNS
        """
        cost = []
        costcu = []
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
            #self.destroyAndRepair(destroyOpNr, repairOpNr, sizeNBH);
            self.destroyAndRepair(destroyOpNr, repairOpNr, sizeNBH);
            self.tempSolution.computeDistance()
            self.iterationPrint(i, destroyOpNr, repairOpNr, sizeNBH)
            #print("Iteration "+str(i)+": (destroy: " + str(destroyOpNr) + ", repair: " + str(repairOpNr) + ", NHB size: " + str(sizeNBH) + ") Found solution with distance: "+str(self.tempSolution.distance))
            #self.tempSolution.print()
            #determine if the new solution is accepted
            state = self.checkIfAcceptNewSol()
            #update the ALNS weights
            cost.append((i,self.tempSolution.distance))
            costcu.append((i,self.bestSolution.distance))
            self.updateWeights(state, destroyOpNr, repairOpNr)
        endtime = time.time() # get the end time
        cpuTime = round(endtime-starttime)
        print("Terminated. Final distance: "+str(self.bestSolution.distance)+", cpuTime: "+str(cpuTime)+" seconds")
        
        self.drawGraph(cost)
        self.drawGraph(costcu)
        
    def drawGraph(self,data):
        x = [item[0] for item in data]
        y = [item[1] for item in data]
        

        results = pd.DataFrame({
            'Iter': x,
            'Cost': y
            })
        fileName = "log/" +  str(self.problem.name)
        print(fileName)
        results.to_csv(fileName, index = False)
        figureName = fileName + ".png"
        plt.plot(x,y,marker='o')
        plt.show()
        plt.savefig(figureName)
        
        
        
    
    def iterationPrint(self, iterationNr, destroyOpNr, repairOpNr, sizeNBH):
        i = str(iterationNr)
        destroyOp = str(destroyOpNr)
        destroyW = str(round(self.destroyOpsWeigths[destroyOpNr-1][1], 2))
        repariOp = str(repairOpNr)
        repairW = str(round(self.repairOpsWeigths[repairOpNr-1][1], 2))
        sizeNBH = str(sizeNBH)
        distance = str(self.tempSolution.distance)
        

        message = "Iteration " + i + ": (destroy: " + destroyOp + " (" + destroyW + "), repair: " + repariOp + " (" + repairW + "), NBH size: " + sizeNBH + "). Found solution with distance: " + distance
        print(message)
        

    def checkIfAcceptNewSol(self):
        """
        Method that checks if we accept the newly found solution
        """
        
    
        state = "Rejected"
        #if we found a global best solution, we always accept
        if self.tempSolution.distance<self.bestDistance:
            self.bestDistance = self.tempSolution.distance
            self.bestSolution = self.tempSolution.copy()
            self.currentSolution = self.tempSolution.copy()
            state = "Global Best"
            print("Found new global best solution.\n")
        
        #currently, we only accept better solutions, no simulated annealing
        if self.tempSolution.distance<self.currentSolution.distance:
            self.currentSolution = self.tempSolution.copy()
            state = "Better Sol"
        elif random.random() < math.e ** -((self.tempSolution.distance - self.currentSolution.distance)/ self.temperature):
            self.currentSolution = self.tempSolution.copy()
            state = "Accepted"
            print("Accepeted the worse soulution")
            #print(self.temperature)
            
        self.temperature = self.temperature * Parameters.coolingRate    

        return state
    
    def updateWeights(self, state, chosenDestroyOp, chosenRepOp):
        """
        Method that updates the weights of the destroy and repair operators
        """
        reward = Parameters.reward[state]
        updateSpeed = Parameters.updateSpeed

        # Update destroy weights
        oldWeight_d = self.destroyOpsWeigths[chosenDestroyOp-1][1]
        newWeight_d = updateSpeed*oldWeight_d + (1-updateSpeed)*reward
        
        self.destroyOpsWeigths[chosenDestroyOp-1] = (self.destroyOpsWeigths[chosenDestroyOp-1][0], newWeight_d)

        # Update repair weights
        oldWeight_r = self.repairOpsWeigths[chosenRepOp-1][1]
        newWeight_r = updateSpeed*oldWeight_r + (1-updateSpeed)*reward
        
        self.repairOpsWeigths[chosenRepOp-1] = (self.repairOpsWeigths[chosenRepOp-1][0], newWeight_r)


    
    def determineDestroyOpNr(self):
        """
        Method that determines the destroy operator that will be applied. 
        Currently we just pick a random one with equal probabilities. 
        Could be extended with weights
        """
        selectedOpNr = self.randomGen.choices([t[0] for t in self.destroyOpsWeigths], weights=[t[1] for t in self.destroyOpsWeigths], k = 1 )[0]
        return selectedOpNr #self.randomGen.randint(1, self.nDestroyOps)
    
    def determineRepairOpNr(self):
        """
        Method that determines the repair operator that will be applied. 
        Currently we just pick a random one with equal probabilities. 
        Could be extended with weights
        """
        selectedOpNr = self.randomGen.choices([t[0] for t in self.repairOpsWeigths], weights=[t[1] for t in self.repairOpsWeigths], k = 1 )[0]
        return selectedOpNr
    
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
            self.tempSolution.executeShawRemoval(sizeNBH, self.randomGen)
        elif destroyHeuristicNr == 3:
            self.tempSolution.executeWorstReomval(sizeNBH, self.randomGen)

        #perform the repair
        if repairHeuristicNr == 1:
            self.tempSolution.executeRandomInsertion(self.randomGen)
        elif repairHeuristicNr == 2:
            self.tempSolution.executeGreedyInsertion(self.randomGen)
        elif repairHeuristicNr == 3:
            self.tempSolution.executeRegretInsertion(self.randomGen)

  
        
