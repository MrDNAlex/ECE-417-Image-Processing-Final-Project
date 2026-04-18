from VideoProcessor import VideoProcessor
from VideoProcessorSettings import VideoProcessorSettings

K = 3
alpha = 0.01
threshold = 0.7
width = 320
height = 240

# Create settings and add useOpenCV flag
settings = VideoProcessorSettings(K, alpha, threshold, width, height)
settings.useOpenCV = False  # Change to True to test OpenCV's MOG2 algorithm

print(f"Testing with OpenCV: {settings.useOpenCV}")

processor = VideoProcessor("Implementation/Data/Traffic1.mp4", settings)

processor.run()

