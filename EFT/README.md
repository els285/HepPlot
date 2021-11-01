# EFT Plots

The module EFT Plots is for generating EFT (Effective Field Theory) one-dimensional limit plots based on the `EFTFitter.jl` output format. 
The output directory of the fit is defined, such that the `1dlimits.txt` and `statistics.txt` files are parsed for the relevant numerical informationn.
A pandas dataframe is generated containing this information, and this dataframe is looped over for the various Wilson coefficients to generate the plot.
LHC-based plot styles can be added; this is facilitated via the `mplhep` module.

## Example
```python3

import matplotlib.pyplot as plt
from parse_directories import auto_construct
from EFTLimitPlotter import LHC_EFT_Plot

df = auto_construct("/home/ethan/EFTfitterSpinCorr.jl/results_ptz_laurynas")

plot_object = LHC_EFT_Plot(df=df,to_plot="all",experiment="ATLAS")#,colours=["red","blue"])

fig,ax = plot_object.make_vertical_plot()
plot_object.plot_global_mode_vertical()

plot_object.include_metadata("",False,50,2017)

plt.show()
input()
