# Hist Ratio Plot class

"""
Take set of histogram data, normalise and plot
Take hist.Hist arguments
"""

import matplotlib.pyplot as plt
import mplhep as hep
import hist
import numpy as np
from hist.intervals import ratio_uncertainty
import boost_histogram as bh

hist1 = bh.Histogram(bh.axis.Regular(10, 0.0, 1.0))

hist2 = bh.Histogram(bh.axis.Regular(10, 0.0, 1.0))
hist2.fill(np.random.rand(1,1000).tolist())


print(hist1/hist2)

print(np.divide(hist1.values(),hist2.values()))

exit()
print(ratio_uncertainty(hist1.values(),hist1.values())) # can provide a lot of Nan

input()

def Hist_Divide(hist1,hist2):
	return np.divide(hist1.values(),hist2.values())

"""
Recommended implementation as follows (for now):

To automate all error calculations, use boost_histogram objects with ratio error computation using hist.intervals.ratio_uncertainty
Store this information in some wrapper object
Errors can be plotted using additiona matplotlib.pyplot functionality
"""

class MyHist:

	def __init__(self,Hist,**kwargs):
		self.Histogram = Hist



class RatioPlot:

	def __init__(self,hists,normaliser):
		self.hists = hists
		self.normaliser = normaliser


	def Compute_Rations(self):
		for hist in self.hists:
			hist.Histogram/self.normaliser.Histogram

	def Plot(self):

		# Figure initialisation
		fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)

		# Top plot
		hep.histplot(self.hists.values(), ax=ax, stack=True, histtype='fill', label=hists.keys())

		# Compute ratios. can do this through boost-histogram division or 
		yerr = ratio_uncertainty(data.values(), tot.values(), 'poisson')



# a = hist.Hist.new.Reg(20,-2,2).Int64().fill(np.random.uniform(-2,2,size=3000))
# b = hist.Hist.new.Reg(20,-2,2).Int64().fill(np.random.normal(0,0.5,size=5000))

print(ratio_uncertainty(hist1.values(),hist1.values())) # can provide a lot of Nan

# print(Hist_Divide(a,b))