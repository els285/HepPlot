
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mplhep as hep

from EFTLimitPlotter import EFT_Plot, LHC_EFT_Plot


data = {"ctG":[[(0,-1,1),(-3,-4,-2)],[(2,1,3),(0,-0.5,0.5)]],"ctZ":[[(2,-3,8),None],[(1,-3,6),None]],"ctH":[[(6,2,10),None],[(2,0,4.5),None]]}

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
import seaborn as sns
# import mplhep as hep

plt.style.use(hep.style.ATLAS)
# sns.set_style("dark")

# x = LHC_EFT_Plot(df=df,to_plot=["Linear","Linear+Quadratic"],orientation="hor",experiment="ATLAS",colours=["red","blue"])
x = EFT_Plot(df=df)
fig,ax=x.make_plot(orientation="hor")
ax.set_xlim(-6,12)
# ax.hlines(y=1,xmin=0,xmax=10,color="red")
hep.atlas.text("Internal",loc=1)
plt.show()
input()
