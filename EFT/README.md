# EFT Plots

The module EFT Plots is for generating EFT (Effective Field Theory) one-dimensional limit plots based on the `EFTFitter.jl` output format, from which data is parsed.

## Parsing
Our `EFTfitter.jl` outputs contains both `.txt` files with data, and a `.josn` file with the same data in a more practically-extractable format.
The `ParseFromTXT.py` script parses the data contained in the `1dlimits.txt` and `statistics.txt` files.
A parser for the JSON file is still required.
Both of these parsing methods will/should return a pandas dataframe with a structure similar to the following:

```
         Linear+Quadratic (Marg.)                                            Linear (Marg.)                              Linear+Quadratic (Indp.)                              
                           Bounds                              Global Mode           Bounds                  Global Mode                   Bounds                   Global Mode
                               68                           95                           68               95                                   68              95              
cHQ1  [(-5.2, -2.3), (-1.0, 8.0)]  [(-5.6, -1.8), (-1.4, 9.0)]   -0.079241  [(-13.0, 13.0)]  [(-13.0, 13.0)]   -0.064140           [(-1.1, 1.15)]  [(-1.1, 1.15)]  2.371551e-07
cHQ3                [(-8.4, 4.0)]               [(-10.0, 6.0)]   -0.048322  [(-10.0, 10.0)]  [(-10.0, 10.0)]   -0.037808            [(-1.2, 1.0)]   [(-1.2, 1.0)]  9.213609e-08
cHt                 [(-4.6, 8.4)]              [(-10.0, 15.0)]   -0.046624  [(-10.5, 10.0)]  [(-10.5, 10.0)]   -0.052951            [(-1.9, 1.5)]   [(-1.9, 1.5)] -2.879516e-07

```
The rows (indices) are the Wilson coefficients. The columns constitute a Pandas MultiIndex with layering 1. Fit (Linear,Linaer+Quadratic,etc.) 2. Data-type (bounds, global mode) 3. Bounds @ various significanes 



## Plotting
LHC-based plot styles can be added; this is facilitated via the `mplhep` module.

## Example
To parse from the output directory:
```python3
from ParseFromTXT import auto_parse
df = auto_parse("<path/to/EFTfitter.jl/output>")
```

The plots are made using the following, where `make_vertical_plot()` plots the limit bounds and `plot_global_mode_vertical()` plots the global mode of each operator.

```python3
from EFTLimitPlotter import LHC_EFT_Plot

Plot_object = LHC_EFT_Plot(df=df,to_plot="all",experiment="ATLAS")#,colours=["red","blue"])

fig,ax = Plot_object.make_plot(orientation="horizontal",plot_global_modes=True)

Plot_object.include_metadata("",False,50,2017)
Plot_object.additional_label(r"SMEFT $\Lambda = 1$ TeV")

```

