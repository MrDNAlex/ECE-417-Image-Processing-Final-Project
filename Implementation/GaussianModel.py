import numpy as np

class GaussianModel:
    
    weight: float
    
    mean: np.ndarray
    
    variance: float
    
    def __init__(self, pixelVals):
        
        self.weight = float(1.0)
        self.mean = np.array(pixelVals, dtype=np.float32)
        self.variance = float(30.0)
    
    def updateModel(self, rho, pixelVals):
        
        distanceSquared = 0.0
        
        for i in range(len(self.mean)):
            self.mean[i] = (1 - rho) * self.mean[i] + rho * pixelVals[i]
            distanceSquared += (pixelVals[i] - self.mean[0])**2
        
        self.variance = (1 - rho) * self.variance + rho*distanceSquared
    
    def getDistanceSquared(self, pixelVals):
        
        distanceSquared = 0.0
        
        for i in range(len(self.mean)):
            distanceSquared += (pixelVals[i] - self.mean[i])**2
            
        return distanceSquared
    
    def updateWeight(self, alpha, match = False):
        if match:
            self.weight = (1 - alpha) * self.weight + alpha
        else:
            self.weight = (1 - alpha) * self.weight
    
    def getFitness(self):
        return self.weight / (self.variance ** 0.5)
        