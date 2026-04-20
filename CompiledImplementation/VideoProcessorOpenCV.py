import json
import os
import cv2
import time
import numpy as np
import pandas as pd
from OpenCVModel import OpenCVModel
from VideoProcessorSettings import VideoProcessorSettings
from Tracking import Tracker

class VideoProcessorOpenCV:

    folderName:str
    """Custom Name for the Folder to store the info into"""

    fileName:str
    """Name of the Video File Being Processed"""

    capture: cv2.VideoCapture
    """CV2 Video Stream"""
    
    subtractor : OpenCVModel
    """Compiled OpenCV Subtractor"""
    
    width:int
    """Width of the Video to Process"""
    
    height: int
    """Height of the Video to Process"""
    
    showComparisonWindow: bool
    """Boolean Toggle for showing the OpenCV Window to view the comparison"""
    
    settings:VideoProcessorSettings
    """Settings for the Video Processor"""
    
    timingData: pd.DataFrame
    """Dataframe to store the timing info for the Video Processor"""
    
    subtractorVideo: cv2.VideoWriter
    """Video Writer for the Raw Subtraction Mask"""
    
    comparisonVideo: cv2.VideoWriter
    """Video Writer for the Comparison of the Raw Video and Subtraction Mask"""
    
    def __init__(self, videoPath: str, settings : VideoProcessorSettings, folderName: str):
        
        self.folderName = folderName
        self.fileName = os.path.basename(videoPath).split(".")[0]
        self.capture = cv2.VideoCapture(videoPath)
        
        # Test that we can open the Video
        returned, frame = self.capture.read()
        if not returned:
            print("Error Reading the Video")
            return
        
        # Assign Processor Settings
        self.settings = settings
        self.width = int(settings.width)
        self.height = int(settings.height)
        
        # Initialize the OpenCV Model
        self.subtractor = OpenCVModel(settings)
        
        # Initialize Benchmarking info
        self.timingData = pd.DataFrame(columns=["Frame Index", "FPS", "Gaussian Time (s)", "Tracking Time (s)", "Full Processing Time (s)"])
        
        # Reset video back to first frame
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        self.tracker = Tracker()
        
    def run(self):
        """Runs the Background Subtractor on the Video until it is done"""
        
        frameIndex = 0
        totalFrames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        FPS = int(self.capture.get(cv2.CAP_PROP_FPS))
        folderPath: str = f"Cache/{self.folderName}"
        
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        
        subtractorVideoSource = cv2.VideoWriter_fourcc(*'mp4v')
        self.subtractorVideo = cv2.VideoWriter(os.path.join(folderPath, f"{self.fileName}-Mask.mp4"), subtractorVideoSource, FPS, (self.width, self.height))
        self.comparisonVideo = cv2.VideoWriter(os.path.join(folderPath, f"{self.fileName}-Comparison.mp4"), subtractorVideoSource, FPS, (self.width * 2, self.height))
        
        while True:
            
            startTimeRaw = time.perf_counter()
            
            # Extract a single frame
            returned, frame = self.capture.read()
            if not returned:
                print("Video finished.")
                break
            
            # Resize the Video if needed
            if (self.settings.resizeVideo):
                frame = cv2.resize(frame, (self.width, self.height))
                
            startTimeProcessing = time.perf_counter()
            
            # Apply the Background Subtractor 
            mask = self.subtractor.apply(frame)
            
            deltaT = time.perf_counter() - startTimeProcessing
            fps = 1.0 / (deltaT)
            completion = frameIndex / totalFrames * 100
            print(f"Finished Frame! FPS: {fps:.2f} {completion:.2f}%")
            
            
            startTimeTracking = time.perf_counter()
            
            _, currentInstances = self.tracker.processMask(mask, frameIndex, float(frameIndex)/FPS)
            
            deltaTTracking = time.perf_counter() - startTimeTracking
            
            # Convert the image to BGR Space so that it can be combined next to raw video
            maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            combinedView = np.hstack((frame, maskBGR))
            
            # Print FPS to terminal to see the difference
            if self.settings.showComparisonWindow:
                if self.settings.showObjectTracking:
                    for instance in currentInstances:
                        x = int(instance.X)
                        y = int(instance.Y)
                        w = int(instance.width)
                        h = int(instance.height)
                        
                        offsetX = x + self.width
                        
                        cv2.rectangle(combinedView, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(combinedView, f"ID: {instance.uID}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        
                        cv2.rectangle(combinedView, (offsetX, y), (offsetX + w, y + h), (0, 255, 0), 2)
                        cv2.putText(combinedView, f"ID: {instance.uID}", (offsetX, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                cv2.putText(combinedView, f"FPS: {fps:.2f}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                cv2.imshow("Video", combinedView)
            
            self.subtractorVideo.write(maskBGR)
            self.comparisonVideo.write(combinedView)
            
            delatTRaw = time.perf_counter() - startTimeRaw
            
            frameIndex += 1
            self.timingData.loc[len(self.timingData)] = [frameIndex, fps, deltaT, deltaTTracking,  delatTRaw]
            
            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the content
        self.capture.release()
        
        if self.settings.showComparisonWindow:
            cv2.destroyAllWindows()
            
    def saveData(self):
        
        folderPath: str = f"Cache/{self.folderName}"
        
        self.subtractorVideo.release()
        self.comparisonVideo.release()
        
        self.timingData.to_csv(os.path.join(folderPath, "Timing.csv"), index=False)
        self.settings.getCSV().to_csv(os.path.join(folderPath, "Settings.csv"), index=False)
        
        data:json = []
        for seq in self.tracker.sequences:
            data.append(seq.getJSON())
            
        with open(os.path.join(folderPath, "Tracking.json"), 'w') as f:
            json.dump(data, f, indent=4)
        
    def extractFrames(self, numFrames: int, outputDir: str):
        """
        Extract a specified number of frames from the video and save them as images.
        """
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
            if self.settings.resizeVideo:
                frame = cv2.resize(frame, (self.width, self.height))
            
            # Apply background subtractor to get the mask
            mask = self.subtractor.apply(frame)
            
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
        """
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