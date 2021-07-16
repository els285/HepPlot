from __future__ import division

from ROOT import TH2D,TCanvas,TFile
import numpy as np

infile = TFile("/home/ethan/Documents/Qualification_Task/ttbar_April22/SmearAll_withEffic/new_smear_comparison.root","READ")

hist2d = infile.Get("inclusive_mu_pt")

hist2d.Draw("COLZ")
raw_input()

import math
 
# Recursive function to return gcd
# of a and b
def gcd_array(array):

	def find_gcd(a,b) :
	    if (a < b) :
	        return find_gcd(b, a)
	     
	    # base case
	    if (abs(b) < 0.001) :
	        return a
	    else :
	        return (find_gcd(b, a - math.floor(a / b) * b))

	num1,num2 = array[0],array[1]
	gcd = find_gcd(num1, num2)
	 
	for i in range(2, len(array)):
	    gcd = find_gcd(gcd, array[i])
	     
	return gcd



def TAxis2Array(Taxis):
    binning = []
    for binn in range(0,Taxis.GetNbins()+1):
        binning.append(Taxis.GetBinUpEdge(binn))
    return binning


def Generate_Bin_Axis(axis):
    min_step = gcd_array(axis)

    steps = (axis[-1]-axis[0])/min_step + 1
    new_binning = np.linspace(axis[0],axis[-1],steps)
    
    return new_binning



def Generate_New_TH2D(hist2d):
    # Get x-axis
    # Get y-axis
    
    x_axis = TAxis2Array(hist2d.GetXaxis())
    y_axis = TAxis2Array(hist2d.GetYaxis())
    
    new_x = Generate_Bin_Axis(x_axis)
    new_y = Generate_Bin_Axis(y_axis)
    
    new_hist2d = TH2D("new","",len(new_x)-1,new_x,len(new_y)-1,new_y)
    
    for x in range(0,len(new_x)-1):
        for y in range(0,len(new_y)-1):
            
            x_bin_value,y_bin_value = new_x[x],new_y[y]
            x_i = hist2d.GetXaxis().FindBin(x_bin_value)
            y_i = hist2d.GetYaxis().FindBin(y_bin_value)
            bin_value = hist2d.GetBinContent(x_i,y_i)
            # print(x,y)
            # print(x_bin_value,y_bin_value)
            # print(x_i,y_i)
            # print(x+1,y+1)
            # print(bin_value)
            new_hist2d.SetBinContent(x+1,y+1,bin_value)

    new_hist2d.Draw("COLZ")
    raw_input()



Generate_New_TH2D(hist2d)

