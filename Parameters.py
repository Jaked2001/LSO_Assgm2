import random
class Parameters: 
    """
    Class that holds all the parameters for ALNS
    """
    
    maketwoOpt = False
    

    nIterations = 80  #number of iterations of the ALNS
    
    minSizeNBH = 10      #minimum neighborhood size CALIBRATED
    maxSizeNBH = 45     #maximum neighborhood size CALIBRATED
    
    randomSeed = 1      #value of the random seed
    reward = {
        "Global Best": 10,
        "Better Sol": 8,
        "Accepted": 5,
        "Rejected": 1
    }
    updateSpeed = 0.8 # For adaptive CALIBRATED
    
    #can add parameters such as cooling rate etc.
    startTempControl = 0.1 # Calibrated  # this means if will accept the solotions with 10% highes cost with 50% Prob
    coolingRate = 0.7 #     updateSpeed = 0.8 # For adaptive

    useBattery = True
    # ------------------------- #

    p = 5 # Calibrated
    Regretk = 2 # Calibrated

    # For shaw removal
    alpha = 0.25 # Calibrated
