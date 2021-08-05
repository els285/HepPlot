import matplotlib.pyplot as plt
import mplhep as hep
import hist
import numpy as np
from hist.intervals import ratio_uncertainty
import boost_histogram as bh
import uproot


class Histogram_Wrapper:

    ''' Wrapper for Boost-Histogram object generated from Uproot parsing of ROOT file '''

    def __init__(self,tree,branch_name,**kwargs):

        self.TTree = tree
        self.branch_name = branch_name

        # self.normalise = kwargs["normalise"] if "normalise" in kwargs else self.normalise
        self.number_of_bins = 26

        self.df = self.Branch2DF(self.TTree,self.branch_name)


        if "binning" in kwargs:
            self.binning = kwargs["binning"]
            self.AutoBin = False

        else:
            self.AutoBin = True
            maxH,minH = self.Get_Extrema(self.df)
            self.binning = np.linspace(minH,maxH,self.number_of_bins)

        self.Histogram = self.Generate_Histogram(self.df,self.binning)
        self.Do_Normalisation()


        # self.ratio_histograms = {}

    # @classmethod
    def Change_Defaults(self,**kwargs):

        self.number_of_bins = kwargs["number_of_bins"] if "number_of_bins" in kwargs else self.number_of_bins


    # @staticmethod
    def errors(self):

        return [np.sqrt(self.Histogram.variances()),np.sqrt(self.Histogram.variances())]

        # if self.Histogram.variances() != None:
        #     return np.sqrt(self.Histogram.variances())
        # else:
        #     return None


    @staticmethod
    def Get_Extrema(df):
        import math
        return float(math.ceil(df.max())),float(math.floor(df.min()))


    @staticmethod
    def Generate_Histogram(df,bins):
        h = bh.Histogram(bh.axis.Variable(bins))
        h.fill(df)
        return h

    @staticmethod
    def Branch2DF(TTree,branch_name):
        return TTree[branch_name].array(library="pd")


    # def Generate_Ratio(self,divisor):
    #     self.ratio_histograms[divisor.Name] = self.Histogram/divisor.Histogram

    def Do_Normalisation(self):
        self.Normalised_Histogram     = self.Histogram / self.Histogram.sum()
        self.Normalised_Uncertainties = ratio_uncertainty(self.Histogram , self.Histogram.sum(),"poisson")



class HEP_Plot:

    # Design parameters
    # def Initialise_ATLAS_Plot(self):

    #     fig, ax, rax =  self.Initialise_LHC_Plot("ATLAS")
    #     l1 = hep.atlas.text("Internal",ax=ax,loc=0)

    #     # return fig,ax,rax

    def Initialise_LHC_Plot(self,experiment):

        allowed_experiment_styles = ["ATLAS","ALICE","LHCb2","CMS","ATLASTex"]
        assert any([experiment == x for x in allowed_experiment_styles]), "Experiment style not defined"

        hep.style.use(experiment)#, {'xtick.direction': 'out'}])
        # return fig,ax,rax


    def Initialise_Seaborn_Plot(self,**kwargs):

        import seaborn as sns
        if "style" in kwargs:
            sns.set_style(kwargs["style"])
        else:
            sns.set_style("dark")
        # return fig,ax,rax

    def Add_Histograms(self,histograms2add: list):
        self.list_of_histograms = self.list_of_histograms + histograms2add



    def Initalise_Plot_Design(self,design,**kwargs):

        self.plot_design = design

        allowed_experiment_styles = ["ATLAS","ALICE","LHCb2","CMS","ATLASTex"]

        # if design=="ATLAS":
        #     self.Initialise_ATLAS_Plot()
        if any([design == x for x in allowed_experiment_styles]):
            self.Initialise_LHC_Plot(design)
        elif design=="Seaborn":
            self.Initialise_Seaborn_Plot(**kwargs)


    @staticmethod
    def Steps_Filled_Erros(ax,Histogram,error_up,error_down): # Need to pass error up and error down

        """For making a histogram plot with steps, where the errors are filled lighter bars above and bellow the step """
        # pass
        hep.histplot(Histogram, ax=ax, stack=False, histtype='step')


        # errps = {'hatch':'////', 'facecolor':'none', 'lw': 0, 'color': 'k', 'alpha': 0.4}
        errps = {'color':'k'}

        ax.stairs(
            values=Histogram.values() + error_up,
            baseline=Histogram.values() - error_down,
            edges=Histogram.axes[0].edges, **errps, label='Stat. unc.')



    def __init__(self,plot_title,**kwargs):
        self.plot_title = plot_title
        self.list_of_histograms = []

        if "plot_design" in kwargs:
            self.plot_design = kwargs["plot_design"]
            self.Initalise_Plot_Design(self.plot_design,**kwargs) # Is there a way to sift a subset of kwargs i.e. **kwargs["seaborn_design_parameters"]
        if "list_of_histograms" in kwargs:
            self.list_of_histograms = kwargs["list_of_histograms"]






# class Histogram_Plot(HEP_Plot):
#     pass



# class LHC_Plot(HEP_Plot):




#     def Set_Experiment_Style(self,experiement_style):      
#         allowed_experiment_styles = ["ATLAS","ALICE","LHCb2","CMS","ATLASTex"]
#         assert any([experiment == x for x in allowed_experiment_styles]), "Experiment style not defined"
#         self.style = experiement_style


#     def Set_Label_Content(label_content,**kwargs):
#         self.label_content  = label_content
#         self.label_location = kwargs["label_location"] if "label_location" in kwargs else None


#     def __init__(self,plot_title,list_of_histograms,experiement_style,**kwargs):
        
#         super().__init__(plot_title,list_of_histograms)
        
#         self.Set_Experiment_Style(experiement_style)
        
#         if "label_content" in kwargs: 
#             Set_Label_Content(**kwargs)



from dataclasses import dataclass
from typing import Any

@dataclass
class Hist_Object:
    Histogram: Any
    error_up: Any
    error_down: Any
    colour: str 
    label: str



class Single_Plot(HEP_Plot):
    pass




class Ratio_Plot(HEP_Plot):

    def __init__(self,plot_title,**kwargs):
        super().__init__(plot_title,**kwargs) 
        self.divisor = kwargs["divisor"] if "divisor" in kwargs else None

    def Divide_Hists(self):

        for hist in self.list_of_histograms:
            hist.Generate_Ratio(self.divisor)

    @staticmethod
    def Compute_Ratio(hist1,hist2):
        ratio_hist = hist1/hist2
        ratio_uncertainties = ratio_uncertainty(hist1,hist2,"poisson")
        return Hist_Object(ratio_hist,ratio_uncertainties[0],ratio_uncertainties[1])
        

    # def Compute_Errors():
    #     pass

    def Make_Plot(self):

        assert len(self.list_of_histograms) != 0, "No histograms passed to plot" 

        # Initialise the plot
        fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)

        # Select whether to do normalisation
        # ax_hists, rax_hists = [],[]
        if self.Normalised == False:
            hist2use   = self.Histogram
            errors2use = self.errors()
        elif self.Normalised == True:
            hist2use  = self.Normalised_Histogram
            errors2use = self.normalised_uncertainties



    def Make_Unnormalised_Plot(self):

        fig,ax,rax = self.Initialise_ATLAS_Plot()


        self.Steps_Filled_Erros(ax=ax,Histogram=self.list_of_histograms[0].Histogram,error_up=self.list_of_histograms[0].errors(),error_down=self.list_of_histograms[0].errors())


        # plt.show()
        # input()
        hep.histplot([h.Histogram for h in self.list_of_histograms], ax=ax, stack=False, histtype='step', label=["MC1", "MC2"])

        # Returns a list of tuples with elements (normalised_histogram  ,  2d array of errors)
        ratio_plot_objects = [self.Compute_Ratio(h.Histogram,self.divisor.Histogram) for h in self.list_of_histograms]
        print(ratio_plot_objects)
        input()
        # hep.histplot([h[0] for h in ratio_plot_objects], ax=rax, stack=False, histtype='step',yerr=[h[1] for h in ratio_plot_objects], label=["MC1", "MC2"])
        # l1 = hep.atlas.text(text='Internal',loc=1)

        self.Steps_Filled_Erros(ax=rax,Histogram=self.list_of_histograms[0].Histogram,error_up=self.list_of_histograms[0].errors(),error_down=self.list_of_histograms[0].errors())


        return plt



    def Make_Normalised_Plot(self):

        fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)

        # input()
        self.Steps_Filled_Erros(ax=ax,Histogram=self.list_of_histograms[0].normalised_histogram,error_up=self.list_of_histograms[0].normalised_uncertainties[0],error_down=self.list_of_histograms[0].normalised_uncertainties[1])

        ratio_plot_objects = [self.Compute_Ratio(h.Histogram,self.divisor.Histogram) for h in self.list_of_histograms]
        self.Steps_Filled_Erros(ax=rax,Histogram=ratio_plot_objects[0].Histogram,error_up=ratio_plot_objects[0].error_up,error_down=ratio_plot_objects[0].error_down)
        plt.show()
        input()

        hep.histplot([h.normalised_histogram for h in self.list_of_histograms], ax=ax, stack=False, histtype='fill', label=["MC1", "MC2"])

        return plt


    def Make_Plot(self):
        pass


        # Call appropriate plotting design function - ATLAS, LaTeX, Seaborn etc

        # Call appropriate plotting macro




def main():

    file1 = uproot.open("/home/ethan/Documents/Qualification_Task/Full_Tests/ttbar/Inclusive_Smearings/ttbar_LEPTONS_WITH_EFFICIENCY_july25.root")
    tree1 = file1["smeared"]

    binning = np.linspace(0,500e3,6)

    H_mu_pt = Histogram_Wrapper(tree1,"mu_pt",binning=binning)#,normalise=False)#,AutoBin=True)
    H_mu_E  = Histogram_Wrapper(tree1,"mu_e" ,binning=binning)#,normalise=False)

    # hep.style.use([hep.style.ATLAS])#, {'xtick.direction': 'out'}])
    # print(H_mu_E.__dict__)
    # input()
    # fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)
    y = Ratio_Plot("plot1",list_of_histograms=[H_mu_pt])#
    y.Initalise_Plot_Design("ATLAS")
    y.Add_Histograms([H_mu_E])
    # ,"Seaborn",[H_mu_pt,H_mu_E])
    print(y.__dict__)

    exit()
    x = Ratio_Plot("plot1","CMS",[H_mu_pt,H_mu_E],divisor=H_mu_E)
    plt = x.Make_Normalised_Plot()

    exit()
    plt.show()
    input()

    # print(H_mu_pt.Histogram.values())
    # print(np.sqrt(H_mu_pt.Histogram.variances()))
    # # print(H_mu_pt.Histogram.errors())


    # normalised_hist = H_mu_pt.Histogram/H_mu_pt.Histogram.sum()
    # print(normalised_hist.values())
    # print(ratio_uncertainty(H_mu_pt.Histogram,H_mu_pt.Histogram.sum(),"poisson"))
    # input()

    hep.histplot([H_mu_pt.Histogram, H_mu_E.Histogram], ax=ax, stack=False, histtype='fill', label=["MC1", "MC2"])

    # ratio_hist = H_mu_pt.Histogram/H_mu_E.Histogram

    # hep.histplot(ratio_hist,ax=rax,histtype='fill')

    plt.show()
    input()


    # Histogram = Branch2Hist(tree1,"mu_pt",binning=np.linspace(0,500e3,101))

    # print(Histogram)

main()



