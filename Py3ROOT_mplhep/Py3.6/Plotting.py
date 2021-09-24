import matplotlib.pyplot as plt
import mplhep as hep
import hist
import numpy as np
from hist.intervals import ratio_uncertainty
import boost_histogram as bh
import uproot
from matplotlib.lines import Line2D


from PyHist_Class import PyHist,Histogram_Wrapper



class HEP_Plot:

    allowed_experiment_styles = ["ATLAS","ALICE","LHCb2","CMS","ATLASTex"]

    def Add_ATLAS_Label(self,label_text,**kwargs):

        assert self.axes,"Axes not defined yet. Add label after plot is made"
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

        # hep.style.use(experiment)#, {'xtick.direction': 'out'}])
        if   experiment=="ATLAS": plt.style.use(hep.style.ATLAS) # This is the correct syntax for Pytohn3.6.9 version (mplhep 0.2.8)
        elif experiment=="CMS"  : plt.style.use(hep.style.CMS)
        elif experiment=="ALICE": plt.style.use(hep.style.ALICE)
        elif experiment=="LHCb2": plt.style.use(hep.setyle.LHCb2)


    def Initialise_Seaborn_Plot(self,**kwargs):

        import seaborn as sns
        if "style" in kwargs:
            sns.set_style(kwargs["style"])
        else:
            sns.set_style("dark")

    def Add_Histograms(self,histograms2add: list):
        self.list_of_histograms = self.list_of_histograms + histograms2add


    def Initialise_Plot_Design(self,design,**kwargs):

        self.plot_design = design

        allowed_experiment_styles = ["ATLAS","ALICE","LHCb2","CMS","ATLASTex"]

        if any([design == x for x in allowed_experiment_styles]):
            self.Initialise_LHC_Plot(design)
        elif design=="Seaborn":
            self.Initialise_Seaborn_Plot(**kwargs)


    def Customise_Legend(self):
        pass


    @staticmethod
    def Steps_Filled_Errors_Root(ax,ROOT_hist):
        pass

    @staticmethod
    def Step_Errorbar_Line(ax,PH):

        x_binning = PH.Bin_Edges
        values    = np.concatenate((PH.Bin_Values,np.asarray([0])), axis=0)
        errors    = PH.Bin_Errors

        ax.plot(x_binning, values,drawstyle="steps-post",color=PH.colour,label=PH.Name,linewidth=PH.linewidth)#Hist_Wrapper.linewidth)
        ax.vlines(x_binning[0],0,values[0],color=PH.colour,linewidth=PH.linewidth)#Hist_Wrapper.linewidth)



    # @staticmethod
    # def Step_Errorbar_Line2(ax,Hist_Wrapper,Normalised):

    #     if Normalised:
    #         PyHist = Hist_Wrapper.Norm_PyWrap_Hist
    #     else:
    #         PyHist = Hist_Wrapper.UnNorm_PyWrap_Hist

    #     x_binning = PyHist.Bin_Edges
    #     values    = np.concatenate((PyHist.Bin_Values,np.asarray([0])), axis=0)
    #     errors    = PyHist.Bin_Errors

    #     ax.plot(x_binning, values,drawstyle="steps-post",color=Hist_Wrapper.colour,label=PyHist.Name,linewidth=2)#Hist_Wrapper.linewidth)
    #     ax.vlines(x_binning[0],0,values[0],color=Hist_Wrapper.colour,linewidth=2)#Hist_Wrapper.linewidth)


    @staticmethod
    def Steps_Filled_Erros(ax,Hist_Wrapper,Normalised):#Histogram,error_up,error_down): # Need to pass error up and error down

        """For making a histogram plot with steps, where the errors are filled lighter bars above and below the step """

        # Histogram = Hist_Ob.Histogram
        # print(Hist_Wrapper.__dict__)
        # input()
        Hist = Hist_Wrapper.Norm_hist if Normalised else Hist_Wrapper.ROOT_hist

        hep.histplot(Hist, ax=ax, stack=False, histtype='step',color=Hist_Wrapper.colour,label=Hist_Wrapper.legend_entry,lw=1.0)

        # Not used
        errps = {'hatch':'////', 'facecolor':'blue', 'lw': 0, 'alpha': 0.4}


        # bin_edges = [xx_axis.GetBinUpEdge(binn) for x in ]
        x_binning = Hist_Wrapper.Bin_Edges(Hist)
        values    = Hist_Wrapper.Bin_Values(Hist)
        errors    = Hist_Wrapper.Bin_Errors(Hist)
        ax.stairs(
            values=values + errors,
            baseline=values - errors,
            edges=x_binning, fill=True,alpha=0.25,color=Hist_Wrapper.colour)



    def __init__(self,plot_title,**kwargs):
        self.plot_title = plot_title
        self.list_of_histograms = []

        norms = ["Normalised","normalised","Normalise","normalise"]
        self.Normalised = False
        for x in norms:
            if x in kwargs:
                self.Normalised = kwargs[x]

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



class Ratio_Plot_ROOT(HEP_Plot):

    def __init__(self,plot_title,**kwargs):
        super().__init__(plot_title,**kwargs) 
        self.divisor = kwargs["divisor"] if "divisor" in kwargs else None
        self.Do_Ratio()

    @staticmethod
    def Compute_Ratio(ROOT_hist_numer,ROOT_hist_denom):
        d_hist = ROOT_hist_numer.Clone()
        d_hist.Divide(ROOT_hist_numer,ROOT_hist_denom)
        return d_hist

    ###### Constructing list of ratio histograms

    def Construct_Ratio_Histograms(self,hist_type):   

        self.list_of_ratio_histograms = []

        for HW in self.list_of_histograms:
            hist = self.Compute_Ratio(getattr(HW,hist_type),getattr(self.divisor,hist_type))
            wrapped=Histogram_Wrapper.Create_Wrapper(hist,"name",colour=HW.colour,linewidth=HW.linewidth)
            self.list_of_ratio_histograms.append(wrapped)

    def Do_Ratio(self):

        assert self.divisor,"Divisor histogram not set"   

        if self.Normalised:
            self.Construct_Ratio_Histograms("Norm_ROOT_hist")
        else:
            self.Construct_Ratio_Histograms("UnNorm_ROOT_hist")

    ###########################################################


    def Make_Errorbar_Line_Plot(self):

        fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)
        self.fig = fig
        self.axes = (ax,rax)

        # Top plot
        for PH in self.list_of_histograms:
            HW = PH.Norm_PyWrap_Hist if self.Normalised else PH.UnNorm_PyWrap_Hist
            self.Step_Errorbar_Line(ax,HW)

        for HW in self.list_of_ratio_histograms:
            self.Step_Errorbar_Line(rax,HW)

        # Ratio

        return plt

        # if self.Normalised:
        #     Steps_Filled_Erros(ax,Hist_Ob)
        # else:
        #     Steps_Filled_Erros(ax,Hist_Ob)


        # pass

       

        # if not self.Normalised:
        #     for HW in self.list_of_histograms:
        #         hist = self.Compute_Ratio(HW.ROOT_hist,self.divisor.ROOT_hist)
        #         self.ratios2plot.append(Ratio_Object(hist,HW.colour))

        # elif self.Normalised:
        #     for HW in self.list_of_histograms:
        #         self.ratios2plot.append(self.Compute_Ratio(HW.Norm_hist,self.divisor.Norm_hist))







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
        ratio_uncertainties = ratio_uncertainty(hist1.view(),hist2.view(),"poisson")
        # print(ratio_uncertainties)
        # input()
        return Hist_Object(ratio_hist,ratio_uncertainties)#[0],ratio_uncertainties[1])

    def Axis_Labels(self,dic_of_labels):
        self.axes[1].set_xlabel(dic_of_labels["x"])
        self.axes[1].set_ylabel(dic_of_labels["y2"])
        self.axes[0].set_ylabel(dic_of_labels["y1"])

    def Axis_XTick_Labels(self,labels,**kwargs):
        # print(self.axes[1].get_xticklabels)
        # input()
        self.axes[1].set_xticklabels(labels)
        

    def Make_Step_Fill_Plot(self):

        assert len(self.list_of_histograms) != 0, "No histograms passed to plot" 

        # Initialise the plot
        fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)

        self.fig = fig
        self.axes = (ax,rax)

        # Select whether to do normalisation
        legend_elements = []

        for H in self.list_of_histograms:

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

            # Do the legend part here
            legend_elements.append(Line2D([0],[0],color=H.colour,lw=2,label=H.label))

        ax.legend(handles=legend_elements)#, loc='center')

        # ax.legend()
        return plt









