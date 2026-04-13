
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
    
    def __init__(self, K, alpha, threshold, width, height, resizeVideo, useMorphology, morphologySize, showComparison):
        self.K = K
        self.alpha = alpha
        self.threshold = threshold
        self.resizeVideo = resizeVideo
        self.width = width
        self.height = height
        self.useMorphology = useMorphology
        self.morphologySize = morphologySize
        self.showComparisonWindow = showComparison
        
    