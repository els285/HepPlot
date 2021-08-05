import matplotlib.pyplot as plt
import mplhep as hep
import hist
import numpy as np
from hist.intervals import ratio_uncertainty
import boost_histogram as bh
import uproot


class Histogram_Wrapper:

    ''' Wrapper for Boost-Histogram object generated from Uproot parsing of ROOT file '''

    def __init__(self):

        self.normalise = True
        self.number_of_bins = 26



def Get_Extrema(df):
    import math
    return float(math.ceil(df.max())),float(math.floor(df.min()))

def Generate_Histogram(df,bins,normalise):
    h = bh.Histogram(bh.axis.Variable(bins))
    h.fill(df)
    if normalise:
        return h/h.sum()
    else:
        return h

def Branch2Hist(tree,branch_name,**kwargs):

    # Branch to dataframe
    df = tree[branch_name].array(library="pd")

    normalise = kwargs["normalise"] if "normalise" in kwargs else True

    if "binning" in kwargs:
        bins = kwargs["binning"]

    elif "AutoBin" in kwargs and kwargs["AutoBin"]:
        maxH,minH = Get_Extrema(df)
        bins = np.linspace(minH,maxH,26)

    else:
        print("Binning not specified")
        exit()

    return Generate_Histogram(df,bins,normalise)


def main():

    file1 = uproot.open("/home/ethan/Documents/Qualification_Task/Full_Tests/ttbar/Inclusive_Smearings/ttbar_LEPTONS_WITH_EFFICIENCY_july25.root")
    tree1 = file1["smeared"]

    Histogram = Branch2Hist(tree1,"mu_pt",binning=np.linspace(0,500e3,101))

    print(Histogram)

main()



