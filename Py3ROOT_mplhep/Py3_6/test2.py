from ROOT import TH1D,TH1
# import matplotlib.pyplot as plt
import numpy as np

TH1.SetDefaultSumw2()

# Make ROOT histograms


from FromTree import project_hist_unNormalised as proj 

ROOThist1 = proj(filename="/home/ethan/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_reco_odd.root",
				treename="reco_odd",
				binning=np.linspace(0,300e3,51),
				branchname="el_pt")

ROOThist2 = proj(filename="/home/ethan/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_reco_odd.root",
				treename="reco_odd",
				binning=np.linspace(0,300e3,51),
				branchname="mu_pt",)



# Convert to Python Wrappers
from PyHist_Class import Histogram_Wrapper as Histogram

x1 = Histogram(ROOThist1,"hist1",colour="blue"  ,legend_entry="tennis")
x2 = Histogram(ROOThist2,"hist2",colour="red"  ,legend_entry="tennis" )


# Initialise the plot
from Plotting import Ratio_Plot_ROOT

p = Ratio_Plot_ROOT("A Plot",list_of_histograms=[x1,x2],divisor=x1,normalise=True)
p.Initialise_Plot_Design("ATLAS")

plt,ax,rax = p.Make_Ratio_Plot("errorbar-line")
import matplotlib
p.Add_ATLAS_Label("Internal")

p.add_axis_labels(x_lower=r"$\Sigma$",y_upper=r"$\eta$",y_lower="y2")


ax.legend(prop={'size': 60})

# Additional design paramters

# ax.yaxis.labelpad = -5
rax.yaxis.labelpad = 40

fig = plt.gcf()
fig.set_size_inches(8, 8)




plt.show()
input()

plt.savefig("save1.png",dpi=300)
