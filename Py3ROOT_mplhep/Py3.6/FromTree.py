import os
from ROOT import TFile,TH1D



def project_hist_unNormalised(filename,treename,binning,branchname):

	"""
	Simple command to pull unnormalised histograms from ROOT TTrees
	"""

	assert os.path.isfile(filename), "Cannot find this file: "+ filename
	file = TFile(filename,"READ")
	assert hasattr(file,treename), "In file "+filename+", TTree not found:" + treename
	tree = file.Get(treename)

	ROOT_hist = TH1D(branchname+"_1D","",len(binning)-1,binning)
	tree.Project(ROOT_hist.GetName(),branchname)

	# ROOT_hist.Scale(1/ROOT_hist.Integral())
	ROOT_hist.SetDirectory(0)

	return ROOT_hist









