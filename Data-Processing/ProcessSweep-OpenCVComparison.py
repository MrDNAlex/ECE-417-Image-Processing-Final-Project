import os
import glob
import pandas as pd

def processVideoComparisonCSV():
    results = []
    
    # Define the resolutions to compare
    maxResolution = ['120p', '240p', '360p', '480p']
    
    # Create a search pattern to find all Mask videos
    searchPath = os.path.join("Data-Processing", "Raw-Data", "Param-Sweep", "*", "Traffic*", "K*", "A*", "T*", "M*", "*-Mask.mp4")
    files = glob.glob(searchPath)

    for file in files:
        # Split the folder path to pull out the names
        parts = os.path.normpath(file).split(os.sep)
        
        try:
            # Pulling from the back ensures we get the right folders regardless of the root path length
            video = parts[-1]
            mFolder = parts[-2]
            tFolder = parts[-3]
            aFolder = parts[-4]
            kFolder = parts[-5]
            trafficFolder = parts[-6]
            resolutionFolder = parts[-7]
            morphNumber = mFolder.replace("M", "")
            
            if resolutionFolder not in maxResolution:
                continue

            # Set baseline paths assuming OpenCV and otsu directories live at the root
            opencvPath = os.path.join("Data-Processing", "Raw-Data", "OpenCV", f"M{morphNumber}", resolutionFolder, trafficFolder, f"{trafficFolder}-Mask.mp4")
            otsuPath = os.path.join("Data-Processing", "Raw-Data", "Otsu", f"M{morphNumber}", resolutionFolder, trafficFolder, f"{trafficFolder}-Mask.mp4")

            # Store the extracted values
            results.append({
                "Resolution": resolutionFolder,
                "Traffic": trafficFolder,
                "K": kFolder,
                "A": aFolder,
                "T": tFolder,
                "M": mFolder,
                "ParamSweep Path": file,
                "OpenCV Path": opencvPath,
                "Otsu Path": otsuPath
            })
            
        except IndexError as e:
            print(f"Path structure didn't match expectations for {file}: {e}")

    # Save the mapped combinations
    if results:
        resultsDF = pd.DataFrame(results)
        
        # Save to a clean CSV
        outputName = "Data-Processing\\Processed\\VideoComparison.csv"
        resultsDF.to_csv(outputName, index=False)
        print(f"Successfully saved {outputName}")
    else:
        print("No files matched the search path.")

if __name__ == "__main__":
    processVideoComparisonCSV()