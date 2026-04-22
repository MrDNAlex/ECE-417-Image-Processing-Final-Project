import os
import sys
import cv2
import numpy as np
import pandas as pd
from skimage.metrics import structural_similarity

def extractFrames(videoPath, numFrames):
    # Open the video file
    cap = cv2.VideoCapture(videoPath)
    if not cap.isOpened():
        print("Didn't Open")
        return []
    
    # Extract total Number of Frames
    totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if totalFrames == 0:
        print("Failed to Extract")
        return []
        
    # Calculate the Frames indexes
    frameIndices = np.linspace(0, totalFrames - 1, numFrames, dtype=int)
    frames = []
    
    for idx in frameIndices:
        # Jump to the specific frame index
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        
        if ret:
            # Convert to grayscale because SSIM works best on 2D image arrays
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frames.append(gray)
            
    cap.release()
    return frames

def calculateSSIM(framesA, framesB):
    # Make sure we have valid frames to compare
    if not framesA or not framesB or len(framesA) != len(framesB):
        print("Wrong Dimensions")
        return (0.0, 0.0)
        
    scores = []
    
    # Compare each matching pair of frames side-by-side
    for fA, fB in zip(framesA, framesB):
        score, _ = structural_similarity(fA, fB, full=True)
        scores.append(score)
    
    return (np.average(scores), np.var(scores), np.median(scores))

def evaluateVideoSimilarities(csvPath, numFrames=10):

    df = pd.read_csv(csvPath)
    
    opencvScoresAvg = []
    otsuScoresAvg = []
    opencvScoresVar = []
    otsuScoresVar = []
    opencvScoresMed = []
    otsuScoresMed = []
    
    # Loop through every row in the dataframe
    for index, row in df.iterrows():
        paramSweepPath = row['ParamSweep Path']
        opencvPath = row['OpenCV Path']
        otsuPath = row['Otsu Path']
        
        # Check if the Gigi file actually exists before trying to read it
        if not os.path.exists(paramSweepPath):
            print(f"Missing video: {paramSweepPath}")
            opencvScoresAvg.append(0.0)
            opencvScoresVar.append(0.0)
            otsuScoresAvg.append(0.0)
            otsuScoresVar.append(0.0)
            continue
            
        # Extract the evenly spaced frames
        paramSweepFrames = extractFrames(paramSweepPath, numFrames)
        opencvFrames = extractFrames(opencvPath, numFrames)
        otsuFrames = extractFrames(otsuPath, numFrames)
        
        # Calculate the average SSIM for this video combination
        scoreOpenCVAvg, scoreOpenCVVar, scoreOpenCVMed = calculateSSIM(paramSweepFrames, opencvFrames)
        scoreOtsuAvg, scoreOtsuVar, scoreOtsuMed = calculateSSIM(paramSweepFrames, otsuFrames)
        
        opencvScoresAvg.append(round(scoreOpenCVAvg, 4))
        opencvScoresVar.append(round(scoreOpenCVVar, 4))
        opencvScoresMed.append(round(scoreOpenCVMed, 4))
        otsuScoresAvg.append(round(scoreOtsuAvg, 4))
        otsuScoresVar.append(round(scoreOtsuVar, 4))
        otsuScoresMed.append(round(scoreOtsuMed, 4))
        
        print(f"Processed row {index + 1}/{len(df)} - OpenCV: (Avg : {scoreOpenCVAvg:.4f}, Var: {scoreOpenCVVar:.4f}, Med:{scoreOpenCVMed:.4f}), Otsu: (Avg : {scoreOtsuAvg:.4f}, Var: {scoreOtsuVar:.4f}, Med: {scoreOtsuMed:.4f})")
        
    # Add the scores back into the dataframe as new columns
    df['SSIM OpenCV AVG'] = opencvScoresAvg
    df['SSIM OpenCV Var'] = opencvScoresVar
    df['SSIM OpenCV Med'] = opencvScoresMed
    df['SSIM Otsu AVG'] = otsuScoresAvg
    df['SSIM Otsu Var'] = otsuScoresVar
    df['SSIM Otsu Med'] = otsuScoresMed
    
    # Save the final results to a new CSV
    outputPath = f"Data-Processing\\Processed\\VideoScores-{os.path.basename(csvPath).split('.')[0].split('-')[1]}-Comp{framesToCompare}.csv"
    df.to_csv(outputPath, index=False)
    print(f"\nSuccessfully saved all scores to {outputPath}")

if __name__ == "__main__":
    
    try:
        fileName = os.path.join("Data-Processing", "Processed", sys.argv[1])
        framesToCompare = int(sys.argv[2])
    except (IndexError, ValueError):
        print("Error: Please provide a valid integer index.")
        sys.exit(1)
    
    if os.path.exists(fileName):
        evaluateVideoSimilarities(fileName, framesToCompare)
    else:
        print(f"Could not find the input CSV at: {fileName}")