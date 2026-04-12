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
        
        self.subtractor = BackgroundSubtractor(settings)
        
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def run(self):
        while True:
            returned, frame = self.capture.read()
            if not returned:
                print("Video finished.")
                break
            
            resizedFrame = cv2.resize(frame, (self.width, self.height))
            
            mask = self.subtractor.apply(resizedFrame)
            
            print("Finished Frame!")
            
            cv2.imshow("Video", resizedFrame)
            cv2.imshow("Foreground Mask", mask)
            
            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        self.capture.release()
        cv2.destroyAllWindows()
        