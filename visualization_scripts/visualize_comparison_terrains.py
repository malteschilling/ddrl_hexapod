"""
Visualize evaluation on different terrains:
compare the two different control architectures 
- decentralized (blue) and centralized (orange)
- evaluated on different terrain types and heights
- and for training on different terrains.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as py

import pandas
import seaborn as sns

# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)] 
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)
    
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Helvetica'
plt.rcParams['axes.edgecolor']='#333F4B'
plt.rcParams['axes.linewidth']=0.8
plt.rcParams['xtick.color']='#333F4B'
plt.rcParams['ytick.color']='#333F4B'

# Remove Type 3 fonts for latex
plt.rcParams['pdf.fonttype'] = 42
# matplotlib.rcParams['ps.fonttype'] = 42

#########################################
# Show Violin plot for evaluated runs
# on flat terrain and uneven terrain
#########################################
sns.set(style="ticks", color_codes=True)
df = pandas.read_csv('Evaluation_Overview_dataframe.csv')

my_pal = {"ppo": tableau20[2], "dppo": tableau20[0]} 

df_select = df.loc[df['Evaluate'].isin(['Flat','Height_010'])]

sns.set(context="paper", palette="colorblind", style="ticks", font_scale=1.2)
fig_violin = sns.FacetGrid(df_select, col="Evaluate", sharey=True, size=4, aspect=.8)
fig_violin = fig_violin.map(sns.violinplot, "Train", "Reward", "Arch_Train", inner='quartile', split=True, palette=my_pal, saturation=0.75).despine(left=True)

fig_violin.fig.set_figwidth(8)
fig_violin.fig.set_figheight(6)

fig_violin.fig.get_axes()[0].set_xlabel("Evaluation on Flat Ter.")
fig_violin.fig.get_axes()[1].set_xlabel("Evaluation on Height Map")
fig_violin.fig.get_axes()[0].set_xticklabels(["Training on Flat Ter.", "Training on Height Map"])
fig_violin.fig.get_axes()[1].set_xticklabels(["Training on Flat Ter.", "Training on Height Map"])
fig_violin.fig.get_axes()[0].set_ylabel("Mean reward per episode")

#fig_violin.fig.get_axes()[0].set_yticks(range(0, 900, 100))
#fig_violin.fig.get_axes()[1].set_yticks([])
#fig_violin.fig.get_axes()[0].set_yticks(range(0, 900, 100))
fig_violin.fig.get_axes()[0].spines["left"].set_visible(True)

# Set legend #
handles, labels = fig_violin.fig.get_axes()[0].get_legend_handles_labels()
# Fixing titles #
fig_violin.fig.get_axes()[0].set_title("")
fig_violin.fig.get_axes()[1].set_title("")

#plt.savefig('violin.pdf')

#########################################
# Show Violin plot for evaluated runs
# on all four terrains
#########################################
sns.set(context="paper", palette="colorblind", style="ticks", font_scale=1.2)
fig_violin_all = sns.FacetGrid(df, col="Evaluate", sharey=True, size=4, aspect=.8)
fig_violin_all = fig_violin_all.map(sns.violinplot, "Train", "Reward", "Arch_Train", inner='quartile', split=True, palette=my_pal, saturation=0.75).despine(left=True)

fig_violin_all.fig.set_figwidth(15)
fig_violin_all.fig.set_figheight(6)

#fig_violin_all.fig.get_axes()[0].set_xlabel("Evaluation on Flat Ter.")
#fig_violin_all.fig.get_axes()[1].set_xlabel("Evaluation on Height Map 0.")
fig_violin_all.fig.get_axes()[0].set_xticklabels(["Training on Flat Ter.", "Training on Height Map"])
fig_violin_all.fig.get_axes()[1].set_xticklabels(["Training on Flat Ter.", "Training on Height Map"])
fig_violin_all.fig.get_axes()[2].set_xticklabels(["Training on Flat Ter.", "Training on Height Map"])
fig_violin_all.fig.get_axes()[3].set_xticklabels(["Training on Flat Ter.", "Training on Height Map"])
fig_violin_all.fig.get_axes()[0].set_ylabel("Mean reward per episode")

#fig_violin.fig.get_axes()[0].set_yticks(range(0, 900, 100))
#fig_violin.fig.get_axes()[1].set_yticks([])
#fig_violin.fig.get_axes()[0].set_yticks(range(0, 900, 100))
fig_violin_all.fig.get_axes()[0].spines["left"].set_visible(True)

# Set legend #
handles, labels = fig_violin_all.fig.get_axes()[0].get_legend_handles_labels()
# Fixing titles #
#fig_violin_all.fig.get_axes()[0].set_title("")
#fig_violin_all.fig.get_axes()[1].set_title("")

plt.show()