# from ROOT import TFile, TH1D

from FromSaved import PyHist_fromROOT as PP

def Make_Plot(hist_name):

	pyh1=PP("/home/ethan/Documents/ttZ/sept_minittv/pythia_outputs/try2/truth_spin1D_combined.root",hist_name)

	pyh1.set_colour("blue")
	pyh1.set_legend_entry(hist_name)

	from HistPlot_noratio import hist1dplot_NOratio as plot 

	plt=plot([pyh1],axis_labels={"x_label":"cos angle","y_label":"Normalised"})
	plt.savefig("/home/ethan/Documents/ttZ/sept_minittv/pythia_outputs/try2/truth_plots/"+hist_name+".png",dpi=300)
	# input()


from ROOT import TFile,TH1D

file0 = TFile("/home/ethan/Documents/ttZ/sept_minittv/pythia_outputs/try2/truth_spin1D_combined.root")
for key in file0.GetListOfKeys():
	Make_Plot(key.GetName())


