
import matplotlib.pyplot as plt
from parse_directories import auto_construct
from EFTLimitPlotter_MultiExclusion import LHC_EFT_Plot

x = auto_construct("/home/ethan/EFTfitterSpinCorr.jl/results_ptz_laurynas")

# print(x)
# input()


y = LHC_EFT_Plot(df=x,
                to_plot=["Linear","Linear+Quadratic","Independent"],
                experiment="ATLAS",
                orientation="horizontal",
                plot_design_dict={"fit legend marker":"errorbar"},
                colours=["red","blue","green"])

# To define the same order every time, it is necessary to specify the to_plot field in the above

# fig,ax=y.make_horizontal_plot()
# y.plot_global_mode_horizontal()

fig,ax=y.make_plot(orientation="vertical",plot_global_modes=True)

y.include_metadata("Internal",True,139.1,2017)

ax.set_xlim(-15,20)

plt.show()
input()

fig.set_size_inches(10, 6)

plt.savefig("fig1.png",dpi=300)