# qPCR Results Analysis

## Overview:
This repository contains a Python tool designed to analyze qPCR (quantitative Polymerase Chain Reaction) data. 
qPCR is a known method for amplifying DNA using PCR. In biology reaserch it is mostly aim to quantify changes in gene expression.
Instead of anlyse the results of the qPCR manually, this program goal is to create qPCR result analysis  accurate and fast. 

## What is qPCR methos?
qPCR, also known as real-time PCR, is a molecular biology technique used to amplify and quantify DNA. Unlike conventional PCR, which only amplifies DNA, qPCR allows for the real-time monitoring of the amplification process, typically through the use of fluorescent dyes or probes that bind to the DNA. The fluorescence emitted during each cycle is proportional to the amount of DNA present, enabling accurate quantification. A key feature of qPCR is the cycle threshold (CT) value, which represents the number of cycles required for the fluorescence signal to cross a defined threshold, and is inversely proportional to the initial amount of target DNA.

For more imformation about qPCR, here is a [link](https://www.youtube.com/watch?v=iu4s3Hbc_bw) for a video showing the techniqe.

Here is an example for qPCR curve result:
<p align="center">
  <img src="qPCR curve 2.png" alt="qPCR" width="500" style="border-radius: 15px;">
</p>

A qPCR curve graph represents the amplification process of DNA during quantitative PCR. It plots the fluorescence signal (y-axis), which corresponds to the amount of amplified DNA, against the cycle number (x-axis). 
The graph typically consists of three phases:
1. **Baseline Phase:** At the start, the fluorescence signal is low and indistinguishable from background noise. This is because the amount of amplified DNA is too small to detect.
2. **Exponential Phase:** As the reaction progresses, the DNA amplification enters a phase of exponential growth. During this phase, the fluorescence signal increases significantly.
3. **Plateau Phase:** Eventually, the reaction components become limiting, and the amplification slows down. The fluorescence signal plateaus, reflecting the reaction's saturation point.
The Cycle Threshold (CT) value is a key feature of the graph. It is the cycle number at which the fluorescence signal surpasses a predefined threshold set above the baseline noise. 

## The code workflow:
### User Input:
The program accepts a YAML configuration file containing the following information:
* Path to Excel file containing qPCR Ct values for all samples
* Reference Gene Name
  - Reference gene: The gene used as a control in the experiment
* Target Gene Names
  - Target genes: The experimental samples being analyzed
* Control Sample Names
* Number of Replicates

### Analyzing data:
* Extracts relevant data from Excel file (sample name, target name, CT values)
* Calculates mean CT values for reference gene replicates
* Performs key calculations:
  - Delta Ct (ΔCt): Difference between target and reference gene Ct values
  - Delta-Delta Ct (ΔΔCt): Difference in ΔCt between experimental and control groups
  - Fold Change: 2^(-ΔΔCt) calculation showing relative gene expression changes
* Validates control samples
* Statistical Analysis:
  - Performs ANOVA test for each target gene
  - Generates bar plots with statistical significance indicators
  - Shows mean values with standard error bars
  - Displays individual data points for replicates

### Output:
* CSV table containing the key calculations.
* A bar plot graphs showing the fold change in each sample.

## How to run the program?
To run the program, use the following command in the terminal:
```
python qpcr_analysis.py -c /path/to/your/config_file.yaml
```

## Packages Required:
Necessary packeges: 
pandas
numpy
scipy
matplotlib
pyyaml
argparse

To install all required packages, run:
```
pip install -r Required packages.txt
```

## Tests:
**ADD**
  
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="python" width="100" style="border-radius: 15px;">
</p>
