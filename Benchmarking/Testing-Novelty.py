import sys
import os
import pandas as pd

# Adds the parent directory to the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CompiledImplementation.SecurityCameraProcessor import SecurityCameraProcessor
from CompiledImplementation.VideoProcessorSettings import VideoProcessorSettings

def ExtractSettings(df: pd.DataFrame) -> list[tuple]:
    """
    Returns a list of tuples containing:
    (VideoProcessorSettings, video_filename, resolution_string)
    """
    SettingsAndVideos = []
    
    # Define resolutions matching the reference style
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

    for index, row in df.iterrows():
        
        # Clean and convert the string variables to numbers
        category = int(str(row['Category']).split("-")[0].strip())
        KVal = int(str(row['K']).replace('K', ''))
        alphaVal = float(str(row['A']).replace('A', '').replace('_', ''))
        thresholdVal = float(str(row['T']).replace('T', ''))
        morphSizeVal = int(str(row['M']).replace('M', ''))
        
        # Get the resolutions
        resolutionString = str(row['Resolution'])
        widthVal = resolutionsX[resolutionString]
        heightVal = resolutionsY[resolutionString]
        
        # Get the Video name
        videoName = str(row.get('Traffic Video', row.get('Traffic', 'Traffic1')))
        videoFileName = f"{videoName}.mp4"
        
        # Define constant and conditional settings
        resizeVideo = False
        horizontalVideo = True
        showComparison = False
        showTracking = False
        
        if morphSizeVal == 0:
            useMorphology = False
        else:
            useMorphology = True
        
        # Create the Settings
        if horizontalVideo:
            setting = VideoProcessorSettings(KVal, alphaVal, thresholdVal, widthVal, heightVal, resizeVideo, useMorphology, morphSizeVal, showComparison, showTracking)
        else:
            setting = VideoProcessorSettings(KVal, alphaVal, thresholdVal, heightVal, widthVal, resizeVideo, useMorphology, morphSizeVal, showComparison, showTracking)
            
        # Create the name
        setting.name = f"Category-{category}\\{resolutionString}\\K-{KVal}\\A-{alphaVal}\\T-{thresholdVal}\\M-{morphSizeVal}"
        
        # Add the tuple to my array
        SettingsAndVideos.append((setting, videoFileName, resolutionString))
        
    return SettingsAndVideos

bestSettingsFile = ["Best-OpenCV-Settings.csv", "Best-Otsu-Settings.csv", "TipTop-Summary-OpenCV.csv",  "TipTop-Summary-Otsu.csv"]

try:
    index = int(sys.argv[1])
except (IndexError, ValueError):
    print("Error: Please provide a valid integer index.")
    sys.exit(1)

# Load the DataFrame
csvPath = os.path.join("Data-Processing", "Processed", bestSettingsFile[index])
df = pd.read_csv(csvPath)

# Generate the array of settings and associated videos
videoSettings = ExtractSettings(df)

# Loop through each extracted setting and run it on its matched video
for setting, video, res in videoSettings:
    print(f"Running : {setting.name} on {video}")
    
    # Create the path dynamically using the matched resolution and video
    videoPath = os.path.join("Videos", res, video)
    
    # Create a Video Processor and run it
    processor = SecurityCameraProcessor(videoPath, setting, os.path.join(bestSettingsFile[index].split(".")[0], setting.name) + f"\\{video.split('.')[0]}")

    processor.run()
    processor.saveData()