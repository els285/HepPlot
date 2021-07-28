import numpy as np
import uproot

from Hist_Wrapper import Histogram_Wrapper
from Plotting import Ratio_Plot


def main():

    file1 = uproot.open("/home/ethan/Documents/Qualification_Task/Full_Tests/ttbar/Inclusive_Smearings/ttbar_LEPTONS_WITH_EFFICIENCY_july25.root")
    tree1 = file1["smeared"]

    binning = np.linspace(0,500e3,31)

    H_mu_pt = Histogram_Wrapper(tree1,"mu_pt",binning=binning,colour="red")#,normalise=False)#,AutoBin=True)
    H_mu_E  = Histogram_Wrapper(tree1,"mu_e" ,binning=binning,colour="blue")#,normalise=False)



    x = Ratio_Plot("plot1",list_of_histograms=[H_mu_pt,H_mu_E],divisor=H_mu_E)
    x.Initalise_Plot_Design("ATLAS")
    plt = x.Make_Plot()

    plt.show()
    input()

main()