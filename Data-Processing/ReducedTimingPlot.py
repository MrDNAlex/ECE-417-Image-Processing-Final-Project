import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Create a Resources Map
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

# Organize the data by total resoltion and order it
pixelMap = {}
for res, dim in resourceMap.items():
    width, height = dim.split('x')
    pixelMap[res] = int(width) * int(height)

resourceOrder = list(resourceMap.keys())
sweeps = ["AlphaSweep", "KSweep", "MorphologySweep", "ThresholdSweep"]

# Define the shapes for plotting
videoMarkers = {
    "Traffic1": "o", # Circle
    "Traffic2": "s", # Square
    "Traffic3": "^", # Triangle pointing up
    "Traffic4": "D", # Diamond
    "Traffic5": "v"  # Triangle pointing down
}

# Select the colours
paramColors = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"]

for sweep in sweeps:
    fileName = f"Data-Processing\\Processed\\{sweep}-Summary.csv"
    
    try:
        df = pd.read_csv(fileName)
    except FileNotFoundError:
        print(f"Could not find {fileName}, skipping plot.")
        continue

    df['Resolution'] = pd.Categorical(df['Resolution'], categories=resourceOrder, ordered=True)
    df['Total_Pixels'] = df['Resolution'].map(pixelMap)
    df = df.sort_values(['Parameter', 'Video', 'Resolution'])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle(f"Performance Metrics: {sweep} (All Videos)", fontsize=18, fontweight='bold')

    # Loop through Parameters and Videos together
    uniqueParams = df['Parameter'].unique()
    uniqueVideos = df['Video'].unique()

    for i, param in enumerate(uniqueParams):
        color = paramColors[i % len(paramColors)]
        
        for video in uniqueVideos:
            marker = videoMarkers.get(video, "x")
            subset = df[(df['Parameter'] == param) & (df['Video'] == video)]
            
            if not subset.empty:
                xValues = subset['Total_Pixels']
                
                # Use thin line for overlap
                ax1.plot(xValues, subset['Average FPS'], marker=marker, color=color, alpha=0.6, linewidth=1.5, markersize=6)
                ax2.plot(xValues, subset['Total Processing Time'], marker=marker, color=color, alpha=0.6, linewidth=1.5, markersize=6)

    # Add the X Axis titles
    allPixels = sorted(pixelMap.values())
    allLabels = resourceOrder

    # Cleanup the graphs to make them look nice
    for ax in [ax1, ax2]:
        ax.set_xscale('log', base=2)
        ax.set_xticks(allPixels)
        ax.set_xticklabels(allLabels, rotation=45)
        
        # Soften grid and remove top/right borders
        ax.grid(True, linestyle=':', alpha=0.7, color='#B0B0B0')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#888888')
        ax.spines['bottom'].set_color('#888888')

    # Format the FPS Plot labels
    ax1.set_title("Average FPS vs Resolution", fontsize=14)
    ax1.set_xlabel("Resolution (Log2)", fontsize=12)
    ax1.set_ylabel("Average FPS", fontsize=12)

    # Format the Compute Time Plot labels
    ax2.set_title("Total Processing Time vs Resolution", fontsize=14)
    ax2.set_xlabel("Resolution (Log2)", fontsize=12)
    ax2.set_ylabel("Processing Time (seconds)", fontsize=12)

    # Create the Legend
    paramHandles = []
    for i, param in enumerate(uniqueParams):
        color = paramColors[i % len(paramColors)]
        line = mlines.Line2D([], [], color=color, marker='None', linewidth=4, label=param)
        paramHandles.append(line)
        
    videoHandles = []
    for video in uniqueVideos:
        marker = videoMarkers.get(video, "x")
        point = mlines.Line2D([], [], color='#555555', marker=marker, linestyle='None', markersize=8, label=video)
        videoHandles.append(point)

    # Add the Legends outside of the plot
    fig.legend(handles=paramHandles, loc='lower center', bbox_to_anchor=(0.5, 0.10), ncol=len(uniqueParams), frameon=False, title="Parameters (Colors)", title_fontproperties={'weight':'bold'})
    fig.legend(handles=videoHandles, loc='lower center', bbox_to_anchor=(0.5, 0.05), ncol=len(uniqueVideos), frameon=False, title="Videos (Shapes)", title_fontproperties={'weight':'bold'})

    # Leave a bit of a gap below
    plt.subplots_adjust(bottom=0.25)

    # Save the plots
    outputFile = f"Data-Processing\\Processed\\Plots\\{sweep}_Master_Plot.png"
    plt.savefig(outputFile, dpi=300)
    print(f"Saved {outputFile}")
    
    plt.close()