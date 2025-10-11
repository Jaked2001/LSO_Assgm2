import random
class Parameters: 
    """
    Class that holds all the parameters for ALNS
    """
    
    nIterations = 50  #number of iterations of the ALNS
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
    
    p = 5
    #
    Regretk = 2

    # For shaw removal
    alpha = 0.25 #Calibrated