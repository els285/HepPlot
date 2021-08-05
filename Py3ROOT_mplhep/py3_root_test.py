from ROOT import TH1D,TH1

import numpy as np

TH1.SetDefaultSumw2()



hist1 = TH1D("hist1","",100,-3,3)
hist1.FillRandom("gaus",1000)

hist2 = TH1D("hist2","",100,-3,3)
hist2.FillRandom("gaus",1000)

hist3 = hist1.Clone()
hist3.Divide(hist2)

import mplhep as hep 

import matplotlib.pyplot as plt

hep.histplot([hist1,hist2])

plt.show()