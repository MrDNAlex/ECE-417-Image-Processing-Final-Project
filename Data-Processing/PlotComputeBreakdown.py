# plot_computation_breakdown.py
import pandas as pd
import matplotlib.pyplot as plt

# Define the resolution resources
resourceOrder = ["120p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
sweeps = ["AlphaSweep", "KSweep", "MorphologySweep", "ThresholdSweep"]

# Load data into dataframe
dataFrames = []
for sweep in sweeps:
    fileName = f"Data-Processing\\Processed\\{sweep}-Summary.csv"
    try:
        df = pd.read_csv(fileName)
        df['Sweep'] = sweep
        dataFrames.append(df)
    except FileNotFoundError:
        continue

if not dataFrames:
    print("No summary CSVs found.")
    exit()

allData = pd.concat(dataFrames, ignore_index=True)
allData['Resolution'] = pd.Categorical(allData['Resolution'], categories=resourceOrder, ordered=True)

# Calculate computation time percentage
allData['Gaussian_Pct'] = (allData['Total Gaussian Time'] / allData['Total Processing Time']) * 100
allData['Tracking_Pct'] = (allData['Total Tracking Time'] / allData['Total Processing Time']) * 100
allData['Other_Pct'] = 100 - allData['Gaussian_Pct'] - allData['Tracking_Pct']

# Average percentage by resolution
breakdownDF = allData.groupby('Resolution')[['Gaussian_Pct', 'Tracking_Pct', 'Other_Pct']].mean().reset_index()

# Create bar chart
fig, ax = plt.subplots(figsize=(10, 6))
xPositions = range(len(breakdownDF['Resolution']))

# Plot layers in organized Fashion
ax.bar(xPositions, breakdownDF['Gaussian_Pct'], label='Background Subtraction', color='#4C72B0', alpha=0.85)
ax.bar(xPositions, breakdownDF['Tracking_Pct'], bottom=breakdownDF['Gaussian_Pct'], label='Object Tracking', color='#DD8452', alpha=0.85)

# Add the remaining time
bottomLayer = breakdownDF['Gaussian_Pct'] + breakdownDF['Tracking_Pct']
ax.bar(xPositions, breakdownDF['Other_Pct'], bottom=bottomLayer, label='Other Overhead', color='#55A868', alpha=0.85)

# Format
ax.set_title("Algorithm Computation Time Breakdown by Resolution", fontsize=16, fontweight='bold')
ax.set_ylabel("Percentage of Total Time (%)", fontsize=12)
ax.set_xlabel("Resolution", fontsize=12)
ax.set_xticks(xPositions)
ax.set_xticklabels(breakdownDF['Resolution'], rotation=45)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=10, frameon=False)

# Clean the graph
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#888888')
ax.spines['bottom'].set_color('#888888')

plt.tight_layout()
outputFile = "Data-Processing\\Processed\\Plots\\Computation_Breakdown_Plot.png"
plt.savefig(outputFile, dpi=300)
print(f"Saved {outputFile}")