import matplotlib.pyplot as plt
import numpy as np
from ROOT import TFile,TAxis,TH1,gROOT
import os
import numpy as np

class Histogram:

    @staticmethod
    def Bin_Edges(hist):
        return np.asarray([hist.GetXaxis().GetBinUpEdge(binn) for binn in range(0,hist.GetXaxis().GetNbins()+1)])


    @staticmethod
    def Bin_Centres(hist):
        return np.asarray([hist.GetXaxis().GetBinCenter(binn+1) for binn in range(0,hist.GetNbinsX())])

    @staticmethod
    def Bin_Values(hist):
        return np.asarray([hist.GetBinContent(binn+1) for binn in range(0,hist.GetNbinsX())])

    @staticmethod
    def Bin_Errors(hist):
        return np.asarray([hist.GetBinError(binn+1) for binn in range(0,hist.GetNbinsX())])

    # @staticmethod
    def Compute_Normalised(self):

        h1dN = self.ROOT_hist.Clone(self.ROOT_hist.GetName()+"_norm")

        h1dN.Scale(1/self.ROOT_hist.Integral())

        return h1dN


    def __init__(self,hist,name,**kwargs):

        '''
        Histogram class has evolved to contain more and more parameters.
        Histogram3.ROOT_hist has proven to be problematic
        '''

        self.name               = name
        self.ROOT_hist          = hist
        self.observable_type    = kwargs["obs"]              if "obs"               in kwargs else None
        self.file_name          = kwargs["filename"]         if "filename"          in kwargs else None
        self.branch_name        = kwargs["branchname"]       if "branchname"        in kwargs else None
        self.legend_entry       = kwargs["legend_entry"]     if "legend_entry"      in kwargs else ""
        self.colour             = kwargs["colour"]           if "colour"            in kwargs else "black"
        self.Norm_hist = self.Compute_Normalised()

