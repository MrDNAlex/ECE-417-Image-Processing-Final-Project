import sys
import os

# Adds the parent directory to the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CompiledImplementation.VideoProcessorOtsu import VideoProcessorOtsu
from CompiledImplementation.VideoProcessorSettings import VideoProcessorSettings

# Define all the Settings
K = 3
alpha = 0.01
threshold = 0.7
width = 854
height = 480
resizeVideo = False
horizontalVideo = True
useMorphology = True
morphSize = [3, 4, 5]
showComparison = False
showTracking = False

VideoFolder = "Videos"
ResFolder = ["120p", "240p", "360p", "480p"]
VideosNames = ["Traffic1.mp4", "Traffic2.mp4", "Traffic3.mp4", "Traffic4.mp4", "Traffic5.mp4"]

resolutionsX = {
    "120p" : 160,
    "240p" : 426,
    "360p" : 640,
    "480p" : 852,
    "720p" : 1280,
    "1080p" : 1920,
    "1440p" : 2560,
    "2160p" : 3840
}

resolutionsY = {
    "120p" : 120,
    "240p" : 240,
    "360p" : 360,
    "480p" : 480,
    "720p" : 720,
    "1080p" : 1080,
    "1440p" : 1440,
    "2160p" : 2160
}

for res in ResFolder:
    for video in VideosNames:
        for m in morphSize:

            # Create the Settings Object
            if horizontalVideo:
                settings = VideoProcessorSettings(K, alpha, threshold, width, height, resizeVideo, useMorphology, m, showComparison, showTracking)
            else:
                settings = VideoProcessorSettings(K, alpha, threshold, height, width, resizeVideo, useMorphology, m, showComparison, showTracking)

            settings.width = resolutionsX[res]
            settings.height = resolutionsY[res]

            # Create a Video Processor and run it
            processor = VideoProcessorOtsu(os.path.join(VideoFolder, res, video), settings, os.path.join("Otsu", f"M{m}", res, video[:-4]))
            processor.run()
            processor.saveData()
