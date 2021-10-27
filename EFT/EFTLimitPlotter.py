# EFT plotter

# Design features - swap orientation: vertical or horizontal
# Should be run on Python3.6 / Python3.7

# Pass a pandas dataframe with a set of Wilson coefficients ad corresponding values


import matplotlib.pyplot as plt

import numpy as np
from numpy.core.defchararray import upper
import pandas as pd
import mplhep as hep


"""
Structure of the DataFrame
WC: Linear, Linear+Quadratic, ...
Each part should then be a list of tuples: if there is a single region found, more if multiple (per operator)
Each tuple should be of the form (global mode, lower bound, upper bound)
"""




data = {"ctG":[(0,-1,1),(0,-3,3)],"ctZ":[(2,-3,8),None],"ctH":[(6,2,10),None]}

# for tup_list in data.values():
#     for tup in tup_list:
#         for x in list(tup):
#             print(x)
#             input()
#         # for x in list(data[wc][tup]):
#         #     print(x)
#         #     input()
# # data = {"ctG":(())}

df = pd.DataFrame.from_dict(data).T

df.columns=["Linear","Linear + Quadratic"]


class EFT_Plot:

    def __init__(self,df,orientation):
        self.df = df
        self.orientation = orientation

    def get_points(self,column,index,row):
            wilson_coef=index
            value=row[column][0]
            lower_bound = row[column][1]
            upper_bound = row[column][2]

            lower_error = value - lower_bound
            upper_error = upper_bound - value

            error_array = np.array([[lower_error ,upper_error]]).T

            return value,error_array


    def make_vertical_plot(self):

        fig, ax = plt.subplots()

        y_points = np.arange(0,df.shape[0]+1)

        for i,(index,row) in enumerate(self.df.iterrows()):

            value,asymmetric_error = self.get_points("Linear",index,row)
            plt.errorbar(x=value,y=i+1,xerr=asymmetric_error,fmt='x')

        ax.set_yticks(y_points[1:])
        ax.set_yticklabels(self.df.index)
        ax.set_ylim(0,len(y_points))

        ax.tick_params(axis='y', which='minor', left=False, right=False)

        plt.ylabel("Wilson Coefficients")
        return plt,fig,ax

    def make_horizontal_plot(self):

        fig, ax = plt.subplots()

        x_points = np.arange(0,df.shape[0]+1)

        for i,(index,row) in enumerate(self.df.iterrows()):

            value,asymmetric_error = self.get_points("Linear",index,row)
            plt.errorbar(x=i+1,y=value,yerr=asymmetric_error,fmt='x')

        ax.set_xticks(x_points[1:])
        ax.set_xticklabels(self.df.index)
        ax.set_xlim(0,len(x_points))

        ax.tick_params(axis='x', which='minor', bottom=False, top=False)

        plt.xlabel("Wilson Coefficients")
        return plt,fig,ax






class LHC_EFT_Plot(EFT_Plot):

    allowed_experiment_styles = ["ATLAS","ALICE","LHCb2","CMS","ATLASTex"]

    def initialise_LHC_plot(self,experiment):


        assert any([experiment == x for x in self.allowed_experiment_styles]), "Experiment style not defined"

        # hep.style.use(experiment)#, {'xtick.direction': 'out'}])
        if   experiment=="ATLAS": plt.style.use(hep.style.ATLAS) # This is the correct syntax for Pytohn3.6.9 version (mplhep 0.2.8)
        elif experiment=="CMS"  : plt.style.use(hep.style.CMS)
        elif experiment=="ALICE": plt.style.use(hep.style.ALICE)
        elif experiment=="LHCb2": plt.style.use(hep.style.LHCb2)
        elif experiment=="ATLASTex": 
            print("This is not supported because do not have a working TexLive distribution")
            # plt.style.use(hep.style.ATLASTex) # T


    def __init__(self,df,orientation,experiment):
        super().__init__(df,orientation)
        self.experiment = experiment

        self.initialise_LHC_plot(experiment)


x = LHC_EFT_Plot(df=df,orientation="hor",experiment="ATLAS")
plt,fig,ax=x.make_vertical_plot()
hep.atlas.text("Internal",loc=0)
plt.show()
input()






