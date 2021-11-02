
import matplotlib.pyplot as plt
from parse_directories import auto_construct
from EFTLimitPlotter import LHC_EFT_Plot

x = auto_construct("/home/ethan/EFTfitterSpinCorr.jl/results_ptz_laurynas")

# print(x.Linear.B)
# input()

y = LHC_EFT_Plot(df=x,to_plot="all",experiment="ATLAS",orientation="horizontal")#,colours=["red","blue"])

fig,ax=y.make_horizontal_plot()
y.plot_global_mode_horizontal()

y.include_metadata("",False,50,2017)

# ax.set_ylim(0.5,4)

plt.show()
input()

fig.set_size_inches(10, 6)

plt.savefig("fig1.png",dpi=300)