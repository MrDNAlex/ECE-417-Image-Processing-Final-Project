import pandas as pd
import matplotlib.pyplot as plt

# Map out the resolutions to width x height
resourceMap = {
    "120p": "160x120",
    "240p": "426x240",
    "360p": "640x360",
    "480p": "854x480",
    "720p": "1280x720",
    "1080p": "1920x1080",
    "1440p": "2560x1440",
    "2160p": "3840x2160"
}

# Define our resolution splits
resSplits = {
    "LowRes": ["120p", "240p", "360p", "480p"],
    "HighRes": ["720p", "1080p", "1440p", "2160p"]
}

# Create a new dictionary to hold the numeric Total Pixels (width * height)
pixelMap = {}
for res, dim in resourceMap.items():
    width, height = dim.split('x')
    pixelMap[res] = int(width) * int(height)

# Keep a sorted list so our X-axis scales up properly
resourceOrder = list(resourceMap.keys())

sweeps = ["AlphaSweep", "KSweep", "MorphologySweep", "ThresholdSweep"]

for sweep in sweeps:
    fileName = f"Data-Processing\\Processed\\{sweep}-Summary.csv"
    
    try:
        df = pd.read_csv(fileName)
    except FileNotFoundError:
        print(f"Could not find {fileName}, skipping plot.")
        continue

    # Make the Resolution column categorical so it sorts by our defined order
    df['Resolution'] = pd.Categorical(df['Resolution'], categories=resourceOrder, ordered=True)
    
    # Create the numeric column for the log scale math
    df['Total_Pixels'] = df['Resolution'].map(pixelMap)

    # Sort the dataframe so the lines draw from left to right properly
    df = df.sort_values(['Parameter', 'Video', 'Resolution'])

    for video in df['Video'].unique():
        
        # Loop through our Low/High resolution splits
        for splitName, splitList in resSplits.items():
            
            # Filter data for this specific video AND this specific resolution group
            splitDF = df[(df['Video'] == video) & (df['Resolution'].isin(splitList))]
            
            if splitDF.empty:
                continue

            # Setup a figure with 1 row and 2 columns for THIS video and split
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
            fig.suptitle(f"Performance Metrics: {sweep} - {video} ({splitName})", fontsize=16)

            # Loop through each parameter to plot its curve
            for param in splitDF['Parameter'].unique():
                subset = splitDF[splitDF['Parameter'] == param]
                
                if not subset.empty:
                    xValues = subset['Total_Pixels']
                    curveLabel = param
                    
                    ax1.plot(xValues, subset['Average FPS'], marker='o', label=curveLabel)
                    ax2.plot(xValues, subset['Total Processing Time'], marker='s', label=curveLabel)

            # Get the matching pixels and labels JUST for this split so the axis is clean
            splitPixels = sorted([pixelMap[res] for res in splitList])
            splitLabels = splitList

            # Format the FPS Plot
            ax1.set_title(f"Average FPS vs Resolution")
            ax1.set_xlabel("Resolution (Log2)")
            ax1.set_ylabel("Average FPS")
            ax1.set_xscale('log', base=2)
            ax1.set_xticks(splitPixels)
            ax1.set_xticklabels(splitLabels, rotation=45)
            
            ax1.grid(True, linestyle='--', alpha=0.6)
            ax1.legend(fontsize='small')

            # Format the Compute Time Plot
            ax2.set_title(f"Total Processing Time vs Resolution")
            ax2.set_xlabel("Resolution (Log2)")
            ax2.set_ylabel("Processing Time (seconds)")            
            ax2.set_xscale('log', base=2)
            ax2.set_xticks(splitPixels)
            ax2.set_xticklabels(splitLabels, rotation=45)
            
            ax2.grid(True, linestyle='--', alpha=0.6)
            ax2.legend(fontsize='small')

            plt.tight_layout()
            outputFile = f"Data-Processing\\Processed\\Plots\\{sweep}_{video}_{splitName}_plot.png"
            plt.savefig(outputFile)
            print(f"Saved {outputFile}")
            
            plt.close()