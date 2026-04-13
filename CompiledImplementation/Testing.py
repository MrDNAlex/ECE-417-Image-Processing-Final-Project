from VideoProcessor import VideoProcessor
from VideoProcessorSettings import VideoProcessorSettings

K = 3
alpha = 0.01
threshold = 0.7
width = 854
height = 480

useMorphology = True
morphSize = 3
horizontalVideo = True

if horizontalVideo:
    settings = VideoProcessorSettings(K, alpha, threshold, width, height, useMorphology, morphSize)
else:
    settings = VideoProcessorSettings(K, alpha, threshold, height, width, useMorphology, morphSize)

processor = VideoProcessor("Implementation/Data/Universal.mp4", settings)

processor.run()

