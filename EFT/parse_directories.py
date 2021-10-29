# For parsing a series of text files 

"""
Basic plotting format
cHQ1	[-5.2],[7.0]
cHQ3	[-8.4],[4.0]
cHt	[-4.6],[8.4]
"""

import re 

def compute_mid_point(lower,upper): 
    return 0.5*(upper - lower)


def extract_bounds_from_txt(filename):

    data = {}
    file1 = open(filename, 'r')
    Lines = file1.readlines()

    for x in Lines:
        indiv_line = x.replace("\t",",")
        t = indiv_line.split(",")
        lower_bound =float(t[1].replace("[","").replace("]",""))
        upper_bound =float(t[2].replace("[","").replace("]","").replace("\n",""))
        data[t[0]] =[(lower_bound,upper_bound)]

    return data


def extract_global_mode(filename):
    """
    The lines in the txt file are NamedTuples, which are a Python object. Surely we can push to some other filetype from that?
    """
    
    data = {}
    file1 = open(filename, 'r')
    Lines = file1.readlines()

    for x in Lines:
        l1 =x.split("[")[1].replace("\n","").split(")")
        for m in l1:
            l2 = m.strip("").replace("(","").split(",")
            for x in l2:
                if "parameter" in x:
                    wilson_coef = x.replace(" ","").split("=")[1].replace(":","")
                if "global_mode" in x:
                    global_mode = x.replace(" ","").split("=")[1]
            assert "wilson_coef" in locals(), "parameter term not found"
            assert "global_mode" in locals(),"global mode value not found"
            data[wilson_coef] = float(global_mode)
    
    return data

def Parse(bounds_filename,statistics_filename):

    bounds_data       =  extract_bounds_from_txt(bounds_filename)
    global_mode_data  =  extract_global_mode(statistics_filename)

    data = {}
    for wc in bounds_data:
        assert wc in global_mode_data.keys(),"Cannot find "+wc+" in global_mode_data"
        data[wc] = {"Bounds":bounds_data[wc],"Global Mode":global_mode_data[wc]}
    # data = {**bounds_data, **global_mode_data}

    import pandas as pd

    df = pd.DataFrame.from_dict(data).T
    return df 

print(Parse(bounds_filename="/home/ethan/EFTfitterSpinCorr.jl/results_ptz_laurynas/Numerics/1dlimits.txt",
            statistics_filename="/home/ethan/EFTfitterSpinCorr.jl/results_ptz_laurynas/Numerics/statistics.txt"))
