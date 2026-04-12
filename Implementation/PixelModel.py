from GaussianModel import GaussianModel

class PixelModel:
    
    K: int
    
    alpha: float
    
    threshold: float
    
    models: list[GaussianModel]
    
    STDDEVSQR = 2.5**2
    
    def __init__(self, kernels = 3, alpha = 0.01, threshold = 0.7):
        self.K = kernels
        self.alpha = alpha
        self.threshold = threshold
        self.models = []
        
    def processPixel(self, pixel):
        
        # Add the pixel immediately to Initialize if non exist
        if (len(self.models) == 0):
            initModel = GaussianModel(pixel)
            self.models.append(initModel)
            return 0
        
        matchedModel = None
        
        # Update the Models
        for model in self.models:
            if model.getDistanceSquared(pixel) < self.STDDEVSQR * model.variance:
                model.updateWeight(self.alpha, True)
                model.updateModel(self.alpha, pixel)
                matchedModel = model
            else:
                model.updateWeight(self.alpha)

        # Add the new Model if there are no matches
        if matchedModel is None:
            newModel = GaussianModel(pixel)
            if (len(self.models) < self.K):
                self.models.append(newModel)
            else:
                self.models[-1] = newModel
        
        # Normalize the Model weights
        totalWeight = sum(model.weight for model in self.models)
        for model in self.models:
            model.weight /= totalWeight
        
        # Sort the Models by reverse fitness
        self.models.sort(key=lambda m:m.getFitness(), reverse=True)
        
        weightSum = 0.0
        isBackground = False
        
        for model in self.models:
            weightSum += model.weight
            
            if model == matchedModel:
                isBackground = True
            
            if (weightSum > self.threshold):
                break
            
        if isBackground:
            return 0
        else:
            return 255
        
        
        
    