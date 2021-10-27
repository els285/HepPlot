
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mplhep as hep

from EFTLimitPlotter import LHC_EFT_Plot


data = {"ctG":[(0,-1,1),(0,-3,3)],"ctZ":[(2,-3,8),(1,-3,6)],"ctH":[(6,2,10),(2,0,4.5)]}

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

df.columns=["Linear","Linear+Quadratic"]

x = LHC_EFT_Plot(df=df,to_plot=["Linear","Linear+Quadratic"],orientation="hor",experiment="ATLAS",colours=["red","blue"])
plt,fig,ax=x.make_vertical_plot()
# ax.hlines(y=1,xmin=0,xmax=10,color="red")
hep.atlas.text("Internal",loc=0)
plt.show()
input()
