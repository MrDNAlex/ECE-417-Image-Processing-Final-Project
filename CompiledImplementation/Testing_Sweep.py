import os
from VideoProcessor import VideoProcessor
from VideoProcessorSettings import VideoProcessorSettings

# Define all the Settings
K = [2,3,4,5]
alpha = [0.001, 0.01, 0.1]
threshold = [0.5, 0.6, 0.7, 0.8]
width = 854
height = 480
resizeVideo = True
horizontalVideo = True
useMorphology = True
morphSize = [3, 4, 5]
showComparison = True
showTracking = True

VideoFolder = "Videos"
ResFolder = ["120p", "240p", "360p", "480p"]
VideosNames = ["Traffic1.mp4", "Traffic2.mp4", "Traffic3.mp4", "Traffic4.mp4", "Traffic5.mp4"]


for res in ResFolder:
    for video in VideosNames:
        for k in K:
            for a in alpha:
                for t in threshold:
                    if horizontalVideo:
                        settings = VideoProcessorSettings(k, a, t, width, height, resizeVideo, useMorphology, morphSize, showComparison, showTracking)
                    else:
                        settings = VideoProcessorSettings(k, a, t, height, width, resizeVideo, useMorphology, morphSize, showComparison, showTracking)
                        
                    processor = VideoProcessor(os.path.join(VideoFolder, res, video), settings, os.path.join(res, video[:-4], f"K{k}/A{a}_/T{t}"))
                    processor.run()
                    processor.saveData()


