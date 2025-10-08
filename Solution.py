# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:54:49 2022

@author: Original template by Rolf van Lieshout
"""
import numpy as np
import sys
from Route import Route
from Problem import Location, PDPTW

class Solution:
    """
    Method that represents a solution tot the PDPTW

    Attributes
    ----------
    problem : PDPTW
        the problem that corresponds to this solution
    routes : List of Routes
         Routes in the current solution
    served : List of Requests
        Requests served in the current solution
    notServed : List of Requests
         Requests not served in the current solution 
    distance : int
        total distance of the current solution
    """
    def __init__(self,problem,routes,served,notServed): 
        self.problem = problem
        self.routes = routes
        self.served = served
        self.notServed = notServed
        
    def computeDistance(self):
        """
        Method that computes the distance of the solution
        """
        self.distance = 0
        for route in self.routes: 
            self.distance += route.distance
            
    def __str__(self): 
        """
        Method that prints the solution
        """
        nRoutes = len(self.routes)
        nNotServed = len(self.notServed)
        toPrint = f"Solution with {nRoutes} routes and {nNotServed} unserved requests: "
        for route in self.routes: 
            toPrint+= route.__str__()
            
    def executeRandomRemoval(self,nRemove,random):
        """
        Method that executes a random removal of requests
        
        This is destroy method number 1 in the ALNS

        Parameters
        ----------
        nRemove : int
            number of requests that is removed.
                 
        Parameters
        ----------
        randomGen : Random
            Used to generate random numbers

        """
        

        for i in range(nRemove):
            #terminate if no more requests are served
            if len(self.served)==0: 
                break
            #pick a random request and remove it from the solutoin
            req = random.choice(self.served) 
            self.removeRequest(req)
            


    def executeShawRemoval(self, nRemove, random):
        """
        Method that executes Shaw Removal Heuristic: it removes requests that are somewhat similar. This is a variation of the method proposed by Ropke et al. (2006).
        It only considers distance and demand as parameters to evaluate relatedness.

        It's destroy method number 2 in the ALNS 

        Parameters
        ----------
        nRemove : int
            number of requests that are removed.
        randomGen : random
            Used to generate random numbers

        """

        if len(self.served) == 0:
            return
        # Pick a random request (then find similar ones)
        req = random.choice(self.served)
        candidates = self.evaluateRelatedness(req)
        # print(candidates[0][1])
        # print(candidates[1][1])
        for i in range(nRemove):
            if len(self.served) == 0:
                break
            self.removeRequest(candidates[i][1])

    def evaluateRelatedness(self, req):
        """
        Method taht calculates a relatedness parameter between a reference request (req) and all other requests in the problem, returning a list of requests ordered from greatest to lowest relatedness.

        It uses only 2 parameters: distance and demand
        """

        # Pick a random request (then find similar ones)
        
        self.removeRequest(req)
        
        relatedness = []
        
        for request in self.served:
            # Distance component
            pickUpDist = Location.getDistance(req.pickUpLoc, request.pickUpLoc)
            requestDist = Location.getDistance(req.deliveryLoc, request.deliveryLoc)
            R_dist = (pickUpDist+requestDist)  / self.problem.distMatrix_Max
            
            # Demand component (normalized)
            req_demand = req.pickUpLoc.demand
            request_demand = req.pickUpLoc.demand
            
            R_demand = abs(req_demand - request_demand) / self.problem.capacity # Assumes no loc has demand greater than vehicle capacity. Should not matter, since we are using difference between demands anyway, so this should alsways be between 0 and 1.


            # Calculate R (relatedness)
            R =  R_dist + R_demand # relatedness parameter
            
            relatedness.append((req, request, R))
            # print("Printing relatedness")
            # print(relatedness[request])
        relatedness.sort(key=lambda x: x[2], reverse = True) # Sort all requests based on relatedness
        return relatedness
    
    
    def executeWorstReomval(self,nReomve, random):
        """
        Method that executes Worst Removal Heuristic: it removes the requests that appear to be placed in the wrong position in the solution. This is a variation of the method proposed by Ropke et al. (2006).
        

        It's destroy method number 3 in the ALNS 

        Parameters
        ----------
        nRemove : int
            number of requests that are removed.
        randomGen : random
            Used to generate random numbers

        """
        
        if len(self.served) == 0:
            return
        
        
        while nReomve > 0:
            cost = []
            if len(self.served) == 0: # this was werid
                break
            for req in self.served: # to find which route is now serving this requset
                routefound = None
                for route in self.routes:
                    if req in route.requests:
                        routefound = route
                        break
                if routefound is None: # Code should not reach here
                    continue
                # This can be impoved for efficency 
                # insted of calcualting the whole tour, it is possible to calculate the two new line and minus it from the orginal
                
                orginalCost = routefound.distance
                temp = routefound.copy()
                temp.removeRequest(req)
                newCost =temp.distance
                deltaCost = orginalCost - newCost 
                cost.append((req,deltaCost))
                
                
            # randomization controlled by the parameter p
            p = 1 
            
            cost.sort(key=lambda x: x[1] , reverse=True)   # sort by form worst based on the delta cost
            # The random removal
            randomN = random.random()
            reqNumber = int(len(cost) * (randomN ** p))
            
            self.removeRequest(cost[reqNumber][0])
            nReomve -= 1
                        
        
    
    
    def removeRequest(self,request):
        """
        Method that removes a request from the solution
        """
        #iterate over routes to find in which route the request is served
        for route in self.routes:
            if request in route.requests: 
                #remove the request from the route and break from loop
                route.removeRequest(request)
                break
        #update lists with served and unserved requests
        self.served.remove(request)
        self.notServed.append(request)
        
    def copy(self):
        """
        Method that creates a copy of the solution and returns it
        """
        #need a deep copy of routes because routes are modifiable
        routesCopy = list()
        for route in self.routes:
            routesCopy.append(route.copy())
        copy = Solution(self.problem,routesCopy,self.served.copy(),self.notServed.copy())
        copy.computeDistance()
        return copy
        
    def executeRandomInsertion(self,randomGen):
        """
        Method that randomly inserts the unserved requests in the solution
        
        This is repair method number 1 in the ALNS
        
        Parameters
        ----------
        randomGen : Random
            Used to generate random numbers

        """

        #iterate over the list with unserved requests
        while len(self.notServed)>0:
            #pick a random request
            req = randomGen.choice(self.notServed)

            #keep track of routes in which req could be inserted
            potentialRoutes = self.routes.copy() 
            inserted = False
            while len(potentialRoutes)>0:
                #pick a random route
                
                randomRoute = randomGen.choice(potentialRoutes)
                
                afterInsertion, _ = randomRoute.greedyInsert(req)
                if afterInsertion==None:
                    #insertion not feasible, remove route from potential routes
                    potentialRoutes.remove(randomRoute)
                else: 
                    #insertion feasible, update routes and break from while loop
                    inserted = True
                    #print("Possible")
                    self.routes.remove(randomRoute)
                    self.routes.append(afterInsertion)
                    break
            
            # if we were not able to insert, create a new route
            if not inserted:
                #create a new route with the request
                locList = [self.problem.depot,req.pickUpLoc,req.deliveryLoc,self.problem.depot]
                newRoute = Route(locList,[req],self.problem)
                self.routes.append(newRoute)
            #update the lists with served and notServed requests
            self.served.append(req)
            self.notServed.remove(req)
         
    def executeGreedyInsertion(self, randomGen):
        """
        Method that inserts unserved requests in the solution using a basic greedy heuristic.
        It looks for the best overall position to insert each requests.

        This is repair method number 2 in the ANLS.

        Parameters
        ----------
        randomGen : Random
            Used to generate random numbers
        """
        
        while len(self.notServed) > 0:
            bestRequest = None
            bestRoute = None
            bestDist = sys.maxsize
            inserted = False
            for route in self.routes:
                candidateRequest = None
                candidateRoute = None
                candidateDist = sys.maxsize
                for req in self.notServed:
                    newRoute, dist = route.greedyInsert(req)
                    if newRoute == None:
                        continue
                    elif dist<candidateDist:
                        candidateRequest = req
                        candidateRoute = newRoute
                        candidateDist = dist
                if candidateRoute==None:
                    continue
                if candidateDist < bestDist:
                    inserted = True
                    routeToRemove = route
                    bestRequest = candidateRequest
                    bestRoute = candidateRoute
                    bestDist = candidateDist
            if inserted==True:
                self.routes.remove(routeToRemove)
                self.routes.append(bestRoute)
                self.served.append(bestRequest)
                self.notServed.remove(bestRequest)

            elif not inserted:
                #Impossible to insert in existing routes, create new route:
                locList = [self.problem.depot,req.pickUpLoc,req.deliveryLoc,self.problem.depot]
                newRoute = Route(locList,[req],self.problem)
                self.routes.append(newRoute)
                self.served.append(req)
                self.notServed.remove(req)
                
            #update the lists with served and notServed requests
            # I think we should also apend to served and remove from not serves here
            # it reaches, 
            
            
    def executeRegretInsertion(self, randomG):
        """
        Method that inserts unserved requests in the solution using the Regret-k heuristic.
        The regret heuristic tries to improve upon the basic greedy heuristic by incorporating a kind of look ahead
        information when selecting the request to insert.
        k is set to 2 right now.
        
        This is repair method number 3 in the ANLS.
        
        
        
        Parameters
        ----------
        randomGen : Random
            Used to generate random numbers
            
        """
        k = 2 # we can change this, 
        while len(self.notServed) > 0:
            bestRequest = None
            bestRoute = None
            bestRegret = -sys.maxsize # to keep track of the largest Regret
            bestCost = sys.maxsize
            routeToRemove = None
            
            for req in self.notServed:
                costs = []
                
                for route in self.routes:
                    newRoute, dist = route.greedyInsert(req)
                    if newRoute is not None:
                        costs.append((dist,newRoute,route))
                        # newRoute is after insertion
                        # roure is before 
                
                if len(costs) == 0:
                    continue
                
                costs.sort(key=lambda x:x[0]) # sort based on dist
              
                regretCost = 0
             
                 
                for j in range(1,min(k,len(costs))):
                    regretCost = regretCost + costs[j][0] - costs[0][0] # regret cost between best and second option
                if regretCost > bestRegret or (regretCost == bestRegret and costs[0][0] < bestCost): # Ties are broken by selecting the request with best insertion cost
                        bestRegret = regretCost
                        bestRequest = req
                        bestRoute = costs[0][1]  # best route to insert
                        routeToRemove = costs[0][2]
                        #print(cost[0])
                        bestCost = costs[0][0] # we need this for tie breaks
                
                       
                        
            if bestRequest is None:
       
                req = randomG.choice(self.notServed)
                locList = [self.problem.depot, req.pickUpLoc, req.deliveryLoc, self.problem.depot]
                newRoute = Route(locList, [req], self.problem)
                self.routes.append(newRoute)
                self.served.append(req)
                self.notServed.remove(req)
            else:                  
                self.routes.remove(routeToRemove)
                self.routes.append(bestRoute)
                self.served.append(bestRequest)
                self.notServed.remove(bestRequest)
            #break
        #print(cost)
        #print(costs[0])
   
   
            