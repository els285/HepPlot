import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

# xbins = [0,1,2,3]
# ybins = [0,1,2,3]
#
# H = [[1,2,1],[1,3,2]]
#
# fig, ax = plt.subplots()
# #
# # X,Y = np.meshgrid(xbins,ybins)
# #
# # pc = ax.pcolormesh(X,Y,H)
# #
# # plt.show()
# # input()
# # plt.close()
# #
# # fig2, ax2 = plt.subplots()
#
# hep.hist2dplot(H,xbins,ybins)
#
# plt.show()
# input()
# plt.close()
import numpy as np

import seaborn as sns

# hep.set_style(hep.style.ATLAS)
hep.style.use(hep.style.CMS)
fig,ax = plt.subplots()
xbins, ybins = [0, 1, 2, 3], [0, 1, 3]
H = np.array([[2,1], [1,2], [3,5]])
hep.hist2dplot(H, xbins, ybins)

# plt.show()
import streamlit as st

st.write("""
# HEP Dashboard
Welcome to the HEP Dashboard, designed to display your HEP plots in an interactive way!
""")

st.pyplot(fig)
# st.write(plt.run(window=15))
