# Make HEP plot using plotly

from matplotlib.pyplot import show
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.randint(0,100,size=(1000, 4)), columns=list('ABCD'))



# import mplhep as hep

# hep.style.use("ATLAS")

fig = px.histogram(df,x='A', nbins=50,width=1000,height=800)

fig.update_xaxes(showline=True, linewidth=2, linecolor='black' , ticks='inside', ticklen=10, tickwidth=3, mirror="ticks")
fig.update_yaxes(showline=True, linewidth=2, linecolor='black' , ticks='inside', ticklen=10, tickwidth=3, mirror="ticks")


fig.update_layout({'paper_bgcolor':'rgba(0,0,0,0)',
    'plot_bgcolor':'rgba(0,0,0,0)'})#,'font_family':'TeX Gyre Heros Regular','font_color':'black','font_size':'32'})

fig.add_trace(go.Scatter(
    x=[20],
    y=[30],
    mode="lines+text",
    text=["<b><i>ATLAS</i></b> Internal"],
    textposition="middle center"
))

# fig.update_yaxes(ticks="inside", col=1,showline=True,mirror=True)
# fig.update_xaxes(ticks="inside", col=1,showline=True,mirror=True)

fig.update_layout(font=dict(
        family="Arial",
        size=28,
        color="black"))
        # xaxis=dict(title = 'T (K)', showgrid=False, showline=True, mirror=True, ticks='inside')))



# For tick marks, look here: https://github.com/plotly/plotly.js/issues/903
    
fig.show()