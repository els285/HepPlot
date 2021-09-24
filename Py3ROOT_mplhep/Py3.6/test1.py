from ROOT import TH1D,TH1
# import matplotlib.pyplot as plt
import numpy as np

TH1.SetDefaultSumw2()

# Make ROOT histograms


hist1 = TH1D("hist1","",10,-1,1)
hist1.FillRandom("gaus",1000)

hist2 = TH1D("hist2","",10,-1,1)
hist2.FillRandom("gaus",1000)

hist3 = hist1.Clone()
hist3.Divide(hist2)

# Convert to Python Wrappers


from PyHist_Class import Histogram_Wrapper as Histogram

x1 = Histogram(hist1,"hist1",colour="blue"  ,legend_entry="tennis")
x2 = Histogram(hist2,"hist2",colour="red"  ,legend_entry="tennis" )


# Initialise the plot
from Plotting import Ratio_Plot_ROOT

p = Ratio_Plot_ROOT("A Plot",list_of_histograms=[x1,x2],divisor=x1,normalise=True)
p.Initialise_Plot_Design("ATLAS")

plt,ax,rax = p.Make_Ratio_Plot("errorbar-line")

p.Add_ATLAS_Label("Internal")



plt.savefig("save1.png",dpi=300)
