import pandas as pd
import os

# Define inputs and outputs
videoNames = ["Traffic1", "Traffic2", "Traffic3", "Traffic4", "Traffic5"]
outputDir = os.path.join("Data-Processing", "Processed")
os.makedirs(outputDir, exist_ok=True)

# Collect all video data into one list
allData = []

for video in videoNames:
    fileName = os.path.join(outputDir, f"VideoScores-Merged-{video}.csv")
    
    try:
        df = pd.read_csv(fileName)
        df['Traffic Video'] = video 
        allData.append(df)
    except FileNotFoundError:
        print(f"File {fileName} not found. Skipping.")
        continue

if not allData:
    print("No data was found. Exiting.")
    exit()

masterDF = pd.concat(allData, ignore_index=True)

# Generate the Raw Video outputs (Best for every Video + Res + M)
bestResultsCV = []
bestResultsOtsu = []

for (video, res, mVal), group in masterDF.groupby(['Traffic Video', 'Resolution', 'M']):
    
    # Best OpenCV
    bestIdxCV = group['SSIM OpenCV AVG'].idxmax()
    bestRowCV = masterDF.loc[bestIdxCV].copy()
    bestRowCV['Method'] = 'OpenCV'
    bestResultsCV.append(bestRowCV)
    
    # Best Otsu
    bestIdxOtsu = group['SSIM Otsu AVG'].idxmax()
    bestRowOtsu = masterDF.loc[bestIdxOtsu].copy()
    bestRowOtsu['Method'] = 'Otsu'
    bestResultsOtsu.append(bestRowOtsu)

if bestResultsCV and bestResultsOtsu:
    bestCVDF = pd.DataFrame(bestResultsCV)
    bestOtsuDF = pd.DataFrame(bestResultsOtsu)
    
    # Sort
    bestCVDF = bestCVDF.sort_values(['Resolution', 'M', 'Traffic Video'])
    bestOtsuDF = bestOtsuDF.sort_values(['Resolution', 'M', 'Traffic Video'])
    
    # Save standard outputs
    outPathCV = os.path.join(outputDir, "Best-OpenCV-Settings.csv")
    outPathOtsu = os.path.join(outputDir, "Best-Otsu-Settings.csv")
    
    bestCVDF.to_csv(outPathCV, index=False)
    bestOtsuDF.to_csv(outPathOtsu, index=False)
    
    print(f"Successfully saved OpenCV merged results to {outPathCV}")
    print(f"Successfully saved Otsu merged results to {outPathOtsu}")

# Generate the Tip-Top Summary Files
summaryCV = []
summaryOtsu = []

# Helper function to easily append clean rows
def addSummaryRow(targetList, category, video, res, mVal, k, a, t, score):
    targetList.append({
        'Category': category,
        'Traffic Video': video,
        'Resolution': res,
        'M': mVal,
        'K': k, 'A': a, 'T': t,
        'Best Score': score
    })

# CATEGORY 1: Best per Video
for video, group in masterDF.groupby('Traffic Video'):
    bestCV = group.loc[group['SSIM OpenCV AVG'].idxmax()]
    addSummaryRow(summaryCV, '1 - Best per Video', bestCV['Traffic Video'], bestCV['Resolution'], bestCV['M'], bestCV['K'], bestCV['A'], bestCV['T'], bestCV['SSIM OpenCV AVG'])
    
    bestOtsu = group.loc[group['SSIM Otsu AVG'].idxmax()]
    addSummaryRow(summaryOtsu, '1 - Best per Video', bestOtsu['Traffic Video'], bestOtsu['Resolution'], bestOtsu['M'], bestOtsu['K'], bestOtsu['A'], bestOtsu['T'], bestOtsu['SSIM Otsu AVG'])

# CATEGORY 2: Best per Resolution
for res, group in masterDF.groupby('Resolution'):
    bestCV = group.loc[group['SSIM OpenCV AVG'].idxmax()]
    addSummaryRow(summaryCV, '2 - Best per Resolution', bestCV['Traffic Video'], bestCV['Resolution'], bestCV['M'], bestCV['K'], bestCV['A'], bestCV['T'], bestCV['SSIM OpenCV AVG'])
    
    bestOtsu = group.loc[group['SSIM Otsu AVG'].idxmax()]
    addSummaryRow(summaryOtsu, '2 - Best per Resolution', bestOtsu['Traffic Video'], bestOtsu['Resolution'], bestOtsu['M'], bestOtsu['K'], bestOtsu['A'], bestOtsu['T'], bestOtsu['SSIM Otsu AVG'])

# CATEGORY 3: Best per M size
for mVal, group in masterDF.groupby('M'):
    bestCV = group.loc[group['SSIM OpenCV AVG'].idxmax()]
    addSummaryRow(summaryCV, '3 - Best per M size', bestCV['Traffic Video'], bestCV['Resolution'], bestCV['M'], bestCV['K'], bestCV['A'], bestCV['T'], bestCV['SSIM OpenCV AVG'])
    
    bestOtsu = group.loc[group['SSIM Otsu AVG'].idxmax()]
    addSummaryRow(summaryOtsu, '3 - Best per M size', bestOtsu['Traffic Video'], bestOtsu['Resolution'], bestOtsu['M'], bestOtsu['K'], bestOtsu['A'], bestOtsu['T'], bestOtsu['SSIM Otsu AVG'])

# CATEGORY 4: Absolute Best Overall
bestAllCV = masterDF.loc[masterDF['SSIM OpenCV AVG'].idxmax()]
addSummaryRow(summaryCV, '4 - Absolute Best Overall', bestAllCV['Traffic Video'], bestAllCV['Resolution'], bestAllCV['M'], bestAllCV['K'], bestAllCV['A'], bestAllCV['T'], bestAllCV['SSIM OpenCV AVG'])

bestAllOtsu = masterDF.loc[masterDF['SSIM Otsu AVG'].idxmax()]
addSummaryRow(summaryOtsu, '4 - Absolute Best Overall', bestAllOtsu['Traffic Video'], bestAllOtsu['Resolution'], bestAllOtsu['M'], bestAllOtsu['K'], bestAllOtsu['A'], bestAllOtsu['T'], bestAllOtsu['SSIM Otsu AVG'])

# Save the Tip-Top Summaries
dfSummaryCV = pd.DataFrame(summaryCV)
dfSummaryOtsu = pd.DataFrame(summaryOtsu)

outMasterCV = os.path.join(outputDir, "TipTop-Summary-OpenCV.csv")
outMasterOtsu = os.path.join(outputDir, "TipTop-Summary-Otsu.csv")

dfSummaryCV.to_csv(outMasterCV, index=False)
dfSummaryOtsu.to_csv(outMasterOtsu, index=False)

print(f"Successfully saved OpenCV Tip-Top Summary to {outMasterCV}")
print(f"Successfully saved Otsu Tip-Top Summary to {outMasterOtsu}")