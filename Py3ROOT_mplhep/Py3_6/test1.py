from ROOT import TH1D,TH1
# import matplotlib.pyplot as plt
import numpy as np

TH1.SetDefaultSumw2()

# Make ROOT histograms


hist1 = TH1D("hist1","",20,-1,1)
hist1.FillRandom("gaus",1000)

hist2 = TH1D("hist2","",20,-1,1)
hist2.FillRandom("gaus",1000)

hist3 = hist1.Clone()
hist3.Divide(hist2)

# Convert to Python Wrappers
from PyHist_Class import Histogram_Wrapper as Histogram

x1 = Histogram(hist1,"hist1",colour="red"  ,legend_entry="tennis")
x2 = Histogram(hist2,"hist2",colour="blue"  ,legend_entry="tennis" )


# Initialise the plot
from Plotting import Ratio_Plot_ROOT

p = Ratio_Plot_ROOT("A Plot",list_of_histograms=[x1,x2],divisor=x1,normalise=True)
p.Initialise_Plot_Design("ATLAS")

plt,ax,rax = p.Make_Ratio_Plot("filled-hist",filled=x2)
import matplotlib
# p.Add_ATLAS_Label("Internal")

p.add_axis_labels(x_lower=r"$\Sigma$",y_upper=r"$\eta$",y_lower="y2")


# Additional design paramters

# ax.yaxis.labelpad = -5
rax.yaxis.labelpad = 40

fig = plt.gcf()
fig.set_size_inches(8, 8)


plt.show()
input()

plt.savefig("Example_Plots/plt_lineerrorbar.png",dpi=300)
