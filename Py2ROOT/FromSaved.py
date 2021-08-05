
import os
from ROOT import TFile,TH1D
from PyHep_Hist import Histogram



def PyHist_fromROOT(filename,histname):

	'''
	Function extracts ROOT TTree from associated ROOT file
	Could implement a sub-function here such that it can be used to loop over many files
	'''

	assert os.path.isfile(filename), "Cannot find this file: "+ filename
	file = TFile(filename,"READ")
	# assert hasattr(file,treename), "In file "+filename+", TTree not found:" + treename
	# tree = file.Get(treename)

	ROOT_hist = file.Get(histname)
	# ROOT_hist.Draw()
	# raw_input()



	ROOT_hist.Scale(1/ROOT_hist.Integral())
	ROOT_hist.SetDirectory(0)

	py_hist = Histogram(ROOT_hist,filename+histname)



	return py_hist









