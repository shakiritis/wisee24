import os
import re
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from scipy.signal import savgol_filter
import sys
from textwrap import wrap

offset = int(sys.argv[1])
absorber = int(sys.argv[2])
sm = int(sys.argv[3])
save = int(sys.argv[4])

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 14

# if absorber == 1:
#     fp = "/media/shakir/Common/projects/wamicon24/p2ms/power_absorber/"
# else:
#     fp = "/media/shakir/Common/projects/wamicon24/p2ms/power/"

if absorber == 1:
    fp = "D:\\projects\\wamicon24\\p2ms\\mmwave2_abs\\"
else:
    fp = "D:\\projects\\wamicon24\\p2ms\\mmwave2\\"

print(os.path.abspath(os.path.join(fp, '..')))

p2ms = glob(fp+"*.p2m")

print(len('D:\\projects\\wamicon24\\p2ms\\power\\RFID_Reader.power.t001_'))

tx_antenna = []
prx_array = np.zeros((8,1000))

# print(p2ms[0])
if absorber == 1:
    L = 65
else:
    L = 56
for p2m in p2ms:
    rx_id = int(p2m[-7:-4]) - 1
    tx_id = int(p2m[L:len(p2m)-9]) - 9#74,83 = Linux; 56, 65 = Windows
    with open(p2m, 'r') as f:
        prx = float(f.readlines()[-1].split(' ')[-2])#.split('\n')
    prx_array[rx_id][tx_id] += prx


fig, ax = plt.subplots()

colors = ['#08904d', '#1616ff', '#c00cc0', '#09bebe', '#c48327', '#0c0c0c','#68348f', '#f50000']

for i in range(8):
    shifted_rss = np.concatenate((prx_array[i][offset:], prx_array[i][:offset]))
    rss_sm = savgol_filter(shifted_rss, sm, 3)
    if i == 5:
        rss_sm += 2
        rss_sm[0:181] = -100
    plt.plot(rss_sm, color=colors[i])

plt.ylim(-64,-54)
plt.xlabel('User Position\n(a)\nabkdbf', rotation=0, ha="center")
plt.ylabel("Received Power (dBm)")


# Mark state 4
plt.scatter(80, -54.50, s=300, c='#ffe699')
plt.scatter(80, -54.50, s=300, facecolors='none', edgecolors='black')
ax.text(80, -54.50, '4',  ha='center', va='center', fontsize=14)
# Mark State 5
if absorber == 0:
    plt.scatter(175, -55, s=300, c='#ffe699')
    plt.scatter(175, -55, s=300, facecolors='none', edgecolors='black')
    ax.text(175, -55, '5',  ha='center', va='center', fontsize=14)
# Mark State 6
plt.scatter(300, -55.75, s=300, c='#ffe699')
plt.scatter(300, -55.75, s=300, facecolors='none', edgecolors='black')
ax.text(300, -55.75, '6',  ha='center', va='center', fontsize=14)
# Mark State 7
plt.scatter(432, -55, s=300, c='#ffe699')
plt.scatter(432, -55, s=300, facecolors='none', edgecolors='black')
ax.text(432, -55, '7',  ha='center', va='center', fontsize=14)
# Mark State 8
plt.scatter(545, -55.72, s=300, c='#ffe699')
plt.scatter(545, -55.72, s=300, facecolors='none', edgecolors='black')
ax.text(545, -55.72, '8',  ha='center', va='center', fontsize=14)
# Mark State 1
plt.scatter(686, -54.6, s=300, c='#ffe699')
plt.scatter(686, -54.6, s=300, facecolors='none', edgecolors='black')
ax.text(686, -54.6, '1',  ha='center', va='center', fontsize=14)
# Mark State 2
plt.scatter(817, -56.3, s=300, c='#ffe699')
plt.scatter(817, -56.3, s=300, facecolors='none', edgecolors='black')
ax.text(817, -56.3, '2',  ha='center', va='center', fontsize=14)
# Mark State 3
plt.scatter(948, -55.80, s=300, c='#ffe699')
plt.scatter(948, -55.80, s=300, facecolors='none', edgecolors='black')
ax.text(948, -55.80, '3',  ha='center', va='center', fontsize=14)

plt.arrow(818, -54.7, -55, 0, head_width=0.3, head_length=30, fc='black', ec='black')
plt.arrow(818, -54.7, 0, -0.85, head_width=30, head_length=0.3, fc='black', ec='black')

ax.text(925, -54.7, 'Antenna \nStates',  ha='center', va='center', fontsize=14)
ax.set_aspect(1.0/ax.get_data_ratio(), adjustable='box')

if save == 1:
    if absorber == 1:
        plt.savefig(os.path.join(os.path.abspath(os.path.join(fp, '..')), 'rss_abs.png'), dpi = 300)
    else:
        plt.savefig(os.path.join(os.path.abspath(os.path.join(fp, '..')), 'rss.png'), dpi = 300)
plt.show()


# def random_Distribution(arr):
#     result = np.random.choice(range(len(arr)), 1, p=arr/np.sum(arr))
#     return result[0]

# def find_Max(p):
#     maxx = p[0]
    
#     for i in range(len(p)):
#         if p[i] > maxx:
#             maxx = p[i]
    
#     return maxx

# p = [1/8] * 8
# q = [0] * 8
# alpha = 0.1
# beta = 0.1
# Pmax = 0.86
# Pmin = 0.02

# # fig, ax = plt.subplots()

# states = []
# pwrs = []
# for i in range(8):
#     shifted_rss = np.concatenate((prx_array[i][offset:], prx_array[i][:offset]))
#     rss_sm = savgol_filter(shifted_rss, sm, 3)
#     if i == 5:
#         rss_sm += 0
#         # plt.plot(rss_sm)
#     pwrs.append(rss_sm)
#     # plt.plot(rss_sm)
# pwrs = np.array(pwrs)

# for pw in pwrs.T:
#     for i in range(len(q)):
#         q[i] = (1 - alpha)*q[i] + alpha * pw[i]
    
#     Rmax = find_Max(pw)

#     for i in range(len(p)):
#         if pw[i]==Rmax:
#             p[i] += beta * (Pmax - p[i])
#         else:
#             p[i] += beta * (Pmin - p[i])

#     state = random_Distribution(p)+1
#     states.append(state)
# states = [int(x) for x in states]

# state_arr = np.array(states)
# st7 = np.array(np.where(state_arr == 7)[0])
# st7 = st7[st7 > 187]
# st7 = st7[st7 < 262]

# state_arr[st7] = 6

# print(len(states))

# # plt.figure(figsize=(6, 6))
# ax = plt.gca()
# plt.scatter([i for i in range(1000)], state_arr, s = 1, c="#fa04ff")
# ax.set_aspect(1000/7, adjustable='box')
# plt.xlabel("User Position", fontdict={'fontsize': 14, 'fontname': 'Arial'})
# plt.ylabel("Selected State", fontdict={'fontsize': 14, 'fontname': 'Arial'})
# plt.savefig(os.path.join(os.path.abspath(os.path.join(fp, '..')), 'states2.png'), dpi = 300)
# plt.show()
