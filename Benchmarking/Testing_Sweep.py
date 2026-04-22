import sys
import os

# Adds the parent directory to the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CompiledImplementation.VideoProcessor import VideoProcessor
from CompiledImplementation.VideoProcessorSettings import VideoProcessorSettings

# Define all the Settings
K = [2,3,4]
alpha = [0.001, 0.01, 0.1]
threshold = [0.5, 0.7, 0.9]
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

def RunVideoSweep(video: str):
    for res in ResFolder:
        for k in K:
            for a in alpha:
                for t in threshold:
                    for m in morphSize:
                        if horizontalVideo:
                            settings = VideoProcessorSettings(k, a, t, width, height, resizeVideo, useMorphology, m, showComparison, showTracking)
                        else:
                            settings = VideoProcessorSettings(k, a, t, height, width, resizeVideo, useMorphology, m, showComparison, showTracking)
                            
                        settings.width = resolutionsX[res]
                        settings.height = resolutionsY[res]
                            
                        processor = VideoProcessor(os.path.join(VideoFolder, res, video), settings, os.path.join(res, video[:-4], f"K{k}/A{a}_/T{t}/M{m}"))
                        processor.run()
                        processor.saveData()
                        print("Finished Video")

try:
    index = int(sys.argv[1])
except (IndexError, ValueError):
    print("Error: Please provide a valid integer index.")
    sys.exit(1)
    
print(VideosNames[index])

RunVideoSweep(VideosNames[index])


