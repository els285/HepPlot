from ROOT import TH1D,TH1,TFile
# import matplotlib.pyplot as plt
import numpy as np

TH1.SetDefaultSumw2()



# hist1 = TH1D("hist1","",100,-3,3)
# hist1.FillRandom("gaus",1000)

# hist2 = TH1D("hist2","",100,-3,3)
# hist2.FillRandom("gaus",1000)

# hist3 = hist1.Clone()
# hist3.Divide(hist2)



file0 = TFile("~/Documents/ttZ/sept_minittv/pythia_outputs/final_combined/truth_spin1D_combined.root")

print(file0)

hist1 = file0.Get("ttZ_spincorr_hel_truth")

from PyHist_New import Histogram
x1 = Histogram(hist1,"hist1",colour="blue"  ,legend_entry="tennis")





# hist1.Scale(1/hist1.Integral())


# x1 = Histogram(hist1,"hist1",colour="blue"  ,legend_entry="tennis")
# x2 = Histogram(hist2,"hist2",colour="red",legend_entry="tennis")

import matplotlib.pyplot as plt 
import mplhep as hep



# plt.style.use(hep.style.ATLAS) # This is the correct syntax for Pytohn3.6.9 version (mplhep 0.2.8)

fig, ax = plt.subplots()

# fig,ax =
# Ratio plot
# fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)



# hep.atlas.text("Internal",loc=1)#,ax=ax,loc=0)


# hep.histplot(x1.ROOT_hist,ax=ax)
# ax.errorbar(0, 10000, yerr=100000)
plt.axvline(0,-10000,10000)


# print(x1.Bin_Centres(x1.ROOT_hist))
# print(x1.Bin_Values(x1.ROOT_hist))

plt.xlim((1,11))

plt.show()
input()


# from Plotting import Ratio_Plot_ROOT

# p = Ratio_Plot_ROOT("A Plot",list_of_histograms=[x1,x2],divisor=x1)
# p.Initalise_Plot_Design("ATLAS")

# plt = p.Make_Plot()

# plt.show()

# input()


# import mplhep as hep 

# import matplotlib.pyplot as plt

# plt.style.use(hep.style.ATLAS)

# fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)

# hep.atlas.text("jsghshgjk",ax=ax,loc=1)



# for hist in [x1,x2]:
# 	hep.histplot(hist.ROOT_hist, ax=ax, stack=False, histtype='step',color=hist.colour,label=hist.legend_entry,lw=1.0)


# # hep.histplot([hist1,hist2])

# plt.savefig("plot3_test.png",dpi=300)
