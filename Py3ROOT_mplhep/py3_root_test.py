from ROOT import TH1D,TH1
# import matplotlib.pyplot as plt
import numpy as np

TH1.SetDefaultSumw2()



hist1 = TH1D("hist1","",5,-3,3)
hist1.FillRandom("gaus",1000)

hist2 = TH1D("hist2","",5,-3,3)
hist2.FillRandom("gaus",1000)

hist3 = hist1.Clone()
hist3.Divide(hist2)


from PyHist_New import Histogram

x1 = Histogram(hist1,"hist1",colour="blue"  ,legend_entry="tennis")
x2 = Histogram(hist2,"hist2",colour="red",legend_entry="tennis")



from Plotting import Ratio_Plot_ROOT

p = Ratio_Plot_ROOT("A Plot",list_of_histograms=[x1,x2],divisor=x1)
p.Initalise_Plot_Design("ATLAS")

plt = p.Make_Plot()

plt.show()

input()


import mplhep as hep 

import matplotlib.pyplot as plt

plt.style.use(hep.style.ATLAS)

fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)

hep.atlas.text("jsghshgjk",ax=ax,loc=1)



for hist in [x1,x2]:
	hep.histplot(hist.ROOT_hist, ax=ax, stack=False, histtype='step',color=hist.colour,label=hist.legend_entry,lw=1.0)


# hep.histplot([hist1,hist2])

plt.savefig("plot3_test.png",dpi=300)
