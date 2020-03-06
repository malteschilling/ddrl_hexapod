"""
Visualize Learning over Time for decentralized approach compared to centralized approach
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

#########################################
# Show Median Values over Multiple Seeds
#########################################

# CORRECTION: For learning curve in original submission, one seed was shown two times 
# which lead to a worse result (graphs look very similar, but performance was already
# reached after 1988 episodes).

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
# Show Mean Values (and shaded std dev) over multiple seeds
#########################################

# Calculate mean and std dev - store in numpy arrays
dec_values = np.zeros( (len(filename_dec), 5000) )
for i in range(0,(len(filename_dec))):
	df = pandas.read_csv(filename_dec[i])
	dec_values[i] = df['main/epreward'][0:5000]
dec_mean = np.mean(dec_values, axis=0)
dec_std = np.std(dec_values, axis=0)
dec_lower_std = dec_mean - dec_std
dec_upper_std = dec_mean + dec_std

# Calculate mean and std dev - store in numpy arrays
centr_values = np.zeros( (len(filename_centr), 5000) )
for i in range(0,(len(filename_centr))):
	df = pandas.read_csv(filename_centr[i])
	centr_values[i] = df['main/epreward'][0:5000]
centr_mean = np.mean(centr_values, axis=0)
centr_std = np.std(centr_values, axis=0)
centr_lower_std = centr_mean - centr_std
centr_upper_std = centr_mean + centr_std

# Plotting functions
fig = plt.figure(figsize=(10, 6))
# Remove the plot frame lines. They are unnecessary chartjunk.  
ax_arch = plt.subplot(111)  
ax_arch.spines["top"].set_visible(False)  
ax_arch.spines["right"].set_visible(False)  
     
#ax_arch.set_yscale('log')
ax_arch.set_xlim(0, 5000)
ax_arch.set_ylim(0, 800)  

# Use matplotlib's fill_between() call to create error bars.   
plt.fill_between(range(0,len(centr_mean)), centr_lower_std,  
                 centr_upper_std, color=tableau20[3], alpha=0.5)  
plt.fill_between(range(0,len(dec_mean)), dec_lower_std,  
                 dec_upper_std, color=tableau20[1], alpha=0.5) 
plt.plot(range(0,len(dec_mean)), dec_mean, color=tableau20[0], lw=1)
plt.plot(range(0,len(centr_mean)), centr_mean, color=tableau20[2], lw=1)

ax_arch.set_xlabel('Training Epochs', fontsize=14)
ax_arch.set_ylabel('Mean Reward per Episode', fontsize=14)

#plt.plot(range(0,len(dec_mean)), dec_values[4,:], color=tableau20[0], lw=2, linestyle='--')
#plt.plot(range(0,len(dec_mean)), centr_values[1,:], color=tableau20[2], lw=2, linestyle='--')

# Plotting line from maximum value reached by centralized approach
dec_already_at_central_max = 0
for i in range(0,5000):
	if (dec_mean[i]>np.max(centr_mean)):
		dec_already_at_central_max = i
		break
print('Reached centralized value at ', dec_already_at_central_max)
plt.plot([dec_already_at_central_max,dec_already_at_central_max,5000], [0.,np.max(centr_mean), np.max(centr_mean)], color=tableau20[6], linestyle='--')
#plt.savefig('epreward_learning_corrected.pdf')

plt.show()