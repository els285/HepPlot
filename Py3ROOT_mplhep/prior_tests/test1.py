import matplotlib.pyplot as plt


import mplhep as hep

plt.style.use(hep.style.ATLAS) # This is the correct syntax for Pytohn3.6.9 version (mplhep 0.2.8)

from ROOT import TH1D,TH1,TFile
# import matplotlib.pyplot as plt
import numpy as np

TH1.SetDefaultSumw2()

file0 = TFile("~/Documents/ttZ/sept_minittv/pythia_outputs/final_combined/truth_spin1D_combined.root")

# print(file0)

hist1 = file0.Get("ttZ_spincorr_hel_truth")


fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)


# ax.errorbar(0, 10000, yerr=100000)

hep.histplot(hist1,ax=ax)

# rax.errorbar(0, 10000, yerr=100000)

hep.atlas.text("Internal",loc=1,ax=ax)
plt.show()