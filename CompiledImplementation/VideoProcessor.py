import time

import cv2
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
        
        self.subtractor = BackgroundSubtractor(settings.width, settings.height, settings.K, settings.alpha, settings.threshold, settings.useMorphology)
        
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def run(self):
        while True:
            returned, frame = self.capture.read()
            if not returned:
                print("Video finished.")
                break
            
            startTime = time.time()
            
            #resizedFrame = cv2.resize(frame, (self.width, self.height))
            
            mask = self.subtractor.apply(frame)
            
            fps = 1.0 / (time.time() - startTime)
            
            # Print FPS to terminal to see the difference
            print(f"Finished Frame! FPS: {fps:.2f}")
            
            cv2.imshow("Video", frame)
            cv2.imshow("Foreground Mask", mask)
            
            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        self.capture.release()
        cv2.destroyAllWindows()
        