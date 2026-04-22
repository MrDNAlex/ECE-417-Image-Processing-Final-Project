import os
import pandas as pd

videoNames = ["Traffic1", "Traffic2", "Traffic3", "Traffic4", "Traffic5"]
framesCompared = [5, 10, 25, 50, 100, 250, 500]
desiredColumns = ["Resolution", "Traffic", "K", "A", "T", "M", "Frames Compared", "SSIM OpenCV AVG", "SSIM OpenCV Var", "SSIM OpenCV Med", "SSIM Otsu AVG", "SSIM Otsu Var", "SSIM Otsu Med"]

# Loop through all videos and Frames to compare
for video in videoNames:
    videoScores = []
    for frames in framesCompared:
        scorePath = os.path.join("Data-Processing", "Processed", "Scores", f"VideoScores-{video}-Comp{frames}.csv")
        
        # Make sure the file exists
        if (not os.path.exists(scorePath)):
            continue
        
        # Read the file and add athe Frames Compared Column
        df = pd.read_csv(scorePath)
        df["Frames Compared"] = frames
        
        videoScores.append(df)
            
    if len(videoScores) == 0:
        print("No files found")
        break
    
    # Merge the Files and Save to a CSV
    filePath = os.path.join("Data-Processing", "Processed", f"VideoScores-Merged-{video}.csv")
    mergedDataFrame = pd.concat(videoScores, ignore_index=True)
    mergedDataFrame.to_csv(filePath, index=False)
    print(f"Saved the Merged Data for {video} to {filePath}")
