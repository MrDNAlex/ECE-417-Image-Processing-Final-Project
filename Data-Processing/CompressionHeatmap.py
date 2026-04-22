import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Setup Directories and Load Data
outputDir = os.path.join("Data-Processing", "Processed", "Plots")
os.makedirs(outputDir, exist_ok=True)
fileName = os.path.join("Data-Processing", "Processed", "Compression-Sizes-Merged.csv")

try:
    df = pd.read_csv(fileName)
except FileNotFoundError:
    print(f"File {fileName} not found. Skipping.")
    exit()

# Clean strings for a cleaner presentation
df['A'] = df['A'].astype(str).str.replace('_', '')
df['T'] = df['T'].astype(str).str.replace('T', '')
df['K'] = df['K'].astype(str).str.replace('K', '')
df['M'] = df['M'].astype(str).str.replace('M', '')
df['Refresh Index'] = df['Refresh Index'].astype(str)
df['Use Object Detection'] = df['Use Object Detection'].astype(str)

# Calculate Percentage
df['Compressed Size (%)'] = (df['Compressed Size (Bytes)'] / df['Raw Size (Bytes)']) * 100

plotCategories = [
    'Best-OpenCV-Settings', 
    'Best-Otsu-Settings', 
    'TipTop-Summary-OpenCV', 
    'TipTop-Summary-Otsu'
]

resOrder = ["120p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
potentialVars = ['Use Object Detection', 'Refresh Index', 'K', 'M', 'A', 'T', 'Resolution']

# Function to dynamically find boundaries for our multi-layered hierarchy
def getBlocks(multiIdx, levelIdx):
    blocks = []
    start = 0
    currVal = multiIdx[0][levelIdx]
    currParent = multiIdx[0][:levelIdx]
    for i in range(1, len(multiIdx)):
        val = multiIdx[i][levelIdx]
        parent = multiIdx[i][:levelIdx]
        if val != currVal or parent != currParent:
            blocks.append((currVal, start, i))
            start = i
            currVal = val
            currParent = parent
    blocks.append((currVal, start, len(multiIdx)))
    return blocks

# Formatting function for custom text rendering
def formatLabel(varName, val):
    if varName == 'Resolution':
        return str(val)
    elif varName == 'Refresh Index':
        return f"Ref: {val}"
    else:
        return f"{varName}: {val}"

globalMin = df['Compressed Size (%)'].min()
globalMax = df['Compressed Size (%)'].max()

# Create a plot for each category
for cat in plotCategories:
    subset = df[df['Best Settings Category'] == cat].copy()
    if subset.empty:
        print(f"No data for {cat}. Skipping.")
        continue
        
    # Only keep variables that actually change
    activeVars = [v for v in potentialVars if subset[v].nunique() > 1]
    counts = {v: subset[v].nunique() for v in activeVars}
    
    # Calculate the most balanced split point
    bestDiff = float('inf')
    bestSplit = ([], [])
    for i in range(1, len(activeVars)):
        c = activeVars[:i]
        r = activeVars[i:]
        diff = abs(np.prod([counts[x] for x in c]) - np.prod([counts[y] for y in r]))
        if diff < bestDiff:
            bestDiff = diff
            bestSplit = (c, r)
            
    cols, idx = bestSplit
    
    if 'Resolution' in activeVars:
        subset['Resolution'] = pd.Categorical(subset['Resolution'], categories=resOrder, ordered=True)

    pivot = pd.pivot_table(
        subset, values='Compressed Size (%)', index=idx, columns=cols, aggfunc='mean'
    ).dropna(how='all').dropna(axis=1, how='all')

    # Force a massive canvas so the text scales nicely with square cells
    fig, ax = plt.subplots(figsize=(24, 24))
    
    sns.heatmap(pivot, annot=True, cmap="OrRd_r", fmt=".1f", ax=ax,
                vmin=globalMin, vmax=globalMax, square=True, annot_kws={"size": 16},
                cbar_kws={'shrink': 0.6, 'pad': 0.02})

    cbar = ax.collections[0].colorbar
    cbar.set_label('Compressed Size as % of Raw Size', size=20, weight='bold', labelpad=20)
    cbar.ax.tick_params(labelsize=14)
    
    # --- X-Axis Formatting ---
    transX = ax.get_xaxis_transform()
    colIdx = pivot.columns
    ax.set_xticks([i + 0.5 for i in range(len(colIdx))])
    
    innermostCol = cols[-1] if len(cols) > 1 else cols[0]
    ax.set_xticklabels([formatLabel(innermostCol, colIdx[i][-1] if len(cols)>1 else colIdx[i]) for i in range(len(colIdx))], rotation=90, fontsize=16)
    ax.set_xlabel("")
    
    for level in range(len(cols)-1):
        blocks = getBlocks(colIdx, level)
        depth = (len(cols) - 2 - level)
        # Increased gap logic so text doesn't hit rotated inner labels
        y_text = -0.15 - (depth * 0.08)  
        
        for val, start, end in blocks:
            if start > 0: ax.axvline(start, color='black', linewidth=3)
            ax.text((start + end) / 2.0, y_text, formatLabel(cols[level], val), transform=transX, ha='center', va='top', fontsize=18, fontweight='bold')

    # --- Y-Axis Formatting ---
    transY = ax.get_yaxis_transform()
    rowIdx = pivot.index
    ax.set_yticks([i + 0.5 for i in range(len(rowIdx))])
    
    innermost_row = idx[-1] if len(idx) > 1 else idx[0]
    ax.set_yticklabels([formatLabel(innermost_row, rowIdx[i][-1] if len(idx)>1 else rowIdx[i]) for i in range(len(rowIdx))], rotation=0, fontsize=16)
    ax.set_ylabel("")

    for level in range(len(idx)-1):
        blocks = getBlocks(rowIdx, level)
        depth = (len(idx) - 2 - level)
        x_text = -0.15 - (depth * 0.08)  
        
        for val, start, end in blocks:
            if start > 0: ax.axhline(start, color='black', linewidth=3)
            ax.text(x_text, (start + end) / 2.0, formatLabel(idx[level], val), transform=transY, ha='right', va='center', rotation=90, fontsize=18, fontweight='bold')

    # Static pad pushes title high above the heatmap bounds
    ax.set_title(f"Category: {cat}", fontsize=36, fontweight='bold', pad=80)
    
    outputImg = os.path.join(outputDir, f"Compression_Heatmap_{cat}.png")
    plt.savefig(outputImg, bbox_inches='tight', pad_inches=1.2)
    plt.close()

print("Successfully generated and saved refined heatmaps.")