import matplotlib.pyplot as plt
import numpy as np
from ROOT import TFile,TAxis,TH1,gROOT
import os

class Histogram:

    @staticmethod
    def Compute_Normalised(hist):

        h1dN = hist.Clone(hist.GetName()+"_norm")

        h1dN.Scale(1/hist.Integral())

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
        self.Norm_hist = self.Compute_Normalised(self.ROOT_hist)

