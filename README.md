# qPCR Results Analysis

## Overview:
This repository contains a Python tool designed to analyze qPCR (quantitative Polymerase Chain Reaction) data. 
qPCR is a known method for amplifying DNA using PCR. In biology reaserch it is mostly aim to quantify changes in gene expression.
Instead of anlyse the results of the qPCR manually, this program goal is to create qPCR result analysis  accurate and fast. 

## What is qPCR methos?
qPCR, also known as real-time PCR, is a molecular biology technique used to amplify and quantify DNA. Unlike conventional PCR, which only amplifies DNA, qPCR allows for the real-time monitoring of the amplification process, typically through the use of fluorescent dyes or probes that bind to the DNA. The fluorescence emitted during each cycle is proportional to the amount of DNA present, enabling accurate quantification. A key feature of qPCR is the cycle threshold (CT) value, which represents the number of cycles required for the fluorescence signal to cross a defined threshold, and is inversely proportional to the initial amount of target DNA.

For more imformation about qPCR, here is a [link](https://www.youtube.com/watch?v=iu4s3Hbc_bw) for a video showing the techniqe.

Here is an example for qPCR curse result:
<p align="center">
  <img src="https://www.researchgate.net/profile/Min_Kang37/post/qPCR-amplification-curve-height-difference-in-standard-curve/attachment/59d626fb6cda7b8083a23f06/AS%3A523314999160832%401501779426616/download/2.png" alt="qPCR" width="100" style="border-radius: 15px;">
</p>




The tool takes an Excel file with qPCR results and the name of the refernce gene as inputs and generates a table and visualization of key analysis metrics. 
Specifically, it computes the following:
* Delta Ct (ΔCt): The difference in Ct values between the target gene and the reference gene.
* Delta-Delta Ct (ΔΔCt): The difference in ΔCt values between the experimental and control groups.
* Fold Change: The 2^(-ΔΔCt) calculation, which indicates the relative change in gene expression.
  
## Features:
</u>Input:</u> 
* Excel file containing qPCR Ct values for both the target and reference genes.  
* Reference gene name. 

</u>Output:</u>
* A table containing the calculation results.
* A bar plot graph showing the fold change across the samples.

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="python" width="100" style="border-radius: 15px;">
</p>
