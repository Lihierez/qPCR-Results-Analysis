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
* Excel file containing qPCR Ct values for all samples.
* Reference Gene name
  -  Reference gene: The gene that eas used as a control in the expirament.
* Target gene Names
  -  Target gene: The expirament samples.
* Names and number of the samples (Treaded samples and control samples).
* Number of replicates

### Analyzing data:
* Extracts from Excel file the relevant data- sample name, target name, CT values.
* Calulate CT mean for replicas for referace gene.
* Computes the following:
  - Delta Ct (ΔCt): The difference in Ct values between the target gene and the reference gene.
  - Delta-Delta Ct (ΔΔCt): The difference in ΔCt values between the experimental and control groups.
  - Fold Change: The 2^(-ΔΔCt) calculation, which indicates the relative change in gene expression.
* Cheking controls samples.

### Output:
* A table containing the calculation results.
* A bar plot graph showing the fold change across the samples.

## How to run the program?
**ADD**

## Packages Required:
**ADD**

## Tests:
**ADD**
  
<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="python" width="100" style="border-radius: 15px;">
</p>
