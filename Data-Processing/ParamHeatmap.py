import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

videoNames = ["Traffic1", "Traffic2", "Traffic3", "Traffic4", "Traffic5"]
outputDir = os.path.join("Data-Processing", "Processed", "Plots")
os.makedirs(outputDir, exist_ok=True)

# Define resolution order to force the hierarchy to sort properly
resOrder = ["120p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]

for video in videoNames:
    fileName = os.path.join("Data-Processing", "Processed", f"VideoScores-Merged-{video}.csv")
    
    try:
        df = pd.read_csv(fileName)
    except FileNotFoundError:
        print(f"File {fileName} not found. Skipping.")
        continue

    # Clean strings for a cleaner presentation
    df['A'] = df['A'].str.replace('_', '')
    df['T'] = df['T'].str.replace('T', '')
    df['K'] = df['K'].str.replace('K', '')
    df['M'] = df['M'].str.replace('M', '')

    df['Resolution'] = pd.Categorical(df['Resolution'], categories=resOrder, ordered=True)
    
    # Ensure Frames Compared is numeric for proper sorting
    df['Frames Compared'] = pd.to_numeric(df['Frames Compared'])
    frameLevels = sorted(df['Frames Compared'].unique())
    
    # Create the iteration list: First the full average, then individual frame subsets
    plotIterations = ['Averaged'] + frameLevels

    for frameVal in plotIterations:
        # Determine the subset and naming conventions for this iteration
        if frameVal == 'Averaged':
            subset = df
            titleSuffix = "Averaged Across All Frames"
            fileSuffix = "Averaged"
        else:
            subset = df[df['Frames Compared'] == frameVal]
            titleSuffix = f"{frameVal} Frames Compared"
            fileSuffix = f"{frameVal}Frames"

        # Calculate the global color scale between both algorithms for the current subset
        globalMin = min(subset['SSIM OpenCV AVG'].min(), subset['SSIM Otsu AVG'].min())
        globalMax = max(subset['SSIM OpenCV AVG'].max(), subset['SSIM Otsu AVG'].max())

        # Create the pivot tables
        pivotCv = pd.pivot_table(
            subset, values='SSIM OpenCV AVG', index=['A', 'T', 'Resolution'], columns=['K', 'M'], aggfunc='mean'
        ).dropna(how='all').dropna(axis=1, how='all')

        pivotOtsu = pd.pivot_table(
            subset, values='SSIM Otsu AVG', index=['A', 'T', 'Resolution'], columns=['K', 'M'], aggfunc='mean'
        ).dropna(how='all').dropna(axis=1, how='all')

        # Create Subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 16), sharey=True)
        fig.suptitle(f"SSIM Average Score Heatmap - {video} ({titleSuffix})", fontsize=26, fontweight='bold', y=0.96)
        
        # Draw the heatmaps without color bars
        sns.heatmap(pivotCv, annot=True, cmap="YlGnBu", fmt=".3f", ax=ax1, 
                    vmin=globalMin, vmax=globalMax, cbar=False, annot_kws={"size": 15})
        sns.heatmap(pivotOtsu, annot=True, cmap="YlGnBu", fmt=".3f", ax=ax2, 
                    vmin=globalMin, vmax=globalMax, cbar=False, annot_kws={"size": 15})
                    
        ax1.set_title("OpenCV AVG Score", fontsize=22, fontweight='bold', pad=40)
        ax2.set_title("Otsu AVG Score", fontsize=22, fontweight='bold', pad=40)

        # Extract and format the Global Colorbar on the far right
        cbarAx = fig.add_axes([0.92, 0.15, 0.015, 0.7]) 
        cbar = fig.colorbar(ax1.collections[0], cax=cbarAx)
        cbar.set_label('SSIM AVG Score', fontsize=20, fontweight='bold', labelpad=20)
        cbar.ax.tick_params(labelsize=16)

        # X-AXIS HIERARCHY (Columns: K -> M)
        colLevelsK = pivotCv.columns.get_level_values('K')
        colLevelsM = pivotCv.columns.get_level_values('M')

        kBlocks = []
        start = 0
        currK = colLevelsK[0]
        for i in range(1, len(colLevelsK)):
            if colLevelsK[i] != currK:
                kBlocks.append((currK, start, i))
                start = i
                currK = colLevelsK[i]
        kBlocks.append((currK, start, len(colLevelsK)))

        # Apply X-axis formatting to subplots
        for ax in [ax1, ax2]:
            ax.set_xticks([i + 0.5 for i in range(len(colLevelsM))])
            ax.set_xticklabels([f"M{m}" for m in colLevelsM], rotation=0, fontsize=12)
            ax.set_xlabel("") 

            # Draw dividers and top titles
            for kVal, start, end in kBlocks:
                if start > 0:
                    ax.axvline(start, color='black', linewidth=3)
                    
                midPoint = (start + end) / 2.0
                ax.text(midPoint, -0.15, f"Kernel: K{kVal}", ha='center', va='bottom', fontsize=16, fontweight='bold')

        # Y-AXIS HIERARCHY (Rows: A -> T -> Resolution)
        rowLevelsA = pivotCv.index.get_level_values('A')
        rowLevelsT = pivotCv.index.get_level_values('T')
        rowLevelsRes = pivotCv.index.get_level_values('Resolution')

        tBlocks = []
        start = 0
        currA = rowLevelsA[0]
        currT = rowLevelsT[0]
        for i in range(1, len(rowLevelsT)):
            if rowLevelsT[i] != currT or rowLevelsA[i] != currA:
                tBlocks.append((currA, currT, start, i))
                start = i
                currT = rowLevelsT[i]
                currA = rowLevelsA[i]
        tBlocks.append((currA, currT, start, len(rowLevelsT)))

        aBlocks = []
        start = 0
        currA = rowLevelsA[0]
        for i in range(1, len(rowLevelsA)):
            if rowLevelsA[i] != currA:
                aBlocks.append((currA, start, i))
                start = i
                currA = rowLevelsA[i]
        aBlocks.append((currA, start, len(rowLevelsA)))

        # Apply inner Y-axis ticks to the left subplot only
        ax1.set_yticks([i + 0.5 for i in range(len(rowLevelsRes))])
        ax1.set_yticklabels(rowLevelsRes, rotation=0, fontsize=11)
        ax1.set_ylabel("") 
        ax2.set_ylabel("")

        # Draw horizontal dividers on subplots
        for ax in [ax1, ax2]:
            for _, tVal, start, end in tBlocks:
                if start > 0:
                    ax.axhline(start, color='gray', linewidth=1.5, linestyle='--')
            for aVal, start, end in aBlocks:
                if start > 0:
                    ax.axhline(start, color='black', linewidth=3)

        # Draw rotated left titles on the LEFT subplot only
        for _, tVal, start, end in tBlocks:
            midPoint = (start + end) / 2.0
            ax1.text(-0.45, midPoint, f"Thresh: {tVal}", ha='center', va='center', rotation=90, fontsize=14, fontweight='bold', color='#444444')

        for aVal, start, end in aBlocks:
            midPoint = (start + end) / 2.0
            ax1.text(-0.65, midPoint, f"Alpha: {aVal}", ha='center', va='center', rotation=90, fontsize=16, fontweight='bold')

        # Final Adjustments
        fig.subplots_adjust(left=0.08, right=0.90, top=0.88, bottom=0.05, wspace=0.03) 

        # Dynamically append the file suffix so we don't overwrite the images
        outputImg = os.path.join(outputDir, f"ParamSweep-Heatmap-{video}-{fileSuffix}.png")
        plt.savefig(outputImg)
        plt.close()
        
        print(f"Successfully saved shared hierarchical heatmap for {video} ({fileSuffix}) to {outputImg}")