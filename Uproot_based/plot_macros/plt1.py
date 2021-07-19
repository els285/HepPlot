def Generate_Histogram(num_bins,hist_range,df,normalise):
    bins = np.linspace(hist_range[0],hist_range[1],num_bins+1)
    h = bh.Histogram(bh.axis.Variable(bins))
    h.fill(df)
    if normalise:
        return h/h.sum()
    else:
        return h


def Get_Extrema(df):
    import math
    return float(math.ceil(df.max())),float(math.floor(df.min()))

#Streamlit suffers from the problem of being slow to generate a slider for histogram extrema which are very large values 
#This is problematic for pT and eta


def EPT_Histogram(nb,minH,maxH,df,index):
    nearest10k = lambda a: math.ceil(a/10e3)*10e3
    maxH = nearest10k(maxH)
    hist_range = st.slider('Range of histogram',value=[0.0,maxH/1e3],key=index)
    hist_range = tuple([1e3*x for x in hist_range])
    return Generate_Histogram(nb,hist_range,df)

def Angular_Histogram(nb,minH,maxH,df,index):
    hist_range = st.slider('Range of histogram',value=[minH,maxH],key=index)
    return Generate_Histogram(nb,hist_range,df)



def Branch2Hist(tree,branch_name,index):
    df = tree[branch_name].array(library="pd")

    nb = st.slider('Number of bins',min_value=1,max_value=100,value=50,key=index)
    maxH,minH = Get_Extrema(df)

    #####

    # Switch statement to select correct histogram based on branch name
    if "_eta" in branch_name or "_phi" in branch_name:
        h = Angular_Histogram(nb,minH,maxH,df,index)
    else:
        h = EPT_Histogram(nb,minH,maxH,df,index)

    return h ,df



# class PolyHist:

#     d


def Plot_SingleHist(h,branch_name):

    fig,ax = plt.subplots()
    hep.histplot(h)
    plt.xlabel(branch_name)
    plt.ylabel("Number of events")
    st.pyplot(fig)

