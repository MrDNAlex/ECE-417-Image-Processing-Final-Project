import os
import glob
import pandas as pd

sweeps = ["AlphaSweep", "KSweep", "MorphologySweep", "ThresholdSweep"]

for sweep in sweeps:
    results = []
    
    # Create a search pattern to find all Timing.csv files in this sweep
    searchPath = os.path.join("Data-Processing", "Raw-Data", "Timing", sweep, "*", "*", "*", "Timing.csv")
    files = glob.glob(searchPath)

    for file in files:
        # Split the folder path to pull out the names
        parts = os.path.normpath(file).split(os.sep)
        
        parameterFolder = parts[4]
        resolution = parts[5]
        video = parts[6]

        try:
            # Read timing data
            df = pd.read_csv(file)
            
            avgFPS = df['FPS'].mean()
            totalGaussianTime = df['Gaussian Time (s)'].sum()
            totalTrackingTime = df['Tracking Time (s)'].sum()
            totalProcessingTime = df['Full Processing Time (s)'].sum()

            # Store the extracted values
            results.append({
                "Parameter": parameterFolder,
                "Resolution": resolution,
                "Video": video,
                "Average FPS": avgFPS,
                "Total Gaussian Time": totalGaussianTime,
                "Total Tracking Time": totalTrackingTime,
                "Total Processing Time": totalProcessingTime
            })
        except Exception as e:
            print(f"Could not read {file}: {e}")

    # Group the results and average them across the 5 traffic videos
    if results:
        resultsDF = pd.DataFrame(results)
        
        # Save to a clean CSV
        outputName = f"Data-Processing\\Processed\\{sweep}-Summary.csv"
        resultsDF.to_csv(outputName, index=False)
        print(f"Successfully saved {outputName}")