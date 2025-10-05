# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 13:54:49 2022

@author: Original template by Rolf van Lieshout
"""
import numpy as np
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
                
                afterInsertion = randomRoute.greedyInsert(req)
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
        

        