import sys
import os

# Adds the parent directory to the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CompiledImplementation.SecurityCameraProcessor import SecurityCameraProcessor
from CompiledImplementation.VideoProcessorSettings import VideoProcessorSettings

# Define all the Settings
K = 3
alpha = 0.01
threshold = 0.9
width = 852
height = 480
resizeVideo = False
horizontalVideo = True
useMorphology = True
morphSize = 9
showComparison = True
showTracking = False

# Create the Settings Object
if horizontalVideo:
    settings = VideoProcessorSettings(K, alpha, threshold, width, height, resizeVideo, useMorphology, morphSize, showComparison, showTracking)
else:
    settings = VideoProcessorSettings(K, alpha, threshold, height, width, resizeVideo, useMorphology, morphSize, showComparison, showTracking)

VideosNames = ["Traffic1.mp4", "Traffic2.mp4", "Traffic3.mp4", "Traffic4.mp4", "Traffic5.mp4"]

for video in VideosNames:
    # Create a Video Processor and run it
    videoPath = os.path.join("Videos", "480p", video)
    processor = SecurityCameraProcessor(videoPath, settings, video.split(".")[0])

    processor.run()
    processor.saveData()
