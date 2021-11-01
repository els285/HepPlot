# EFT Plots

The module EFT Plots is for generating EFT (Effective Field Theory) one-dimensional limit plots based on the `EFTFitter.jl` output format. 
The output directory of the fit is defined, such that the `1dlimits.txt` and `statistics.txt` files are parsed for the relevant numerical informationn.
A pandas dataframe is generated containing this information, and this dataframe is looped over for the various Wilson coefficients to generate the plot.
LHC-based plot styles can be added; this is facilitated via the `mplhep` module.
