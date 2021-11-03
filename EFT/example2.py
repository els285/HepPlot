
import matplotlib.pyplot as plt
from parse_directories import auto_construct
from EFTLimitPlotter_MultiExclusion2 import ATLAS_HiggsStyle_EFT_Plot, LHC_EFT_Plot

x = auto_construct("/home/ethan/EFTfitterSpinCorr.jl/results_ptz_laurynas")

# print(x)
# input()


y = ATLAS_HiggsStyle_EFT_Plot(df=x,to_plot="all",
                # to_plot=["Linear+Quadratic (Marginalised)","Linear (Marginalsied)" ,"Linear+Quadratic (Independent)"],
                experiment="ATLAS",
                orientation="horizontal",
                plot_zero_line=True)

# To define the same order every time, it is necessary to specify the to_plot field in the above

# fig,ax=y.make_horizontal_plot()
# y.plot_global_mode_horizontal()

fig,ax=y.make_plot(orientation="horizontal",plot_global_modes=True)
# print(y.__dict__)
# input()

y.include_metadata("Internal",True,139,2017)
y.additional_label(r"SMEFT $\Lambda = 1$ TeV")

# ax.set_xlim(-15,20)


# plt.show()
# input()

fig.set_size_inches(10, 6)

plt.savefig("fig1.png",dpi=300)