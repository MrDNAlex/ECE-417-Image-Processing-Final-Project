from VideoProcessor import VideoProcessor
from VideoProcessorSettings import VideoProcessorSettings

K = 3
alpha = 0.01
threshold = 0.7
width = 320
height = 240

settings = VideoProcessorSettings(K, alpha, threshold, width, height)

processor = VideoProcessor("Implementation/Data/Traffic Video.mkv", settings)

processor.run()

