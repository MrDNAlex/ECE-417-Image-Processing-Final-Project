import cv2
import time
import numpy as np
from BackgroundSubtractor import BackgroundSubtractor
from VideoProcessorSettings import VideoProcessorSettings

class VideoProcessor:

    capture: cv2.VideoCapture
    """CV2 Video Stream"""
    
    subtractor : BackgroundSubtractor
    """Compiled Gaussian Video Subtractor"""
    
    resizeVideo: bool
    """Boolean toggle for resizing the video on the Fly using OpenCV"""
    
    width:int
    """Width of the Video to Process"""
    
    height: int
    """Height of the Video to Process"""
    
    showComparisonWindow: bool
    """Boolean Toggle for showing the OpenCV Window to view the comparison"""
    
    def __init__(self, videoPath, settings : VideoProcessorSettings):
        
        self.capture = cv2.VideoCapture(videoPath)
        
        # Test that we can open the Video
        returned, frame = self.capture.read()
        if not returned:
            print("Error Reading the Video")
            return
        
        self.width = settings.width
        self.height = settings.height
        self.resizeVideo = settings.resizeVideo
        self.showComparisonWindow = settings.showComparisonWindow
        self.subtractor = BackgroundSubtractor(settings.width, settings.height, settings.K, settings.alpha, settings.threshold, settings.useMorphology, settings.morphologySize)
        
        # Reset video back to first frame
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def run(self):
        """Runs the Background Subtractor on the Video until it is done"""
        
        frameIndex = 0
        totalFrames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        
        while True:
            # Extract a single frame
            returned, frame = self.capture.read()
            if not returned:
                print("Video finished.")
                break
            
            # Resize the Video if needed
            if (self.resizeVideo):
                frame = cv2.resize(frame, (self.height, self.width))
                
            startTime = time.time()
            
            # Apply the Background Gaussian Subtractor 
            mask = self.subtractor.apply(frame)
            
            deltaT = time.time() - startTime
            fps = 1.0 / (deltaT)
            completion = frameIndex / totalFrames * 100
            print(f"Finished Frame! FPS: {fps:.2f} {completion:.2f}%")
            
            # Convert the image to BGR Space so that it can be combined next to raw video
            maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            combinedView = np.hstack((frame, maskBGR))
            
            # Print FPS to terminal to see the difference
            if self.showComparisonWindow:
                
                cv2.putText(combinedView, f"FPS: {fps:.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                cv2.imshow("Video", combinedView)
            
            frameIndex += 1
            
            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the content
        self.capture.release()
        if self.showComparisonWindow:
            cv2.destroyAllWindows()
        