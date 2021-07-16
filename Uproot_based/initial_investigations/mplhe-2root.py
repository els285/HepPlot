import ROOT
file = ROOT.TFile("~/Documents/feb15_test1.root","READ")

tree = file.Get("smeared")

import numpy as np

bins = np.linspace(0,1e6,11)
hist = ROOT.TH1D("mu_pt","",len(bins)-1,bins)


import mplhep as hep
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

hep.histplot(hist)

plt.show()


# plt.show()
# hep.style.use("ATLAS")
# plt.bar(h.axes[0].centers, h, h.axes[0].widths)
# plt.show()
# input()
# plt.close()

# print(caz.__dict__)
# # print(tree)