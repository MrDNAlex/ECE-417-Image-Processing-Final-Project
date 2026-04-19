import os
from VideoProcessor import VideoProcessor
from VideoProcessorSettings import VideoProcessorSettings

# Define all the Settings
K = 3
alpha = 0.01
threshold = 0.7
width = 854
height = 480
resizeVideo = True
horizontalVideo = True
useMorphology = True
morphSize = 3
showComparison = True
showTracking = True

# Create the Settings Object
if horizontalVideo:
    settings = VideoProcessorSettings(K, alpha, threshold, width, height, resizeVideo, useMorphology, morphSize, showComparison, showTracking)
else:
    settings = VideoProcessorSettings(K, alpha, threshold, height, width, resizeVideo, useMorphology, morphSize, showComparison, showTracking)

# Create a Video Processor and run it
videoPath = os.path.join("Videos", "Traffic1.mp4")
processor = VideoProcessor(videoPath, settings, "TrafficOutput")

# Extract 10 mask frames to "CompiledImplementation_Frames" directory
#processor.extractFrames(10, "CompiledImplementation_Frames")

# Extract 10 raw video frames to "CompiledImplementation_RawFrames" directory
processor.extractRawFrames(10, "CompiledImplementation_RawFrames")

#processor.run()
#processor.saveData()
