# plot_fps_distribution.py
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# Define the resolution resources
resourceOrder = ["120p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
sweeps = ["AlphaSweep", "KSweep", "MorphologySweep", "ThresholdSweep"]

# Load data into dataframe
dataFrames = []
for sweep in sweeps:
    fileName = f"Data-Processing\\Processed\\{sweep}-Summary.csv"
    try:
        df = pd.read_csv(fileName)
        dataFrames.append(df)
    except FileNotFoundError:
        continue

allData = pd.concat(dataFrames, ignore_index=True)

# Extract FPS into list
fpsData = []
for res in resourceOrder:
    # Filter the data and grab just the FPS numbers as a list
    resValues = allData[allData['Resolution'] == res]['Average FPS'].dropna().values
    fpsData.append(resValues)

# Create the Boxplot
fig, ax = plt.subplots(figsize=(12, 6))

# Removed tick_labels from here so we can force them manually
boxPlot = ax.boxplot(fpsData, patch_artist=True)

# Style the boxes and median lines
for box in boxPlot['boxes']:
    box.set(facecolor='#8172B3', alpha=0.6, linewidth=1.5)
for median in boxPlot['medians']:
    median.set(color='#C44E52', linewidth=2)

# Format the Plot
ax.set_yscale('log', base=2)
ax.set_title("Distribution of Average FPS by Resolution (Log2 Scale)", fontsize=16, fontweight='bold')
ax.set_ylabel("Average FPS (Log2)", fontsize=12)
ax.set_xlabel("Resolution", fontsize=12)

# Explicitly set the X-axis positions and text labels
xPositions = range(1, len(resourceOrder) + 1)
ax.set_xticks(xPositions)
ax.set_xticklabels(resourceOrder, rotation=45)

ax.grid(True, axis='y', linestyle=':', alpha=0.7, color='#B0B0B0')

# Clean borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#888888')
ax.spines['bottom'].set_color('#888888')

# Build the Explanatory Legend
iqrPatch = mpatches.Patch(color='#8172B3', alpha=0.6, label='Middle 50% of Data (IQR)')
medianLine = mlines.Line2D([], [], color='#C44E52', linewidth=2, label='Median FPS')
outlierPoint = mlines.Line2D([], [], color='black', marker='o', markerfacecolor='white', markersize=6, linestyle='None', label='Outliers')

ax.legend(handles=[iqrPatch, medianLine, outlierPoint], loc='upper right', fontsize=10, frameon=True)

plt.tight_layout()
outputFile = "Data-Processing\\Processed\\Plots\\FPS_Distribution_Boxplot.png"
plt.savefig(outputFile, dpi=300)
print(f"Saved {outputFile}")