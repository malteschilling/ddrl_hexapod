"""
Visualize Learning over Time for individual seeds for 
decentralized approach compared to centralized approach
(trained on flat terrain, run over 10 seeds each for 5000 epochs).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as py

import pandas

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

# Log file directories
filename_dec = ['Flat_Terrain/decentralized/dppoSeed1Groundplane/DPPOSeed1Groundplane.csv',
	'Flat_Terrain/decentralized/dppoSeed2Groundplane/DPPOSeed2Groundplane.csv',
	'Flat_Terrain/decentralized/dppoSeed3Groundplane/DPPOSeed3Groundplane.csv',
	'Flat_Terrain/decentralized/dppoSeed4Groundplane/DPPOSeed4Groundplane.csv',
	'Flat_Terrain/decentralized/dppoSeed5Groundplane/DPPOSeed5Groundplane.csv',
	'Flat_Terrain/decentralized/dppoSeed6Groundplane/DPPOSeed6Groundplane.csv',
	'Flat_Terrain/decentralized/dppoSeed7Groundplane/DPPOSeed7Groundplane.csv',
	'Flat_Terrain/decentralized/dppoSeed8Groundplane/DPPOSeed8Groundplane.csv',
	'Flat_Terrain/decentralized/dppoSeed9Groundplane/DPPOSeed9Groundplane.csv',
	'Flat_Terrain/decentralized/dppoSeed10Groundplane/DPPOSeed10Groundplane.csv']

filename_centr = ['Flat_Terrain/centralized/ppoSeed1Groundplane/PPOSeed1Groundplane.csv', 
	'Flat_Terrain/centralized/ppoSeed2Groundplane/PPOSeed2Groundplane.csv',
	'Flat_Terrain/centralized/ppoSeed3Groundplane/PPOSeed3Groundplane.csv',
	'Flat_Terrain/centralized/ppoSeed4Groundplane/PPOSeed4Groundplane.csv',
	'Flat_Terrain/centralized/ppoSeed5Groundplane/PPOSeed5Groundplane.csv',
	'Flat_Terrain/centralized/ppoSeed6Groundplane/PPOSeed6Groundplane.csv',
	'Flat_Terrain/centralized/ppoSeed7Groundplane/PPOSeed7Groundplane.csv',
	'Flat_Terrain/centralized/ppoSeed8Groundplane/PPOSeed8Groundplane.csv',
	'Flat_Terrain/centralized/ppoSeed9Groundplane/PPOSeed9Groundplane.csv',
	'Flat_Terrain/centralized/ppoSeed10Groundplane/PPOSeed10Groundplane.csv']
	
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
# Show rewards for individual seeds
#########################################

# Setup matplotlib figure
fig = plt.figure(figsize=(8, 6))
ax_training = plt.subplot(111)  
ax_training.spines["top"].set_visible(False)  
ax_training.spines["right"].set_visible(False)  
ax_training.set_xlim(0, 5000) 

#plt.axvline(x=5000, color=tableau20[6], linestyle='--')

# Plot individual seeds and median (was picked by hand)
for f_name in filename_dec:
	df = pandas.read_csv(f_name)
	df['main/eprewmean'].plot(c='tab:blue', style='--', linewidth=0.75)

# Plot Median value
df = pandas.read_csv(filename_dec[3])
df['main/eprewmean'].plot(c='tab:blue')

for f_name in filename_centr:
	df = pandas.read_csv(f_name)
	df['main/eprewmean'].plot(c='tab:orange', style='--', linewidth=0.75)
	
# Plot Median value
df = pandas.read_csv(filename_centr[6])
df['main/eprewmean'].plot(c='tab:orange')

ax_training.set_xlabel('Training Epochs', fontsize=14)
ax_training.set_ylabel('Mean Reward per Episode', fontsize=14)
plt.savefig('epreward_learning_seeds.pdf')

#########################################
# Show rewards longer training for individual seeds
#########################################
# Setup matplotlib figure
fig = plt.figure(figsize=(12, 6))
ax_training = plt.subplot(111)  
ax_training.spines["top"].set_visible(False)  
ax_training.spines["right"].set_visible(False)  
ax_training.set_xlim(0, 10000) 

#plt.axvline(x=5000, color=tableau20[6], linestyle='--')

# Plot individual seeds and median (was picked by hand)
for i in range(0,3):
	df = pandas.read_csv(filename_dec[i])
	df['main/eprewmean'].plot(c='tab:blue', style='--', linewidth=1)
	df = pandas.read_csv(filename_centr[i])
	df['main/eprewmean'].plot(c='tab:orange', style='--', linewidth=1)

ax_training.set_xlabel('Training Epochs', fontsize=14)
ax_training.set_ylabel('Mean Reward per Episode', fontsize=14)

plt.savefig('epreward_longlearning_seeds.pdf')
plt.show()