import ROOT

from FromSaved import PyHist_fromROOT as PHF

pythia_hist = PHF("/home/ethan/Documents/ttZ/july21/july21_ttZ_spincorrelations_pythia3.root","cos_delta_phi_top_pythia")

herwig_hist = PHF("/home/ethan/Documents/ttZ/july21/july21_ttZ_spincorrelations_herwig3.root","cos_delta_phi_top_herwig")

pythia_hist.set_legend_entry("PYTHIA")
herwig_hist.set_legend_entry("HERWIG")

pythia_hist.set_colour("red")
herwig_hist.set_colour("blue")


# print(pythia_hist.__dict__)
# exit()
from HistPlot1 import hist1dplot_withratio as plot

axis_labels = {"x_label": r"\cos \phi","y_upper":"Normalised Number of Events","y_lower": "Ratio w.r.t. Pythia sample"}

plot([pythia_hist,herwig_hist],normaliser=pythia_hist,axis_labels=axis_labels,title="")