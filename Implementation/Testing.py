from VideoProcessor import VideoProcessor
from VideoProcessorSettings import VideoProcessorSettings

K = 3
alpha = 0.01
threshold = 0.7
width = 854
height = 480

# Create settings and add useOpenCV flag
settings = VideoProcessorSettings(K, alpha, threshold, width, height)
settings.useOpenCV = False  # Change to True to test OpenCV's MOG2 algorithm
settings.useOtsu = True     # Change to True to test Otsu's binarization method

print(f"Testing with OpenCV: {settings.useOpenCV}, useOtsu: {settings.useOtsu}")

processor = VideoProcessor("Implementation/Data/Traffic1.mp4", settings)

# Extract 10 mask frames to "Implementation_Frames" directory
#processor.extractFrames(10, "Frames_otsu")

# Extract 10 raw video frames to "Implementation_RawFrames" directory
#processor.extractRawFrames(10, "Implementation_RawFrames")

processor.run()

