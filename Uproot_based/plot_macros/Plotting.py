import matplotlib.pyplot as plt
import mplhep as hep
import hist
import numpy as np
from hist.intervals import ratio_uncertainty
import boost_histogram as bh
import uproot

from Hist_Wrapper import Histogram_Wrapper, Hist_Object



class HEP_Plot:

    allowed_experiment_styles = ["ATLAS","ALICE","LHCb2","CMS","ATLASTex"]

    def Add_ATLAS_Label(self,label_text,**kwargs):

        ax = self.axes[0]

        if self.plot_design in ["ATLAS","ATLASTex"]:

            loc = kwargs["loc"] if "loc" in kwargs else 1

            if loc == 1:
                yaxis_limits = ax.get_ylim()
                ax.set_ylim(yaxis_limits[0],yaxis_limits[1]*1.2)
            l1 = hep.atlas.text(label_text,ax=ax,loc=loc)

            if "specific_location" in kwargs:
                #Defined from first word
                x_diff,y_diff = l1[1]._x - l1[0]._x , l1[1]._y - l1[0]._y

                l1[0]._x = kwargs["specific_location"][0]
                l1[0]._y = kwargs["specific_location"][1]
                l1[1]._x = kwargs["specific_location"][0] + x_diff
                l1[1]._y = kwargs["specific_location"][1] + y_diff

 
    def Initialise_LHC_Plot(self,experiment):

        assert any([experiment == x for x in self.allowed_experiment_styles]), "Experiment style not defined"

        hep.style.use(experiment)#, {'xtick.direction': 'out'}])


    def Initialise_Seaborn_Plot(self,**kwargs):

        import seaborn as sns
        if "style" in kwargs:
            sns.set_style(kwargs["style"])
        else:
            sns.set_style("dark")

    def Add_Histograms(self,histograms2add: list):
        self.list_of_histograms = self.list_of_histograms + histograms2add


    def Initalise_Plot_Design(self,design,**kwargs):

        self.plot_design = design

        allowed_experiment_styles = ["ATLAS","ALICE","LHCb2","CMS","ATLASTex"]

        if any([design == x for x in allowed_experiment_styles]):
            self.Initialise_LHC_Plot(design)
        elif design=="Seaborn":
            self.Initialise_Seaborn_Plot(**kwargs)


    @staticmethod
    def Steps_Filled_Erros(ax,Hist_Ob):#Histogram,error_up,error_down): # Need to pass error up and error down

        """For making a histogram plot with steps, where the errors are filled lighter bars above and below the step """

        Histogram = Hist_Ob.Histogram 

        hep.histplot(Histogram, ax=ax, stack=False, histtype='step',color=Hist_Ob.colour)


        errps = {'hatch':'////', 'facecolor':'blue', 'lw': 0, 'alpha': 0.4}
        # errps = {'alpha':0.4}

        ax.stairs(
            values=Histogram.values() + Hist_Ob.errors_up,
            baseline=Histogram.values() - Hist_Ob.errors_down,
            edges=Histogram.axes[0].edges, label='Stat. unc.',fill=True,alpha=0.25,color=Hist_Ob.colour)



    def __init__(self,plot_title,**kwargs):
        self.plot_title = plot_title
        self.list_of_histograms = []
        self.Normalised = True
        self.fig  = None
        self.axes = None

        if "plot_design" in kwargs:
            self.plot_design = kwargs["plot_design"]
            self.Initalise_Plot_Design(self.plot_design,**kwargs) # Is there a way to sift a subset of kwargs i.e. **kwargs["seaborn_design_parameters"]
        if "list_of_histograms" in kwargs:
            self.list_of_histograms = kwargs["list_of_histograms"]
        if "plot_normalised" in kwargs and not kwargs["plot_normalised"]:
            self.Normalised = False





class Single_Plot(HEP_Plot):
    pass




class Ratio_Plot(HEP_Plot):

    '''
    The Ratio_Plot inherits from the parent HEP_Plot class
    The methods here are:
        - the computation of ratio histograms
        - the initialistion of the mpl object
        - the filling of the plot
    '''

    def __init__(self,plot_title,**kwargs):
        super().__init__(plot_title,**kwargs) 
        self.divisor = kwargs["divisor"] if "divisor" in kwargs else None

    @staticmethod
    def Compute_Ratio(hist1,hist2):
        ratio_hist = hist1/hist2
        ratio_uncertainties = ratio_uncertainty(hist1,hist2,"poisson")
        return Hist_Object(ratio_hist,ratio_uncertainties)#[0],ratio_uncertainties[1])
        

    def Make_Plot(self):

        assert len(self.list_of_histograms) != 0, "No histograms passed to plot" 

        # Initialise the plot
        fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)

        self.fig = fig
        self.axes = (ax,rax)



        # Select whether to do normalisation

        for H in self.list_of_histograms:

            print(H.branch_name)

            if self.Normalised == False:

                self.Steps_Filled_Erros(ax=ax,Hist_Ob=H.UnNorm_Hist)
                ratio_obj = self.Compute_Ratio(H.UnNorm_Hist.Histogram,self.divisor.UnNorm_Hist.Histogram)
                ratio_obj.Set_Features(colour=H.colour)
                self.Steps_Filled_Erros(ax=rax,Hist_Ob=ratio_obj)

            elif self.Normalised == True:
                self.Steps_Filled_Erros(ax=ax,Hist_Ob=H.Norm_Hist)
                ratio_obj = self.Compute_Ratio(H.Norm_Hist.Histogram,self.divisor.Norm_Hist.Histogram)
                ratio_obj.Set_Features(colour=H.colour)
                self.Steps_Filled_Erros(ax=rax,Hist_Ob=ratio_obj)


        return plt









