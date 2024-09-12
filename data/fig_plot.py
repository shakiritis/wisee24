import os
import re
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from glob import glob
from scipy.signal import savgol_filter
import sys
from textwrap import wrap
import time

absorber = int(sys.argv[1])
# metric = sys.argv[2]
alg = sys.argv[2]
save = int(sys.argv[3])
N = 1000

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 15
# plt.rcParams["text.usetex"] =True
# params = {'mathtext.default': 'regular' }          
# plt.rcParams.update(params)
Pmax = [0.79, 0.86, 0.93]
epsilon = [0.05, 0.1, 0.15]
fig, ax = plt.subplots()
aspect = []

labels_ap = [r'$P_{max}$: 0.93, without absorber', r'$P_{max}$: 0.86, without absorber', r'$P_{max}$: 0.79, without absorber',
             r'$P_{max}$: 0.93, with absorber', r'$P_{max}$: 0.86, with absorber', r'$P_{max}$: 0.79, with absorber']

labels_eg = [r'  : 0.15, without absorber', r'  : 0.10, without absorber', r'  : 0.05, without absorber',
             r'  : 0.15, with absorber', r'  : 0.10, with absorber', r'  : 0.05, with absorber']

colors = ['g', 'black', 'navy']
colors_abs = ['tomato', 'orange', 'violet']


if alg == 'ap':
    for i, p in enumerate(Pmax):
        snr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\snr_abs_{}_{}.npy'.format('ap', p))
        pr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\pr_abs_{}_{}.npy'.format('ap', p))
        snr = np.load('D:\\projects\\wamicon24\\data\\2\\snr_{}_{}.npy'.format('ap', p))
        pr = np.load('D:\\projects\\wamicon24\\data\\2\\pr_{}_{}.npy'.format('ap', p))

        aspect.append(np.max(snr))
        plt.plot(snr, pr, label = labels_eg[i], color = colors[i], linewidth=2, linestyle='dashed')
        plt.plot(snr_abs, pr_abs, label = labels_eg[i+3], color = colors_abs[i], linewidth=2)

if alg == 'eg':
    for i, p in enumerate(epsilon):
        snr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\snr_abs_{}_{}.npy'.format('eg', p))
        pr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\pr_abs_{}_{}.npy'.format('eg', p))
        snr = np.load('D:\\projects\\wamicon24\\data\\2\\snr_{}_{}.npy'.format('eg', p))
        pr = np.load('D:\\projects\\wamicon24\\data\\2\\pr_{}_{}.npy'.format('eg', p))

        aspect.append(np.max(snr))
        plt.plot(snr, pr, label = labels_ap[i], color = colors[i], linewidth=2, linestyle='dashed')
        plt.plot(snr_abs, pr_abs, label = labels_ap[i+3], color = colors_abs[i], linewidth=2)

if alg == 'aio':
    ap_snr = np.load('D:\\projects\\wamicon24\\data\\2\\snr_ap_0.93.npy')
    ap_snr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\snr_abs_ap_0.93.npy')
    ap_pr = np.load('D:\\projects\\wamicon24\\data\\2\\pr_ap_0.93.npy')
    ap_pr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\pr_abs_ap_0.93.npy')

    eg_snr = np.load('D:\\projects\\wamicon24\\data\\2\\snr_eg_0.05.npy')
    eg_snr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\snr_abs_eg_0.05.npy')
    eg_pr = np.load('D:\\projects\\wamicon24\\data\\2\\pr_eg_0.05.npy')
    eg_pr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\pr_abs_eg_0.05.npy')

    r_snr = np.load('D:\\projects\\wamicon24\\data\\2\\snr_r_xx.npy')
    r_snr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\snr_abs_r_xx.npy')
    r_pr = np.load('D:\\projects\\wamicon24\\data\\2\\pr_r_xx.npy')
    r_pr_abs = np.load('D:\\projects\\wamicon24\\data\\2\\pr_abs_r_xx.npy')

    aspect = [np.max(ap_snr), np.max(ap_snr_abs), np.max(eg_snr), np.max(eg_snr_abs)]
    plt.plot(ap_snr, ap_pr, 'g', linewidth=2, label = '  -greedy: without absorber')
    plt.plot(ap_snr_abs, ap_pr_abs, c = 'black', linewidth=2, linestyle = (0,(5,1)), label = '  -greedy: with absorber')
    plt.plot(eg_snr, eg_pr, c = 'navy', linestyle = (0, (1,1)), linewidth=2, label = 'AP: without absorber')
    plt.plot(eg_snr_abs, eg_pr_abs, c = 'tomato',linestyle = (5, (10,3)),  linewidth = 2, label = 'AP: with absorber')
    plt.plot(r_snr, r_pr, c = 'orange', linestyle = 'dashed', linewidth=2, label = 'Random: without absorber')
    plt.plot(r_snr_abs, r_pr_abs, c = 'violet',linestyle = 'dashdot',  linewidth = 2, label = 'Random: with absorber')



# ax.set_aspect(max(aspect), adjustable='box')
plt.grid(True, color='grey', linestyle='--', linewidth=0.2)
plt.xlabel('SNR (dB)')
plt.ylabel('CDF of SNR')
# matplotlib.style.use('classic')
plt.legend(loc='upper left', framealpha=0.3, frameon=True,prop={'family':'Arial', 'size':12})
plt.xticks([(i)*5 for i in range(8)])
yticks = [0.0,0.2,0.4,0.6,0.8,1.0]  # Get the current y-ticks
plt.yticks(yticks[1:])  # Set the y-ticks to exclude the lowest one
plt.axhline(0, color='black', linewidth=0.8)  # X-axis at y=0
plt.axvline(0, color='black', linewidth=0.8)
plt.xlim(0,38)
plt.ylim(0,1.0)

if save == 1:
    plt.savefig('../figs/2/{}.png'.format(alg), dpi = 300)
plt.show()

# if alg == 'eg':
#     for p in Pmax:
#         snr_fp = 'D:\\projects\\wamicon24\\data\\snr_{}_{}.npy'.format(alg, metric)
#         pr_fp = 'D:\\projects\\wamicon24\\data\\pr_{}_{}.npy'.format(alg, metric)

# if absorber == 1:
#     snr_fp = 'D:\\projects\\wamicon24\\data\\snr_{}_{}.npy'.format(alg, metric)
#     pr_fp = 'D:\\projects\\wamicon24\\data\\pr_{}_{}.npy'.format(alg, metric)
# else:
#     snr_fp = 'D:\\projects\\wamicon24\\data\\snr_abs_{}_{}.npy'.format(alg, metric)
#     pr_fp = 'D:\\projects\\wamicon24\\data\\pr_abs_{}_{}.npy'.format(alg, metric)

# snr = np.load(snr_fp)
# pr = np.load(pr_fp)

# fig, ax = plt.subplots()
# plt.plot(snr, pr, color = 'g')
# # plt.plot(snr_abs, pr_abs, color = 'r')
# plt.xlabel('SNR (dB)')
# plt.ylabel('CDF of SNR')
# plt.grid(True, color='grey', linestyle='--', linewidth=0.3)
# ax.set_aspect(np.max(snr), adjustable='box')
# plt.show()




