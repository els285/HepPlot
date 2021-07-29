import numpy as np
import uproot

from Hist_Wrapper import Histogram_Wrapper
from Plotting import Ratio_Plot


def main():

    file1 = uproot.open("~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_reco_even.root")
    tree1 = file1["reco_even"]

    file2 = uproot.open("~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_particleLevel_even.root")
    tree2 = file2["particleLevel_even"]

    binning = np.linspace(0,500e3,41)

    H_mu_pt = Histogram_Wrapper(tree1,"mu_pt",binning=binning,colour="red" ,label="reco",normalise=True)#,AutoBin=True)
    H_mu_E  = Histogram_Wrapper(tree2,"mu_pt" ,binning=binning,colour="blue",label="truth",normalise=True)

    # Initialise the plot
    x = Ratio_Plot("plot1",list_of_histograms=[H_mu_pt,H_mu_E],divisor=H_mu_E,plot_normalised=True)
    x.Initalise_Plot_Design("ATLAS")

    # Returns the plt object so adjustments can be made here
    plt = x.Make_Step_Fill_Plot()
    x.Add_ATLAS_Label("Internal")
    x.Axis_Labels({"x": "pT [GeV]","y1":"Events","y2":"Ratio"})
    x.Axis_XTick_Labels([0,50,100,150,200,250])

    # plt.show()
    # input()

    plt.savefig("plot2_test.png",dpi=300)
    print("Plot generated and saved.")


main()