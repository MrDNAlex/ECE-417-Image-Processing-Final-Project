import sys
import os

# Adds the parent directory to the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CompiledImplementation.VideoProcessorSettings import VideoProcessorSettings
from CompiledImplementation.VideoProcessor import VideoProcessor

def RunLowResSweep(settings: list[VideoProcessorSettings]):
    resolutionsX = {
        "120p" : 160,
        "240p" : 426,
        "360p" : 640,
        "480p" : 852,
    }
    
    resolutionsY = {
        "120p" : 120,
        "240p" : 240,
        "360p" : 360,
        "480p" : 480,
    }
    
    videos = ["Traffic1.mp4", "Traffic2.mp4", "Traffic3.mp4", "Traffic4.mp4", "Traffic5.mp4"]
    
    for res in resolutionsX.keys():
        for setting in settings:
            cloneSettings = setting.clone()
            
            cloneSettings.width = resolutionsX[res]
            cloneSettings.height = resolutionsY[res]
            cloneSettings.name = cloneSettings.name + f"\\{res}"
            
            for vid in videos:
                print(f"Running : {cloneSettings.name}")
                vidProcessor = VideoProcessor(os.path.join("Videos", res, vid), cloneSettings, cloneSettings.name + f"\\{vid.split('.')[0]}")
                vidProcessor.run()
                vidProcessor.saveData()

def RunHighResSweep(settings: list[VideoProcessorSettings], index):
    
    resolutionsX = {
        "720p" : 1280,
        "1080p" : 1920,
        #"1440p" : 2560,
        #"2160p" : 3840
    }
    
    resolutionsY = {
        "720p" : 720,
        "1080p" : 1080,
        #"1440p" : 1440,
        #"2160p" : 2160
    }
    
    videos = ["Traffic1.mp4", "Traffic2.mp4", "Traffic3.mp4", "Traffic4.mp4", "Traffic5.mp4"]
    
    for res in resolutionsX.keys():
        for setting in settings:
            cloneSettings = setting.clone()
            
            cloneSettings.width = resolutionsX[res]
            cloneSettings.height = resolutionsY[res]
            cloneSettings.name = cloneSettings.name + f"\\{res}"
            
            print(f"Running : {cloneSettings.name}")
            vidProcessor = VideoProcessor(os.path.join("Videos", res, videos[index]), cloneSettings, cloneSettings.name + f"\\{videos[index].split('.')[0]}")
            vidProcessor.run()
            vidProcessor.saveData()
        
# Define all the Base Settings
K = 2
alpha = 0.01
threshold = 0.7
width = 854
height = 480
resizeVideo = False
horizontalVideo = True
useMorphology = True
morphSize = 3
showComparison = False
showTracking = False

BASE_SETTINGS = VideoProcessorSettings(K, alpha, threshold, width, height, resizeVideo, useMorphology, morphSize, showComparison, showTracking)

def KSweep(highRes: bool, index: int):
    Settings = []
    KVals = [1, 2, 3, 4]
    
    for ks in KVals:
        baseClone = BASE_SETTINGS.clone()
        baseClone.K = ks
        baseClone.name = f"KSweep\\K-{ks}"
        Settings.append(baseClone)
    
    if not highRes:
        RunLowResSweep(Settings)
    else:
        RunHighResSweep(Settings, index)

def AlphaSweep(highRes: bool, index: int):
    Settings = []
    Alphas = [0.5, 0.1, 0.01, 0.001]
    
    for alpha in Alphas:
        baseClone = BASE_SETTINGS.clone()
        baseClone.alpha = alpha
        baseClone.name = f"AlphaSweep\\Alpha-{alpha}"
        Settings.append(baseClone)
    
    if not highRes:
        RunLowResSweep(Settings)
    else:
        RunHighResSweep(Settings, index)

def ThresholdSweep(highRes: bool, index: int):
    Settings = []
    Thresholds = [0.3, 0.5, 0.7, 0.9]
    
    for thresh in Thresholds:
        baseClone = BASE_SETTINGS.clone()
        baseClone.threshold = thresh
        baseClone.name = f"ThresholdSweep\\Thresh-{thresh}"
        Settings.append(baseClone)
    
    if not highRes:
        RunLowResSweep(Settings)
    else:
        RunHighResSweep(Settings, index)

def MorphologySweep(highRes: bool, index: int):
    Settings = []
    MorphologySize = [0, 3, 5, 7]
    
    for morph in MorphologySize:
        baseClone = BASE_SETTINGS.clone()
        
        if morph == 0:
            baseClone.useMorphology = False
        else:
            baseClone.useMorphology = True
            
        baseClone.morphologySize = morph
        baseClone.name = f"MorphologySweep\\Morph-{morph}"
        Settings.append(baseClone)
    
    if not highRes:
        RunLowResSweep(Settings)
    else:
        RunHighResSweep(Settings, index)

try:
    index = int(sys.argv[1])
    highRes = int(sys.argv[2])
    highResIndex = int(sys.argv[3])
except (IndexError, ValueError):
    print("Error: Please provide a valid integer index.")
    sys.exit(1)
    
    
if index == 1:
    print("Running KSweep")
    if highRes == 0:
        KSweep(False, highResIndex)
    else:
        KSweep(True, highResIndex)
        
if index == 2:
    print("Running AlphaSweep")
    if highRes == 0:
        AlphaSweep(False, highResIndex)
    else:
        AlphaSweep(True, highResIndex)
        
if index == 3:
    print("Running ThreshSweep")
    if highRes == 0:
        ThresholdSweep(False, highResIndex)
    else:
        ThresholdSweep(True, highResIndex)
        
if index == 4:
    print("Running MorphologySweep")
    if highRes == 0:
        MorphologySweep(False, highResIndex)
    else:
        MorphologySweep(True, highResIndex)
