
import os
from ROOT import TFile,TH1D
from PyHep_Hist_no_rootnumpy import Histogram



def MakePyHist(filename,treename,binning,branchname):

	'''
	Function extracts ROOT TTree from associated ROOT file
	Could implement a sub-function here such that it can be used to loop over many files
	'''

	assert os.path.isfile(filename), "Cannot find this file: "+ filename
	file = TFile(filename,"READ")
	assert hasattr(file,treename), "In file "+filename+", TTree not found:" + treename
	tree = file.Get(treename)

	ROOT_hist = TH1D("hist","",len(binning)-1,binning)
	tree.Project(ROOT_hist.GetName(),branchname)

	ROOT_hist.Scale(1/ROOT_hist.Integral())
	ROOT_hist.SetDirectory(0)

	py_hist = Histogram(ROOT_hist,filename+"_"+treename+"_"+branchname)



	return py_hist









