
class VideoProcessorSettings:
    
    K: int
    
    alpha: float
    
    threshold: float
    
    width:int
    height: int
    
    useMorphology:bool
    morphologySize: int
    
    def __init__(self, K, alpha, threshold, width, height, useMorphology, morphologySize):
        self.K = K
        self.alpha = alpha
        self.threshold = threshold
        self.width = width
        self.height = height
        self.useMorphology = useMorphology
        self.morphologySize = morphologySize
        
    