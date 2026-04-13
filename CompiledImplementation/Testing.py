from VideoProcessor import VideoProcessor
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
showComparison = False

# Create the Settings Object
if horizontalVideo:
    settings = VideoProcessorSettings(K, alpha, threshold, width, height, resizeVideo, useMorphology, morphSize, showComparison)
else:
    settings = VideoProcessorSettings(K, alpha, threshold, height, width, resizeVideo, useMorphology, morphSize, showComparison)

# Create a Video Processor and run it
processor = VideoProcessor("Videos/Traffic.mp4", settings)
processor.run()
