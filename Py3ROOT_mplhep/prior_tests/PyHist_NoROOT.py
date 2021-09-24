import matplotlib.pyplot as plt
import numpy as np
from ROOT import TFile,TAxis,TH1,gROOT
import os
import numpy as np
import pickle


# from dataclasses import dataclass
# @dataclass

class Hist_Wrap:
    """ Basic wrapper for ROOT histogram """

    def __init__(self,Name,Bin_Values,Bin_Errors,Bin_Centres,Bin_Edges):
        self.Name        = Name
        self.Bin_Values  = Bin_Values  
        self.Bin_Errors  = Bin_Errors  
        self.Bin_Centres = Bin_Centres 
        self.Bin_Edges   = Bin_Edges   



class PyHist:
    """
    Larger wrapper which contains Hist_Wraps, including methods for ROOT->numpy conversion
    """

    @staticmethod
    def get_bin_values(hist):
        return np.asarray([hist.GetBinContent(binn+1) for binn in range(0,hist.GetNbinsX())])

    @staticmethod
    def get_bin_errors(hist):
        return np.asarray([hist.GetBinError(binn+1) for binn in range(0,hist.GetNbinsX())])

    @staticmethod
    def get_bin_edges(hist):
        return np.asarray([hist.GetXaxis().GetBinUpEdge(binn) for binn in range(0,hist.GetXaxis().GetNbins()+1)])

    @staticmethod
    def get_bin_centres(hist):
        return np.asarray([hist.GetXaxis().GetBinCenter(binn+1) for binn in range(0,hist.GetNbinsX())])

    @staticmethod
    def Compute_Normalised(ROOT_hist):

        """ Takes a ROOT histogram and normalised it"""

        h1dN = ROOT_hist.Clone(ROOT_hist.GetName()+"_norm")
        return h1dN.Scale(1/ROOT_hist.Integral())

    def Create_Wrapper(self,hist,name):

        Bin_Values  = self.get_bin_values(hist)
        Bin_Errors  = self.get_bin_errors(hist)
        Bin_Centres = self.get_bin_centres(hist)
        Bin_Edges   = self.get_bin_edges(hist)
        return Hist_Wrap(name,Bin_Values,Bin_Errors,Bin_Centres,Bin_Edges)

    def __init__(self,hist,name,**kwargs):

        '''
        The PyHist_NoROOT object is for converting ROOT histograms into numpy objects,
            but the data members of the class should contain no ROOT objects.
        '''

        # Meta-data
        self.name               = name
        self.observable_type    = kwargs["obs"]              if "obs"               in kwargs else None
        self.file_name          = kwargs["filename"]         if "filename"          in kwargs else None

        # Plotting information
        self.legend_entry       = kwargs["legend_entry"]     if "legend_entry"      in kwargs else ""
        self.colour             = kwargs["colour"]           if "colour"            in kwargs else "black"

        # Unnormalised Hist wrapper
        self.UnNorm_Hist = self.Create_Wrapper(hist,self.name+"_Unnormalised")

        # Normalised Hist wrapper
        norm_hist = self.Compute_Normalised(hist)
        self.Norm_Hist   = self.Create_Wrapper(norm_hist,self.name+"_Normalised")




