import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

videoNames = ["Traffic1", "Traffic2", "Traffic3", "Traffic4", "Traffic5"]
outputDir = os.path.join("Data-Processing", "Processed", "Plots")
os.makedirs(outputDir, exist_ok=True)

for video in videoNames:
    fileName = os.path.join("Data-Processing", "Processed", f"VideoScores-Merged-{video}.csv")
    
    try:
        df = pd.read_csv(fileName)
    except FileNotFoundError:
        print(f"File {fileName} not found. Skipping.")
        continue
        
    # Define a 3x2 grid. Left column = OpenCV, Right column = Otsu.
    fig, axs = plt.subplots(3, 2, figsize=(16, 12), sharex=True, sharey='row')
    fig.suptitle(f"SSIM Scores by Number of Frames Compared - {video}", fontsize=18, fontweight='bold')
    
    frameLevels = sorted(df['Frames Compared'].unique())
    colorsCV = plt.cm.Blues(np.linspace(0.4, 1.0, len(frameLevels)))
    colorsOtsu = plt.cm.Oranges(np.linspace(0.4, 1.0, len(frameLevels)))
    
    # Map out the resolution regions
    baseSubset = df[df['Frames Compared'] == frameLevels[0]].reset_index(drop=True)
    resBlocks = []
    startIndex = 0
    currentRes = baseSubset.loc[0, 'Resolution']
    
    for idx in range(1, len(baseSubset)):
        if baseSubset.loc[idx, 'Resolution'] != currentRes:
            resBlocks.append((currentRes, startIndex, idx - 1))
            startIndex = idx
            currentRes = baseSubset.loc[idx, 'Resolution']
    resBlocks.append((currentRes, startIndex, len(baseSubset) - 1))
    
    for i, frames in enumerate(frameLevels):
        subset = df[df['Frames Compared'] == frames].reset_index(drop=True)
        
        # Left Column (Col 0): OpenCV Data
        axs[0, 0].plot(subset.index, subset['SSIM OpenCV AVG'], color=colorsCV[i], alpha=0.8, label=f"{frames}")
        axs[1, 0].plot(subset.index, subset['SSIM OpenCV Var'], color=colorsCV[i], alpha=0.8)
        axs[2, 0].plot(subset.index, subset['SSIM OpenCV Med'], color=colorsCV[i], alpha=0.8)
        
        # Right Column (Col 1): Otsu Data
        axs[0, 1].plot(subset.index, subset['SSIM Otsu AVG'], color=colorsOtsu[i], alpha=0.8, label=f"{frames}")
        axs[1, 1].plot(subset.index, subset['SSIM Otsu Var'], color=colorsOtsu[i], alpha=0.8)
        axs[2, 1].plot(subset.index, subset['SSIM Otsu Med'], color=colorsOtsu[i], alpha=0.8)
        
    # Format Column Titles
    axs[0, 0].set_title("OpenCV Performance", pad=25, fontsize=14, fontweight='bold')
    axs[0, 1].set_title("Otsu Performance", pad=25, fontsize=14, fontweight='bold')
    
    # Format Left Column (OpenCV)
    axs[0, 0].set_ylabel("Average Score", fontsize=12)
    axs[1, 0].set_ylabel("Variance", fontsize=12)
    axs[2, 0].set_ylabel("Median Score", fontsize=12)
    axs[2, 0].set_xlabel("Index (Row Number)", fontsize=12)
    
    # Format Right Column (Otsu)
    axs[2, 1].set_xlabel("Index (Row Number)", fontsize=12)
    
    # Add grids, resolution dividers, and centered text
    for row in range(3):
        for col in range(2):
            # Apply my standard grid format
            axs[row, col].grid(True, linestyle='--', alpha=0.6, color='#B0B0B0')
            
            # Clean borders
            axs[row, col].spines['top'].set_visible(False)
            axs[row, col].spines['right'].set_visible(False)
            axs[row, col].spines['left'].set_color('#888888')
            axs[row, col].spines['bottom'].set_color('#888888')
            
            # Draw vertical dashed lines separating the resolutions
            for _, start, _ in resBlocks[1:]:
                axs[row, col].axvline(x=start - 0.5, color='#B0B0B0', linestyle='--', alpha=0.7)
                
    for col in range(2):
        for res, start, end in resBlocks:
            midPoint = (start + end) / 2.0
            
            # Dropped the text so it clears the tick numbers
            axs[2, col].text(midPoint, -0.25, res, 
                             transform=axs[2, col].get_xaxis_transform(), 
                             ha='center', va='top', fontsize=12, fontweight='bold', color='#555555')
    
    # Place centered split legends above each column with no frame
    axs[0, 0].legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=8, fontsize=10, frameon=False)
    axs[0, 1].legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=8, fontsize=10, frameon=False)
    
    plt.tight_layout()
    
    # Increased bottom padding to make room for the lower text
    fig.subplots_adjust(top=0.90, bottom=0.10)
    
    outputImg = os.path.join(outputDir, f"ParameterIndexCurves-{video}.png")
    plt.savefig(outputImg)
    plt.close()
    
    print(f"Successfully saved {outputImg}")