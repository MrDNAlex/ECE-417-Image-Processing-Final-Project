# ECE-417-Image-Processing-Final-Project
The Final Project for ECE 417 - Image Processing. Will cover Scene detection without the use of Neural Networks

# Setup Development Environment
To setup your environment run the following commands in your terminal :

> Note : it is best to use Bash or CMD to execute these commands

Create a new Virtual Environment :
```bash
python -m venv venv
```

Activate the Virtual Environment (Windows) :
```bash
source venv/Scripts/Activate
```

Install the required packages :
```bash
pip install -r requirements.txt
```

One step Setup
```bash
python -m venv venv
source venv/Scripts/Activate
pip install -r requirements.txt
```

# Reproducing the Results
> Note : All data will be produced in a "Cache" Directory, the data must then be transferred to "Data-Processing/Raw-Data/categoryDirectory" to be processed. Additionally it is suggested to use a High Performance computing device like a Server with many cores to process this data.

Start by compiling the code through Cython for faster processing :
```bash
python CompiledImplementation/setup.py build_ext --build-lib CompiledImplementation/
```

Then, ensure you have a Directory named "Videos" with the video structure :
- Videos
    - 120p
        - Traffic1.mp4
        - Traffic2.mp4
        ...
    - 240p
        - Traffic1.mp4
        - Traffic2.mp4
        ...

Next, run the Timing Benchmark with the following commands :
```bash
nohup python Benchmarking/TimingBenchmark.py 1 0 0 > timing10.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 1 1 0 > timing110.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 1 1 1 > timing111.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 1 1 2 > timing112.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 1 1 3 > timing113.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 1 1 4 > timing114.log 2>&1 &

nohup python Benchmarking/TimingBenchmark.py 2 0 0 > timing20.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 2 1 0 > timing210.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 2 1 1 > timing211.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 2 1 2 > timing212.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 2 1 3 > timing213.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 2 1 4 > timing214.log 2>&1 &

nohup python Benchmarking/TimingBenchmark.py 3 0 0 > timing30.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 3 1 0 > timing310.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 3 1 1 > timing311.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 3 1 2 > timing312.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 3 1 3 > timing313.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 3 1 4 > timing314.log 2>&1 &

nohup python Benchmarking/TimingBenchmark.py 4 0 0 > timing40.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 4 1 0 > timing410.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 4 1 1 > timing411.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 4 1 2 > timing412.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 4 1 3 > timing413.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 4 1 4 > timing414.log 2>&1 &

nohup python Benchmarking/TimingBenchmark.py 1 1 0 > timing110.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 1 1 1 > timing111.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 1 1 2 > timing112.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 1 1 3 > timing113.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 1 1 4 > timing114.log 2>&1 &

nohup python Benchmarking/TimingBenchmark.py 2 1 0 > timing210.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 2 1 1 > timing211.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 2 1 2 > timing212.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 2 1 3 > timing213.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 2 1 4 > timing214.log 2>&1 &

nohup python Benchmarking/TimingBenchmark.py 3 1 0 > timing310.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 3 1 1 > timing311.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 3 1 2 > timing312.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 3 1 3 > timing313.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 3 1 4 > timing314.log 2>&1 &

nohup python Benchmarking/TimingBenchmark.py 4 1 0 > timing410.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 4 1 1 > timing411.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 4 1 2 > timing412.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 4 1 3 > timing413.log 2>&1 &
nohup python Benchmarking/TimingBenchmark.py 4 1 4 > timing414.log 2>&1 &
```

Then transfer it to "Data-Processing/Raw-Data/Timing" and run the following python files :
- `ProcessTiming.py`
- `IndexPlots.py`
- `PlotTiming.py`
- `ReducedTimingPlot.py`
- `PlotFPSDistribution.py`
- `PlotComputeBreakdown.py`
- `PlotProcessingDistribution.py`

Next, we can run the Otsu and OpenCV Benchmarking using the following commands :
```bash
nohup python ./Benchmarking/Testing-OpenCV.py > opencv.log 2>&1 &
nohup python ./Benchmarking/Testing-Otsu.py > otsu.log 2>&1 &
```

And Transfer each folder to "Data-Processing/Raw-Data" followed by running the following benchmarks :
```bash
nohup python Benchmarking/Testing_Sweep.py 0 > sweep_debug1.log 2>&1 &
nohup python Benchmarking/Testing_Sweep.py 1 > sweep_debug2.log 2>&1 &
nohup python Benchmarking/Testing_Sweep.py 2 > sweep_debug3.log 2>&1 &
nohup python Benchmarking/Testing_Sweep.py 3 > sweep_debug4.log 2>&1 &
nohup python Benchmarking/Testing_Sweep.py 4 > sweep_debug5.log 2>&1 &
```

Then we can run the scripts to process and compare the frames using the following :
- `ProcessSweep-OpenCVComparison.py`

Then run the following to compare the Frames and score them :
```bash
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic1.csv 5 > compareTraffic1-5.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic2.csv 5 > compareTraffic2-5.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic3.csv 5 > compareTraffic3-5.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic4.csv 5 > compareTraffic4-5.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic5.csv 5 > compareTraffic5-5.log 2>&1 &

nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic1.csv 10 > compareTraffic1-10.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic2.csv 10 > compareTraffic2-10.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic3.csv 10 > compareTraffic3-10.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic4.csv 10 > compareTraffic4-10.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic5.csv 10 > compareTraffic5-10.log 2>&1 &

nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic1.csv 25 > compareTraffic1-25.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic2.csv 25 > compareTraffic2-25.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic3.csv 25 > compareTraffic3-25.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic4.csv 25 > compareTraffic4-25.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic5.csv 25 > compareTraffic5-25.log 2>&1 &

nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic1.csv 50 > compareTraffic1-50.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic2.csv 50 > compareTraffic2-50.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic3.csv 50 > compareTraffic3-50.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic4.csv 50 > compareTraffic4-50.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic5.csv 50 > compareTraffic5-50.log 2>&1 &

nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic1.csv 100 > compareTraffic1-100.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic2.csv 100 > compareTraffic2-100.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic3.csv 100 > compareTraffic3-100.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic4.csv 100 > compareTraffic4-100.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic5.csv 100 > compareTraffic5-100.log 2>&1 &

nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic1.csv 250 > compareTraffic1-250.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic2.csv 250 > compareTraffic2-250.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic3.csv 250 > compareTraffic3-250.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic4.csv 250 > compareTraffic4-250.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic5.csv 250 > compareTraffic5-250.log 2>&1 &

nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic1.csv 500 > compareTraffic1-500.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic2.csv 500 > compareTraffic2-500.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic3.csv 500 > compareTraffic3-500.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic4.csv 500 > compareTraffic4-500.log 2>&1 &
nohup python ./Data-Processing/CompareFrames.py VideoComparison-Traffic5.csv 500 > compareTraffic5-500.log 2>&1 &
```

Once that is complete, move the files to "Data-Processing/Raw-Data/Compression" and run the following Python Scripts :
- `MergeComparisonScores.py`
- `ParamHeatmap.py`
- `FindBestSettings.py`

And now lastly we use the best settings generated and run the following commands :
```bash
nohup python ./Benchmarking/Testing-Novelty.py 0 > novelty-0.log 2>&1 &
nohup python ./Benchmarking/Testing-Novelty.py 1 > novelty-1.log 2>&1 &
nohup python ./Benchmarking/Testing-Novelty.py 2 > novelty-2.log 2>&1 &
nohup python ./Benchmarking/Testing-Novelty.py 3 > novelty-3.log 2>&1 &
```

Which is then finally processed using the following :
- `ProcessCompression.py`
- `CompressionHeatmap.py`

# Repository 
[Repo](https://github.com/MrDNAlex/ECE-417-Image-Processing-Final-Project) : https://github.com/MrDNAlex/ECE-417-Image-Processing-Final-Project

# Authors 
Alexandre Dufresne-Nappert : a3dufres@uwaterloo.ca

Gigi Sae-Zheng : gsaezhen@uwaterloo.ca

San Basnet : s2basnet@uwaterloo.ca
