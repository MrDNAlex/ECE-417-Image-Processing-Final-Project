import cv2
import time
import numpy as np
from BackgroundSubtractor import BackgroundSubtractor
from VideoProcessorSettings import VideoProcessorSettings

class VideoProcessor:

    capture: cv2.VideoCapture
    subtractor : BackgroundSubtractor
    width:int
    height: int
    
    def __init__(self, videoPath, settings : VideoProcessorSettings):
        
        self.capture = cv2.VideoCapture(videoPath)
        
        returned, frame = self.capture.read()
        if not returned:
            print("Error Reading the Video")
            return
        
        self.width = settings.width
        self.height = settings.height
        
        self.subtractor = BackgroundSubtractor(settings.width, settings.height, settings.K, settings.alpha, settings.threshold, settings.useMorphology, settings.morphologySize)
        
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def run(self):
        while True:
            returned, frame = self.capture.read()
            if not returned:
                print("Video finished.")
                break
            
            startTime = time.time()
            
            mask = self.subtractor.apply(frame)
            
            maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            combinedView = np.hstack((frame, maskBGR))
            
            fps = 1.0 / (time.time() - startTime)
            
            # Print FPS to terminal to see the difference
            print(f"Finished Frame! FPS: {fps:.2f}")
            
            cv2.putText(combinedView, f"FPS: {fps:.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            
            cv2.imshow("Video", combinedView)
            
            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        self.capture.release()
        cv2.destroyAllWindows()
        