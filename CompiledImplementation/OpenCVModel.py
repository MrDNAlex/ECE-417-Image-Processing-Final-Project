import cv2
import numpy as np
from .VideoProcessorSettings import VideoProcessorSettings

# filepath: c:\Users\basne\Desktop\school\ECE417\ECE-417-Image-Processing-Final-Project\Implementation\OpenCVModel.py

class OpenCVModel:
    
    backSub: cv2.BackgroundSubtractor
    
    def __init__(self, settings: VideoProcessorSettings):
        """
        Initialize OpenCV's background subtractor using MOG2 algorithm
        
        Args:
            settings: VideoProcessorSettings object containing configuration
        """
        self.backSub = cv2.createBackgroundSubtractorMOG2(
            detectShadows = False
        )
    
    def apply(self, frame):
        """
        Apply background subtraction to a frame
        
        Args:
            frame: Input video frame (BGR or grayscale)
        
        Returns:
            mask: Binary foreground mask (0 = background, 255 = foreground)
        """
        mask = self.backSub.apply(frame)
        return mask
    
    def getBackgroundImage(self):
        """
        Get the learned background model
        
        Returns:
            background: The background image learned by the model
        """
        return self.backSub.getBackgroundImage()