import pandas as pd

class VideoProcessorSettings:
    
    K: int 
    """Number of Gaussian Kernels to use per pixel"""
    
    alpha: float
    """Learning rate of the Gaussians"""
    
    threshold: float
    """Weight Threshold to cutoff before """
    
    resizeVideo: bool
    """Boolean Toggle on whether to resize the videos image or not"""
    
    width:int
    """Width of the Video to Process"""
    
    height: int
    """Height of the Video to Process"""
    
    useMorphology:bool
    """Boolean Toggle for using Morphology to clean image"""
    
    morphologySize: int
    """Size of the Kernel used for Morphology"""
    
    showComparisonWindow: bool
    """Boolean Toggle for showing the OpenCV Window to view the comparison"""
    
    showObjectTracking: bool
    """Boolean Toggle for showing the Object Tracking within the scene"""
    
    name: str 
    """Name of the Settings"""
    
    def __init__(self, K, alpha, threshold, width, height, resizeVideo, useMorphology, morphologySize, showComparison, showTracking, name = "Settings"):
        self.K = K
        self.alpha = alpha
        self.threshold = threshold
        self.resizeVideo = resizeVideo
        self.width = width
        self.height = height
        self.useMorphology = useMorphology
        self.morphologySize = morphologySize
        self.showComparisonWindow = showComparison
        self.showObjectTracking = showTracking
        self.name = name
        
    def getCSV(self) -> pd.DataFrame:
        
        dataFrame = pd.DataFrame(columns=["Setting Name", "Setting Value"], dtype=str)
        
        dataFrame.loc[len(dataFrame)] = ["Kernels (K)", self.K]
        dataFrame.loc[len(dataFrame)] = ["Alpha", self.alpha]
        dataFrame.loc[len(dataFrame)] = ["Threshold ", self.threshold]
        dataFrame.loc[len(dataFrame)] = ["Resize Video", self.resizeVideo]
        dataFrame.loc[len(dataFrame)] = ["Width", self.width]
        dataFrame.loc[len(dataFrame)] = ["Height", self.height]
        dataFrame.loc[len(dataFrame)] = ["Use Morphology", self.useMorphology]
        dataFrame.loc[len(dataFrame)] = ["Morphology Size", self.morphologySize]
        dataFrame.loc[len(dataFrame)] = ["Show Comparison", self.showComparisonWindow]
        dataFrame.loc[len(dataFrame)] = ["Show Tracking", self.showObjectTracking]
        
        return dataFrame
    
    def clone(self):
        return VideoProcessorSettings(self.K, self.alpha, self.threshold, self.width, self.height, self.resizeVideo, self.useMorphology, self.morphologySize, self.showComparisonWindow, self.showObjectTracking, self.name)
