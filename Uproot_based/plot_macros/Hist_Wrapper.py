import matplotlib.pyplot as plt
import mplhep as hep
import hist
import numpy as np
from hist.intervals import ratio_uncertainty
import boost_histogram as bh
import uproot


class Hist_Object:

    '''
    A basic wrapper for storing a boost-histogram and associated bin errors
    Also required to contain specific plotting information e.g. colour and legend label
    '''

    def __init__(self,Histogram,errors,**kwargs):

        self.Histogram = Histogram 
        self.errors_up = errors[1]
        self.errors_down = errors[0]

        self.Set_Features(**kwargs)

    def Set_Features(self,**kwargs):

        self.colour = kwargs["colour"] if "colour" in kwargs else "black"
        self.label  = kwargs["label"]  if "label"  in kwargs else ""



class Histogram_Wrapper:

    ''' 
    Larger wrapper for Boost-Histogram object generated from Uproot parsing of ROOT file 
    Contains methods for extracting histogram from Uproot file and constructing boost-histogram 
    Stores the above Hist_Objects for both normalised and unnormalised cases
    '''

    def __init__(self,tree,branch_name,**kwargs):

        self.TTree = tree
        self.branch_name = branch_name
        self.number_of_bins = 26

        # Extract histogram for Uproot file TTree
        self.df = self.Branch2DF(self.TTree,self.branch_name)

        self.Generate_Binning(kwargs)

        # Generate boost_histogram, and wrap with errors
        boost_hist = self.Generate_Histogram(self.df,self.binning)
        boost_hist_errors = self.errors(boost_hist)
        self.UnNorm_Hist = Hist_Object(boost_hist,boost_hist_errors)
       
       # Generate normalised histogram, and wrap with errors
        self.Norm_Hist    = self.Do_Normalisation(boost_hist)

        # Plot features
        self.colour = kwargs["colour"] if "colour" in kwargs else None
        self.UnNorm_Hist.colour,self.Norm_Hist.colour = self.colour,self.colour


    def Generate_Binning(self,kwargs):
        if "binning" in kwargs:
            self.binning = kwargs["binning"]
            self.AutoBin = False

        else:
            self.AutoBin = True
            maxH,minH = self.Get_Extrema(self.df)
            self.binning = np.linspace(minH,maxH,self.number_of_bins)


    def Change_Defaults(self,**kwargs):

        self.number_of_bins = kwargs["number_of_bins"] if "number_of_bins" in kwargs else self.number_of_bins


    @staticmethod
    def errors(boost_hist):
        
        ''' Computes the associated bin errors for a non-divided histogram only'''
        return [np.sqrt(boost_hist.variances()),np.sqrt(boost_hist.variances())]


    @staticmethod
    def Get_Extrema(df):

        ''' Computes the largest and smallest value in the histogram to generate histogram bounds'''
        import math
        return float(math.ceil(df.max())),float(math.floor(df.min()))


    @staticmethod
    def Generate_Histogram(df,bins):

        ''' Passes the datafram into histogram form'''
        h = bh.Histogram(bh.axis.Variable(bins))
        h.fill(df)
        return h

    @staticmethod
    def Branch2DF(TTree,branch_name):

        ''' Extracts the branch from TTree and turns into Pandas dataframe'''
        return TTree[branch_name].array(library="pd")


    @staticmethod
    def Do_Normalisation(boost_hist):

        '''Performs normalisation of histogram '''

        Normalised_Histogram     = boost_hist *(1/boost_hist.sum())
        Normalised_Uncertainties = ratio_uncertainty(boost_hist , boost_hist.sum(),"poisson")

        return Hist_Object(Normalised_Histogram,Normalised_Uncertainties)


