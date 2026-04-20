import cv2
import numpy as np
from VideoProcessorSettings import VideoProcessorSettings

# filepath: c:\Users\basne\Desktop\school\ECE417\ECE-417-Image-Processing-Final-Project\Implementation\OtsuModel.py

class OtsuModel:
    """
    Background subtractor using Otsu's binarization method.
    Compares each frame to a background model and applies Otsu's thresholding.
    """
    
    background: np.ndarray
    """The background model (first frame or running average)"""
    
    alpha: float
    """Learning rate for background update"""
    
    useInitialBackground: bool
    """If True, use first frame as background; if False, use running average"""
    
    def __init__(self, settings: VideoProcessorSettings):
        """
        Initialize Otsu-based background subtractor
        
        Args:
            settings: VideoProcessorSettings object containing configuration
        """
        self.alpha = getattr(settings, 'alpha', 0.01)
        self.background = None
        self.useInitialBackground = True  # Use first frame as static background
    
    def apply(self, frame):
        """
        Apply Otsu's binarization to detect foreground
        
        Args:
            frame: Input video frame (BGR)
        
        Returns:
            mask: Binary foreground mask (0 = background, 255 = foreground)
        """
        # Convert to grayscale for Otsu's method
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Initialize background with first frame
        if self.background is None:
            self.background = gray.copy()
            return np.zeros_like(gray, dtype=np.uint8)
        
        # Calculate difference from background
        diff = cv2.absdiff(self.background, gray)
        
        # Apply Otsu's thresholding to the difference
        # THRESH_OTSU flag automatically finds optimal threshold
        _, mask = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Update background using running average
        if not self.useInitialBackground:
            self.background = cv2.addWeighted(self.background, 1 - self.alpha, 
                                               gray, self.alpha, 0)
        
        return mask
    
    def getBackgroundImage(self):
        """
        Get the current background model
        
        Returns:
            background: The background image
        """
        return self.background
    
    def setBackground(self, background):
        """
        Manually set the background model
        
        Args:
            background: The background image to use
        """
        self.background = background.copy()
    
    def resetBackground(self):
        """Reset the background model to None (will be reinitialized on next frame)"""
        self.background = None