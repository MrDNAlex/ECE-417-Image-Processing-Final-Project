import os
import glob
import pandas as pd

def ProcessCompressionSizes():
    results = []
    
    # Create a recursive search pattern matching the new folder structure
    searchPath = os.path.join("Data-Processing", "Raw-Data", "Compression", "**", "*p", "K-*", "A-*", "T-*", "M-*", "Traffic*", "*-Compressed.mp4")
    
    print(f"Scanning for files matching: {searchPath}")
    files = glob.glob(searchPath, recursive=True)

    # Loop through every video found
    for file in files:
        # Split the folder path to pull out the names
        parts = os.path.normpath(file).split(os.sep)
        
        try:
            # Pulling from the back ensures we get the right folders exactly as generated
            compressedFile = parts[-1]        # e.g., Traffic1-Compressed.mp4
            trafficFolder = parts[-2]         # e.g., Traffic1
            mFolder = parts[-3]               # e.g., M-5
            tFolder = parts[-4]               # e.g., T-0.9
            aFolder = parts[-5]               # e.g., A-0.01
            kFolder = parts[-6]               # e.g., K-3
            resolutionFolder = parts[-7]      # e.g., 480p
            category = parts[-8]
            refreshIndex = parts[-9].removeprefix("Ref")
            objDetect = parts[-10].removeprefix("ObjDetect")
            bestSettingCategory = parts[-11]        # e.g., TipTop-Summary-OpenCV

            # Create the Raw Video Path
            rawFile = file.replace("-Compressed.mp4", "-Raw.mp4")
            
            # Get file sizes in bytes
            compressedSize = os.path.getsize(file) if os.path.exists(file) else 0
            rawSize = os.path.getsize(rawFile) if os.path.exists(rawFile) else 0

            # Store the extracted values (cleaning the text for the CSV)
            results.append({
                "Best Settings Category": bestSettingCategory,
                "Category": category,
                "Use Object Detection": objDetect,
                "Refresh Index": refreshIndex,
                "Resolution": resolutionFolder,
                "Traffic Video": trafficFolder,
                "K": kFolder.replace("K-", ""),
                "A": aFolder.replace("A-", ""),
                "T": tFolder.replace("T-", ""),
                "M": mFolder.replace("M-", ""),
                "Raw Size (Bytes)": rawSize,
                "Compressed Size (Bytes)": compressedSize
            })
            
        except IndexError as e:
            print(f"Path structure didn't match expectations for {file}: {e}")

    # Save the mapped combinations
    if results:
        resultsDF = pd.DataFrame(results)
        
        # Ensure the output directory exists
        outputFolder = os.path.join("Data-Processing", "Processed")
        os.makedirs(outputFolder, exist_ok=True)
        
        # Save to a clean CSV
        outputName = os.path.join(outputFolder, "Compression-Sizes-Merged.csv")
        resultsDF.to_csv(outputName, index=False)
        print(f"Successfully processed {len(results)} videos and saved to {outputName}")
    else:
        print("No files matched the search path. Please ensure the script is run in the correct root directory.")

if __name__ == "__main__":    
    ProcessCompressionSizes()