# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 12:41:37 2022

@author: Original template by Rolf van Lieshout
"""

import numpy as np
import math  

class Request:
    """
    Class that represents a request

    Attributes
    ----------
    pickUpLoc : Location
        The pick-up location.
    deliveryLoc : Location
        The delivery location.
    ID : int
        id of request.

    """
    def __init__(self,pickUpLoc,deliveryLoc,ID):
       
        self.pickUpLoc = pickUpLoc
        self.deliveryLoc = deliveryLoc
        self.ID = ID

class Location:
    """
    Class that represents either (i) a location where a request should be picked up
    or delivered or (ii) the depot
    Attributes
    ----------
    requestID : int
        id of request.
    xLoc : int
        x-coordinate.
    yLoc : int
        y-coordinate.
    demand : int
        demand quantity, positive if pick-up, negative if delivery
    startTW : int
        start time of time window.
    endTW : int
        end time of time window.
    servTime : int
        service time.
    typeLoc : int
        1 if pick-up, -1 if delivery, 0 if depot
    nodeID : int
        id of the node, used for the distance matrix
    """
    def __init__(self,requestID,xLoc,yLoc,demand,startTW,endTW,servTime,typeLoc,nodeID):

        self.requestID = requestID
        self.xLoc = xLoc
        self.yLoc = yLoc
        self.demand = demand
        self.startTW = startTW # start Time Window
        self.endTW = endTW
        self.servTime = servTime
        self.typeLoc = typeLoc
        self.nodeID = nodeID
    
    def __str__(self):
        """
        Method that prints the location
        """
        return f"({self.requestID},{self.typeLoc})"

        
    def getDistance(l1,l2): 
        """
        Method that computes the euclidian distance between two locations
        """
        dx = l1.xLoc-l2.xLoc
        dy = l1.yLoc-l2.yLoc
        return math.sqrt(dx**2+dy**2)
        
class PDPTW: 
    """
    Class that represents a pick-up and delivery problem with time windows
    Attributes
    ----------
    name : string
        name of the instance.
    requests : List of Requests
        The set containing all requests.
    depot : Location
        the depot where all vehicles must start and end.
    locations : Set of Locations
        The set containing all locations
     distMatrix : 2D array
         matrix with all distances between cities
    capacity : int
        capacity of the vehicles
    
    """     
    def __init__(self,name,requests,depot,vehicleCapacity):
        self.name = name
        self.requests = requests
        self.depot = depot
        self.capacity = vehicleCapacity
        ##construct the set with all locations
        self.locations = set()
        self.locations.add(depot)
        for r in self.requests: 
            self.locations.add(r.pickUpLoc)
            self.locations.add(r.deliveryLoc)

        #compute the distance matrix
        self.distMatrix = np.zeros((len(self.locations),len(self.locations))) #init as nxn matrix
        for i in self.locations:
            for j in self.locations:
                distItoJ = Location.getDistance(i,j)
                self.distMatrix[i.nodeID,j.nodeID] = distItoJ
    
    def __str__(self):
        return f" PDPTW problem {self.name} with {len(self.requests)} requests and a vehicle capacity of {self.capacity}"

    
    def readInstance(fileName):
        """
        Method that reads an instance from a file and returns the instancesf
        """
        f = open(fileName)
        requests = list()
        unmatchedPickups = dict()
        unmatchedDeliveries = dict()
        nodeCount = 0
        requestCount = 1
        for line in f.readlines()[1:-6]:            
            asList = []
            n  = 13 #columns start every 13 characters
            for index in range(0, len(line), n):
                asList.append(line[index : index + n].strip())
            

            lID = asList[0]
            x = int(asList[2][:-2]) #need to remove ".0" from the string
            y = int(asList[3][:-2])
            if lID.startswith("D"):
                #it is the depot
                depot = Location(0,x,y,0,0,0,0,0,nodeCount)
                nodeCount += 1        
            elif lID.startswith("C"): 
                # it is a location
                lType = asList[1]
                demand = int(asList[4][:-2])
                startTW = int(asList[5][:-2])
                endTW = int(asList[6][:-2])
                servTime = int(asList[7][:-2])
                partnerID = asList[8]
                if lType == "cp":
                    #it is a pick-up
                    if partnerID in unmatchedDeliveries:
                        deliv = unmatchedDeliveries.pop(partnerID)
                        pickup = Location(deliv.requestID,x,y,demand,startTW,endTW,servTime,1,nodeCount)
                        nodeCount += 1  
                        req = Request(pickup,deliv,deliv.requestID)
                        requests.append(req)
                    else: 
                        pickup = Location(requestCount,x,y,demand,startTW,endTW,servTime,1,nodeCount)
                        nodeCount += 1  
                        requestCount += 1  
                        unmatchedPickups[lID] = pickup
                elif lType == "cd":
                    #it is a delivery
                    if partnerID in unmatchedPickups:
                        pickup = unmatchedPickups.pop(partnerID)
                        deliv = Location(pickup.requestID,x,y,demand,startTW,endTW,servTime,-1,nodeCount)
                        nodeCount += 1  
                        req = Request(pickup,deliv,pickup.requestID)
                        requests.append(req)
                    else: 
                        deliv = Location(requestCount,x,y,demand,startTW,endTW,servTime,-1,nodeCount)
                        nodeCount += 1  
                        requestCount += 1  
                        unmatchedDeliveries[lID] = deliv
                        
        #sanity check: all pickups and deliveries should be matched
        if len(unmatchedDeliveries)+len(unmatchedPickups)>0:
            raise Exception("Not all matched")
        
        # read the vehicle capacity 
        f = open(fileName)
        capLine = f.readlines()[-4]
        capacity = int(capLine[-7:-3].strip())

        return PDPTW(fileName,requests,depot,capacity)
