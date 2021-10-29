# EFT plotter

# Design features - swap orientation: vertical or horizontal
# Should be run on Python3.6 / Python3.7

# Pass a pandas dataframe with a set of Wilson coefficients ad corresponding values

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mplhep as hep

"""
Structure of the DataFrame
WC: Linear, Linear+Quadratic, ...
Each part should then be a list of tuples: if there is a single region found, more if multiple (per operator)
Each tuple should be of the form (global mode, lower bound, upper bound)
"""
"""
The data format input could be a json file nested in the structure (EFT model,Wilson coefficient,number of bounds), 
    with each entry containing (value, lower bound, upper bound).
"""



class EFT_Plot:

    """
    Main EFT Plot Class
    Takes a pandas DataFrame as input
    """

    def __init__(self,df,**kwargs):

        self.df = df
        self.orientation = kwargs["orientation"] if "orientation" in kwargs else "vertical"
        self.colours = kwargs["colours"] if "colours" in kwargs else plt.rcParams['axes.prop_cycle'].by_key()['color']
        
        # Assign which columns to plot
        if "to_plot" in kwargs:
            if kwargs["to_plot"]=="all": 
                self.to_plot = self.df.columns.tolist()
            if isinstance(kwargs["to_plot"],list) and all([x in self.df.columns.tolist() for x in kwargs["to_plot"]]):
                self.to_plot = kwargs["to_plot"]
        else:
            self.to_plot = self.df.columns.tolist()

        self.number2plot = len(self.to_plot)
        self.generate_wc_ordinates()


    def get_points(self,tup):
            value       = tup[0]
            lower_bound = tup[1]
            upper_bound = tup[2]

            lower_error = value - lower_bound
            upper_error = upper_bound - value

            error_array = np.array([[lower_error ,upper_error]]).T

            return value,error_array


    def generate_wc_ordinates(self):
        assert self.number2plot < 5 and isinstance(self.number2plot,int), "Too many branches to plot"
        if self.number2plot==1:
            self.wc_array = [0]
        if self.number2plot==2:
            self.wc_array = [-0.05,0.05]
        if self.number2plot==3:
            self.wc_array = [-0.15,0,0.15]
        if self.number2plot==4:
            self.wc_array = [-0.15,-0.05,0.05,0.15]


    def make_plot(self,**kwargs):

        """Makes plot defined by orientation, which can be pre-set or passed to this function"""

        if "orientation" in kwargs: self.orientation=kwargs["orientation"]
        assert self.orientation, "Orientation of plot not defined"
        if self.orientation=="hor":
            fig,ax=self.make_horizontal_plot()
        elif self.orientation=="vert":
            fig,ax=self.make_vertical_plot()
        return fig,ax


    def make_vertical_plot(self):
        
        fig, ax = plt.subplots()

        y_points = np.arange(0,self.df.shape[0]+1)

        for col,yp,color in zip(self.to_plot,self.wc_array,self.colours): # Loop over columns
            for i,(index,row) in enumerate(self.df.iterrows()):
                for tup in row[col]:
                    if tup !=None:
                        value,asymmetric_error = self.get_points(tup)
                        plt.errorbar(x=value,y=i+1+yp,xerr=asymmetric_error,fmt='x',capsize=5,color=color)

        ax.set_yticks(y_points[1:])
        ax.set_yticklabels(self.df.index)
        ax.set_ylim(0,len(y_points))

        ax.tick_params(axis='y', which='minor', left=False, right=False)

        self.make_legend()
        plt.xlabel("Value")
        plt.ylabel("Wilson Coefficients")
        return fig,ax


    def make_horizontal_plot(self):

        fig, ax = plt.subplots()

        self.fig , self.ax = fig,ax

        x_points = np.arange(0,self.df.shape[0]+1)

        for col,xp,color in zip(self.to_plot,self.wc_array,self.colours):
            for i,(index,row) in enumerate(self.df.iterrows()):
                for tup in row[col]:
                    if tup !=None:
                        value,asymmetric_error = self.get_points(tup)
                        plt.errorbar(x=i+1+xp,y=value,yerr=asymmetric_error,fmt='x',capsize=5,color=color)

        ax.set_xticks(x_points[1:])
        ax.set_xticklabels(self.df.index)
        ax.set_xlim(0,len(x_points))

        ax.tick_params(axis='x', which='minor', bottom=False, top=False)

        self.make_legend()

        plt.xlabel("Wilson Coefficients")
        plt.ylabel("Value")
        return fig,ax

    def make_legend(self):
        from matplotlib.lines import Line2D

        handles, labels = plt.gca().get_legend_handles_labels()
        for attrib,colour in zip(self.to_plot,self.colours):
            line = Line2D([0], [0], label=attrib, color=colour)
            handles.extend([line])
        handles.reverse()
        plt.legend(handles=handles)

    def plot_single_values(self,df2):
        """Must same structure of dataframe but with the global modes, this could be contained separately"""
        pass
        
        

class LHC_EFT_Plot(EFT_Plot):

    """
    A daughter class for making the EFT plots in the style of the LHC experiments
    """

    allowed_experiment_styles = ["ATLAS","ALICE","LHCb2","CMS","ATLASTex"]

    def initialise_LHC_plot(self,experiment):

        assert any([experiment == x for x in self.allowed_experiment_styles]), "Experiment style not defined"

        if   experiment=="ATLAS": plt.style.use(hep.style.ATLAS) # This is the correct syntax for Pytohn3.6.9 version (mplhep 0.2.8)
        elif experiment=="CMS"  : plt.style.use(hep.style.CMS)
        elif experiment=="ALICE": plt.style.use(hep.style.ALICE)
        elif experiment=="LHCb2": plt.style.use(hep.style.LHCb2)
        elif experiment=="ATLASTex": 
            print("This is not supported because do not have a working TexLive distribution")
            # plt.style.use(hep.style.ATLASTex) # T

    def include_metadata(self,text,data,lumi,year):
        hep.atlas.label(text, data=data, lumi=lumi, year=year)

    def __init__(self,df,experiment,**kwargs,):
        
        super().__init__(df,**kwargs)
        self.experiment = experiment

        self.initialise_LHC_plot(experiment)














