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
        
        self.subtractor = BackgroundSubtractor(settings)
        
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    def run(self):
        while True:
            returned, frame = self.capture.read()
            if not returned:
                print("Video finished.")
                break
            
            startTime = time.time()
            
            resizedFrame = cv2.resize(frame, (self.width, self.height))
            
            mask = self.subtractor.apply(resizedFrame)
            
            fps = 1.0 / (time.time() - startTime)
            
            # Print FPS to terminal to see the difference
            print(f"Finished Frame! FPS: {fps:.2f}")
            
            cv2.imshow("Video", resizedFrame)
            cv2.imshow("Foreground Mask", mask)
            
            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        self.capture.release()
        cv2.destroyAllWindows()
    
    def extractFrames(self, numFrames: int, outputDir: str):
        """
        Extract a specified number of frames from the video and save them as images.
        
        Args:
            numFrames: Number of frames to extract
            outputDir: Directory path to save the extracted frames
        """
        import os
        
        # Create output directory if it doesn't exist
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        
        # Calculate frame interval to evenly distribute extractions
        totalFrames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = max(1, totalFrames // numFrames)
        
        # Reset to beginning
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        frameIndex = 0
        extracted = 0
        
        while extracted < numFrames:
            returned, frame = self.capture.read()
            if not returned:
                break
            
            # Resize if needed
            resizedFrame = cv2.resize(frame, (self.width, self.height))
            
            # Apply background subtractor to get the mask
            mask = self.subtractor.apply(resizedFrame)
            
            # Save frame at calculated intervals
            if frameIndex % interval == 0:
                filename = f"frame_{extracted:04d}.jpg"
                filepath = os.path.join(outputDir, filename)
                cv2.imwrite(filepath, mask)
                extracted += 1
                print(f"Extracted frame {extracted}/{numFrames}: {filename}")
            
            frameIndex += 1
        
        # Reset video to beginning for other operations
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        print(f"Extracted {extracted} frames to {outputDir}")
    
    def extractRawFrames(self, numFrames: int, outputDir: str):
        """
        Extract raw video frames (without processing) at evenly distributed intervals.
        
        Args:
            numFrames: Number of frames to extract
            outputDir: Directory path to save the extracted frames
        """
        import os
        
        # Create output directory if it doesn't exist
        if not os.path.exists(outputDir):
            os.makedirs(outputDir)
        
        # Calculate frame interval to evenly distribute extractions
        totalFrames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        interval = max(1, totalFrames // numFrames)
        
        # Reset to beginning
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        frameIndex = 0
        extracted = 0
        
        while extracted < numFrames:
            returned, frame = self.capture.read()
            if not returned:
                break
            
            # Save frame at calculated intervals (no processing)
            if frameIndex % interval == 0:
                filename = f"frame_{extracted:04d}.jpg"
                filepath = os.path.join(outputDir, filename)
                cv2.imwrite(filepath, frame)
                extracted += 1
                print(f"Extracted raw frame {extracted}/{numFrames}: {filename}")
            
            frameIndex += 1
        
        # Reset video to beginning for other operations
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        print(f"Extracted {extracted} raw frames to {outputDir}")
        