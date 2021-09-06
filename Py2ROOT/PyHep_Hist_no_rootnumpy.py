import matplotlib.pyplot as plt
import numpy as np
from ROOT import TFile,TAxis,TH1,gROOT
import os
import sys
# import root_numpy

# infile_path = sys.argv[1]


def hist2array(hist):

    contents = []
    for binn in range(0,hist.GetXaxis().GetNbins()):
        contents.append(hist.GetBinContent(binn+1))

    # print(np.asarray(contents))
    # raw_input()
    return np.asarray(contents)



TH1.SetDefaultSumw2()

def preplot(hist,normalise):

    '''
    The preplot function converts existing TH1D into numpy arrays corresponding to bin values and errors
    Also extracts the x-axis bin edges and centres
    TH1Ds can be normalised by turning on the 'normalise' boolean
    '''




    if normalise:
        hist.Scale(1/hist.Integral())

    x_axis = hist.GetXaxis()

    x_binning= []
    x_centre_binning = []
    bin_stat_errors = []

    for binn in range(0,x_axis.GetNbins()+1):
        x_binning.append(x_axis.GetBinUpEdge(binn))
        x_centre_binning.append(x_axis.GetBinCenter(binn))

    for binn in range(0,x_axis.GetNbins()):
        bin_stat_errors.append(hist.GetBinError(binn+1))

        # print(hist.GetBinContent(binn))
        # if hist.GetBinContent(binn) != 0.0: print(1/math.sqrt(hist.GetBinContent(binn)))
        # print(hist.GetBinError(binn))
        # raw_input()

    # Convert x-bins to numpy arrays
    xbins           = np.asarray(x_binning)
    xcbins          = np.asarray(x_centre_binning)
    bin_stat_errors = np.asarray(bin_stat_errors)

    # Remove the last element of the xbins array
    # xnbins = np.delete(xbins,-1,0)

    ## Convert histogram to numpy ndarray
    h1d_num = hist2array(hist)

    ## Append 0 on end for plotting
    h1d_num = np.append(h1d_num,0.0)

    # Finalise bin centre points for plotting of errorbars or data (plus errorbars)
    xcbins = np.delete(xcbins,0,0)

    return xbins,xcbins,h1d_num,bin_stat_errors



def normalised_histograms(hist,normaliser):

    '''
    This function takes a single TH1D plus another TH1D which acts as a divisor.
    Return numpy arrays pertaining to the value and error of each bin in the ratio (hist/normaliser).
    '''

    h1dclone = hist.Clone(hist.GetName()+"_clone")
    h1dclone.Divide(normaliser)

    normaliser_errors = []
    norm_hand_errors = []
    for binn in range(0,h1dclone.GetXaxis().GetNbins()):
        normaliser_errors.append(h1dclone.GetBinError(binn+1))
        # print(h1dclone.GetBinContent(binn+1),hist.GetBinContent(binn+1))
        # raw_input()
        # norm_hand_errors.append(h1dclone.GetBinContent(binn+1)*1/math.sqrt(hist.GetBinContent(binn+1)))

    # print(normaliser_errors)
    # print(norm_hand_errors)

    n1d_num = hist2array(h1dclone)
    n1d_num = np.append(n1d_num,1.0)

    norm_errors = np.asarray(normaliser_errors)
    # norm_hand_errors = np.asarray(norm_hand_errors)

    return n1d_num,norm_errors


class Histogram:
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
        self.observable_value   = kwargs["observable_value"] if "observable_value"  in kwargs else None 
        self.observable_error   = kwargs["observable_error"] if "observable_error"  in kwargs else None
        self.xaxis_label        = kwargs["xaxis_label"]      if "xaxis_label"       in kwargs else None
        self.yaxis_label        = kwargs["yaxis_label"]      if "yaxis_label"       in kwargs else None
        self.individual_normalisation = kwargs["individual_normalisation"] if "individual_normalisation" in kwargs else True

        xx,xc,yy,errors=preplot(hist,self.individual_normalisation)

        self.x_bins         = xx
        self.xc_bins        = xc
        self.ydata          = yy
        self.errors         = errors
        self.binning        = self.x_bins

        if "normaliser" in kwargs:
            yn,norm_errors = normalised_histograms(hist,normaliser)
            self.norm_data      = yn
            self.norm_errors    = norm_errors

        self.colour         = kwargs["colour"]      if "colour"      in kwargs else None
        self.Xaxis_title    = kwargs["Xaxis_title"] if "Xaxis_title" in kwargs else None

    def generate_normalised(self,normaliser):
        # An alternative normalising function which is an attribute function of the Histogram3 class
        # Has been superceded by other ratio plot function
        yn,norm_errors =normalised_histograms(self.ROOT_hist,normaliser.ROOT_hist)
        self.norm_data      = yn
        self.norm_errors    = norm_errors
        self.new_norm_data = np.where(self.norm_data == 0.0, 1, self.norm_data)


    def set_colour(self,colour):
        self.colour = colour

    def set_legend_entry(self,legend_entry):
        self.legend_entry = legend_entry

    def set_binning(self,binning):
        self.binning = binning
        if not hasattr(self,"axis_limits"):
            self.axis_limits = [0,len(self.binning)-1]

    def set_parameters(self,**kwargs):
        if "colour" in kwargs: 
            self.set_colour(kwargs["colour"])
        if "legend_entry" in kwargs:
            self.set_legend_entry(kwargs["legend_entry"])
