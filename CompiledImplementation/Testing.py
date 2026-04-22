import os
from VideoProcessorOpenCV import VideoProcessorOpenCV
from VideoProcessorSettings import VideoProcessorSettings

# Define all the Settings
K = 3
alpha = 0.01
threshold = 0.7
width = 854
height = 480
resizeVideo = False
horizontalVideo = True
useMorphology = True
morphSize = 3
showComparison = True
showTracking = False

# Create the Settings Object
if horizontalVideo:
    settings = VideoProcessorSettings(K, alpha, threshold, width, height, resizeVideo, useMorphology, morphSize, showComparison, showTracking)
else:
    settings = VideoProcessorSettings(K, alpha, threshold, height, width, resizeVideo, useMorphology, morphSize, showComparison, showTracking)

# Create a Video Processor and run it
videoPath = os.path.join("Videos", "Traffic1.mp4")
processor = VideoProcessorOpenCV(videoPath, settings, "TrafficOutput")

processor.run()
processor.saveData()
