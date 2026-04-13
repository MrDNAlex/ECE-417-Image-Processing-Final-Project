from VideoProcessor import VideoProcessor
from VideoProcessorSettings import VideoProcessorSettings

K = 4
alpha = 0.01
threshold = 0.7
width = 854
height = 480
useMorphology = True

settings = VideoProcessorSettings(K, alpha, threshold, width, height, useMorphology)

processor = VideoProcessor("Implementation/Data/Traffic.mp4", settings)

processor.run()

