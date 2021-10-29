
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mplhep as hep

from parse_directories import auto_construct
from EFTLimitPlotter import LHC_EFT_Plot

x = auto_construct("/home/ethan/EFTfitterSpinCorr.jl/results_ptz_laurynas")

y = LHC_EFT_Plot(df=x,to_plot="all",experiment="ATLAS")#,colours=["red","blue"])

fig,ax=y.make_vertical_plot()
y.include_metadata("",False,50,2017)

plt.show()
input()