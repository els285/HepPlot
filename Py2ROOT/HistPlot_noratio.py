
import matplotlib.pyplot as plt
import numpy as np
from ROOT import TFile,TAxis,TH1,gROOT
import os
import sys




def axis_limits_ratio(Hists,margin_factor):
    MAX = max([max(hist.new_norm_data) for hist in Hists])
    MIN = min([min(hist.new_norm_data) for hist in Hists])
    extrema = max(abs(MAX),abs(MIN))   # Just to choose which is larger for symmetry purposes
    if extrema > 1.0:
        scale = round(extrema*margin_factor,1)
    if extrema < 1.0:
        scale = round(extrema/margin_factor,1)
    difference = abs(scale-1)
    max_axis_value = 1 + difference
    min_axis_value = 1 - difference
    return min_axis_value,max_axis_value



def hist1dplot_NOratio(Hists,**kwargs):


    #### Firstly, generate ratio histograms
    # dividing_hist = kwargs["normaliser"]
    # # ratio_dict = ratio_generator(dividing_hist,Hists)
    # # normalised_histograms()
    # for hist in Hists:
    #     hist.generate_normalised(dividing_hist)

    import seaborn as sns
    # sns.set_style("dark")
    # sns.set(rc={'text.usetex':True, 'font.family':'serif', 'font.serif':'sahadeva'})
    # plt.rcParams.update({
    #     "text.usetex": True,
    #     'font.family':'sans-serif', 'font.sans-serif':'sahadeva'})

    plt.rc('font', family='FreeSans')

    fig,ax1 = plt.subplots()
    # fig, (ax1, ax2) = plt.subplots(2,gridspec_kw={'height_ratios': [3, 1]})   

    font = {'family': 'serif',
            'color':  'dimgrey',
            'weight': 'normal',
            'size': 36,
            }

    ######### Main plot parameters
    from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                                   AutoMinorLocator)


    ######################### Ticks #################################


    Nmajor_xticks = 10
    Nminor_xticks = 4

    major_xticks = np.linspace(Hists[0].x_bins[0],Hists[0].x_bins[-1],Nmajor_xticks+1)
    minor_xticks = np.linspace(Hists[0].x_bins[0],Hists[0].x_bins[-1],(Nminor_xticks+1)*Nmajor_xticks+1)

    ax1.set_xticks(minor_xticks, minor = True)
    ax1.set_xticks(major_xticks)
    # ax2.set_xticks(minor_xticks, minor = True)
    # ax2.set_xticks(major_xticks)

    ax1.set_xlim([Hists[0].x_bins[0],Hists[0].x_bins[-1]])
    # ax2.set_xlim([Hists[0].x_bins[0],Hists[0].x_bins[-1]])
# 
    ax1_top = max([max(hist.ydata) for hist in Hists])*1.35
    ax1.set_ylim([0,ax1_top])

    major_yticks1 = np.arange(0,ax1_top,0.05)
    minor_yticks1 = np.arange(0,ax1_top,0.01)

    ax1.set_yticks(minor_yticks1, minor = True)
    ax1.set_yticks(major_yticks1)

    yticks1 = ax1.yaxis.get_major_ticks() 
    yticks1[0].label1.set_visible(False)

    ax1.tick_params(bottom=True, top=True, left=True, right=True,length=10,direction="in",labelsize=18,labelbottom=False,width=1.5)
    ax1.tick_params(bottom=True, top=True, left=True, right=True,which='minor', length=4, direction="in",width=1.5)



    # alr=list(axis_limits_ratio(Hists,1.2))
    # ax2.set_ylim(alr)
 
    # Nmajor_yticks2 = 3
    # Nminor_yticks2 = 9

    # major_yticks2 = np.linspace(alr[0],alr[1],Nmajor_yticks2)
    # minor_yticks2 = np.linspace(alr[0],alr[1],Nminor_yticks2)

    # ax2.set_yticks(minor_yticks2, minor = True)
    # ax2.set_yticks(major_yticks2)

    # ax2.set_xlabel(r"$p_t $",fontsize=32,labelpad=24)
    # ax2.set_ylabel("Ratio",fontsize=32,labelpad=36)
    # ax2.tick_params(bottom=True, top=True, left=True, right=True,length=10,direction="in",labelsize=18,labelbottom=True,width=1.5)
    # ax2.tick_params(bottom=True, top=True, left=True, right=True,which='minor', length=4, direction="in",width=1.5)

    # ax2.set_xticklabels([0,0,200,400,600,800,1000,1200,1400])

    plt.setp(ax1.spines.values(), linewidth=1.5)
    # plt.setp(ax2.spines.values(), linewidth=1.5)

    ############################ ATLAS text #############################

    ax1.text(0.05,0.86,"$ATLAS$ Internal",fontsize=32,transform=ax1.transAxes,fontname="Helvetica Light",fontweight="bold")

    #############

    # Plotting

    linewidth = 2

    #### Added in a part here where the colour argument is called differently depending on whether it exists

    # Loop plotter

    ############################# Plotter ################################################

    ###### Step Histograms (all bar the last histogram)

    for hist in Hists:

        colour = np.random.rand(3,) if hist.colour == None else hist.colour


        ax1.plot(hist.x_bins, hist.ydata,drawstyle="steps-post",color=colour,label=hist.name,linewidth=linewidth)
        ax1.vlines(hist.x_bins[0],0,hist.ydata,color=colour,linewidth=linewidth)

        # ax2.plot(hist.x_bins, hist.new_norm_data,drawstyle="steps-post",color=colour,linewidth=linewidth)
        # ax2.vlines(hist.x_bins[0],1.0,hist.new_norm_data,color=colour,linewidth=linewidth)


    ################## Filled Histogram (last one in the list)    

    fill_colour = np.random.rand(3,) if Hists[-1].colour == None else Hists[-1].colour

    # ax1.fill_between(Hists[-1].x_bins,Hists[-1].ydata,step="post", alpha=0.2,color=fill_colour,label=Hists[-1].name)
    # ax2.fill_between(Hists[-1].x_bins,Hists[-1].new_norm_data,y2=1.0,step="post", alpha=0.2,color=fill_colour,label=Hists[-1].name)


    #################### Errorbars ##################################
    for hist in Hists:

        colour = np.random.rand(3,) if hist.colour == None else hist.colour
        ax1.errorbar(hist.xc_bins, hist.ydata[:-1], yerr=hist.errors, color=colour,alpha=0.4,ls="none")
        # ax2.errorbar(hist.xc_bins, hist.norm_data[:-1], yerr=hist.norm_errors, color=colour,alpha=0.4,ls="none")


    ####################### Legend #########################


    handles, labels = ax1.get_legend_handles_labels()

    labels2 = []
    for h in Hists:
        if hasattr(h,"legend_entry"):
            labels2.append(h.legend_entry)
        else:
            labels2.append(h.name)

    ax1.legend(handles, labels2,fontsize=20,frameon=False,loc="upper right")

    ########################### Axis Labels ######################

    if "axis_labels" in kwargs:
        labels=kwargs["axis_labels"]
        ax1.set_xlabel(labels["x_label"]  ,fontsize=32)#,labelpad=10)
        ax1.set_ylabel(labels["y_label"]  ,fontsize=28)#,labelpad=24)
        # ax2.set_ylabel(labels["y_lower"]  ,fontsize=20)#,labelpad=36)


    ax1.yaxis.set_label_coords(-0.07,0.7)
    # ax2.yaxis.set_label_coords(-0.07,0.5)


    ######################### Title ###########################

    if "title" in kwargs:
            fig.suptitle(kwargs["title"],fontsize=28)
            fig.subplots_adjust(top=0.92)


    fig.set_size_inches(12.5, 10.5, forward=True)

    plt.subplots_adjust(wspace=0.5, hspace=0.025)


    if "save_path" in kwargs and "title" in kwargs:
        if os.path.isdir(kwargs["save_path"]):
            plt.savefig(kwargs["save_path"]+"/" + kwargs["title"] +".png",dpi=300)
        else: print("Directory does not exist, so cannot save image")
    elif "title" in kwargs:
        plt.savefig("./" + kwargs["title"]+".png",dpi=300)

    return plt


