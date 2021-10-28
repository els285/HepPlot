# HepPlot
Scripts for HEP plotting (Largely histograms)

Including plotting macros for my own Pythonic histograms, as well as possible mplhep plotting

Histogram-type plotting is currently split into three different fields:
1. Python3 ROOT-based plotting based on `mplhep` (requires local set-up of latest ROOT: 6.24 running on python3.6.9 - not compatible with python3.7)
2. Python3 Uproot-based plotting based on `mplhep` using python3.7.5
3. Python2, ROOT-based plotting using `matplotlib.pyplot` only. 

My nominal set-up is to use ROOT-based Python3.6 macro. I am unsure of the status of normalisation stat errors in Uproot.

## EFT Plots
Developing section containing Python3.7 (and possibly Julia) scripts for generating EFT-related plots.

On-going issues:
- Using Uproot works apart from correct generation of ratio plots of normalised histograms. Check whether this is a bug or whether a workaround exists...
- Using python3.6.9 ensures proper ROOT treated for ratio plots, but relies on older version of mplhel.
