import matplotlib.pyplot as plt
import mplhep as hep
import hist
import numpy as np

# Equivalent syntax for styling options
hep.style.use([hep.style.ATLAS])#, {'xtick.direction': 'out'}])
# plt.style.use(hep.style.ATLAS)

a = hist.Hist.new.Reg(20,-2,2).Int64().fill(np.random.uniform(-2,2,size=3000))
b = hist.Hist.new.Reg(20,-2,2).Int64().fill(np.random.normal(0,0.5,size=5000))
c = hist.Hist.new.Reg(20,-2,2).Int64().fill(np.random.normal(1,5,size=5000))

tot = a + b
data = tot.copy()
data[...] = np.random.poisson(tot.values())


# # a.plot()
# # plt.show()
# # input()

# a.plot_ratio(b)
# c.plot_ratio(b)
# plt.show()
# input()

from hist.intervals import ratio_uncertainty

# Generates mpl plot axes
fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)

# Plots MC hists
hep.histplot([a, b], ax=ax, stack=True, histtype='fill', label=["MC1", "MC2"])
# Plots data hist (as datapoints with errorbars)
hep.histplot(data, ax=ax, histtype='errorbar', color='k', capsize=4, yerr=True, label="Data")

# mpl 
errps = {'hatch':'////', 'facecolor':'none', 'lw': 0, 'color': 'k', 'alpha': 0.4}
ax.stairs(
    values=tot.values() + np.sqrt(tot.values()),
    baseline=tot.values() - np.sqrt(tot.values()),
    edges=tot.axes[0].edges, **errps, label='Stat. unc.')





# This gives the up and down variation on the plot
yerr = ratio_uncertainty(data.values(), tot.values(), 'poisson')

# print(a.values(),a.values(),'poisson')
# input()
# print(yerr)
# # print(np.sqrt(data.values())/tot.values())
# input()
# # yerr = ratio_uncertainty(a.values(),2,'poisson')
# print(yerr)
# input()

# print(yerr)
# input()
# rax.stairs(1+yerr[1], edges=tot.axes[0].edges, baseline=1-yerr[0], **errps)
hep.histplot(data.values()/tot.values(), tot.axes[0].edges, yerr=np.sqrt(data.values())/tot.values(),
    ax=rax, histtype='fill',  label="Data")
l1 = hep.atlas.text(text='Internal',loc=1,ax=ax)


rax.axhline(1, ls='--', color='k')
rax.set_ylim(0.7, 1.3)
ax.set_xlim(-2, 2)
ax.legend()


plt.show()
input()