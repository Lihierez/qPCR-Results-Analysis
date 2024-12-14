# qPCR Resulrs Analasis
This repository contains a Python tool designed to analyze qPCR (quantitative Polymerase Chain Reaction) data. 
The tool takes an Excel file with qPCR results and the name of the refernce gene as input and generates a table and visualization of key analysis metrics. 
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
