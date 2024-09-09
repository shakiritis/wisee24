import os
import re
import random
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from scipy.signal import savgol_filter
import sys
from textwrap import wrap
import time

absorber = int(sys.argv[1])
metric = sys.argv[2]
alg = sys.argv[3]
N = 1000
# offset = int(sys.argv[1])
# absorber = int(sys.argv[2])
# sm = int(sys.argv[3])
# save = int(sys.argv[4])

# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 14

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 15

k = 8
epsilon = 0.05
alpha = 0.25
beta = 0.1
Pmax = 0.79
Pmin = 0.03
p = [1/k]*k
q = [0] * k
n = [0] * k

def random_Distribution(arr):
    result = np.random.choice(range(len(arr)), 1, p=arr/np.sum(arr))
    return result[0]

def find_Max(p):
    maxx = p[0]
    
    for i in range(len(p)):
        if p[i] > maxx:
            maxx = p[i]
    
    return maxx

def adaptivePursuit(pw, idx):

    Rmax = find_Max(pw)

    for i in range(len(p)):
        if pw[i]==Rmax:
            # print("milse")
            p[i] += beta * (Pmax - p[i])
        else:
            p[i] += beta * (Pmin - p[i])

    state = random_Distribution(p)+1

    return state + 1

def epsilonGreedy(pw, q):
    if random.random() < epsilon:
        return np.random.randint(len(pw))
    else:
        return np.argmax(pw)


def plotPWR(absorber):
    if absorber == 1:
        fp = "D:\\projects\\wamicon24\\p2ms\\mmWave_abs2\\power\\"
        L = len("D:\\projects\\wamicon24\\p2ms\\mmWave_abs2\\power\\RFID_Reader.power.t001_xx.r")
    else:
        fp = "D:\\projects\\wamicon24\\p2ms\\mmWave2\\power\\"
        L = len("D:\\projects\\wamicon24\\p2ms\\mmWave2\\power\\RFID_Reader.power.t001_xx.r")
    
    p2ms = glob(fp+"*.p2m")

    prx_array = np.zeros((N,8))

    for p2m in p2ms:
        n = len(p2m) - L
        rx_id = int(p2m[-n:-4]) - 9
        tx_id = int(p2m[:L][-4:-2]) - 1 # - 1#74,83 = Linux; 56, 65 = Windows
        # if "RFID_Reader.power.t001_08.r1002.p2m" in p2m:
        #     print("tx, rx: ", tx_id, rx_id)
        
        # print("rx, tx, p2m: ", rx_id, tx_id, p2m)

        with open(p2m, 'r') as f:
            prx = float(f.readlines()[-1].split(' ')[-2])#.split('\n')
        # if p2m == "D:\\projects\\wamicon24\\p2ms\\100_txrx\\comSys\\ber\\RFID_Reader.ber.t001_09.r001.p2m":
        #     print(prx)
        prx_array[rx_id][tx_id] += prx
    
    # for idx, ber in enumerate(prx_array):
    #     plt.plot(10**ber)
    
    # plt.show()
    return prx_array  

levels = np.linspace(-85,-54,30)

if metric == 'pwr':
    pwrs = plotPWR(absorber)
    for pw in pwrs.T:
        prb = []
        pw_sm = savgol_filter(pw, 71, 3)
        for lvl in levels:
            prb.append(np.count_nonzero(pw <= lvl)/N)
        print(len(prb), len(levels))
        plt.plot(levels, prb)
    # plt.ylim(-64,-54)
    plt.show()

def plotBER(absorber):
    if absorber == 1:
        fp = "D:\\projects\\wamicon24\\p2ms\\mmWave_abs\\comSys\\ber\\"
        L = len("D:\\projects\\wamicon24\\p2ms\\mmWave_abs\\comSys\\ber\\RFID_Reader.ber.t001_xx.r")
    else:
        fp = "D:\\projects\\wamicon24\\p2ms\\mmWave\\comSys\\ber\\"
        L = len("D:\\projects\\wamicon24\\p2ms\\mmWave\\comSys\\ber\\RFID_Reader.ber.t001_xx.r")
    
    p2ms = glob(fp+"*.p2m")

    ber_array = np.zeros((N,8))

    for p2m in p2ms:

        n = len(p2m) - L
        rx_id = int(p2m[-n:-4]) - 9
        tx_id = int(p2m[:L][-4:-2]) - 1#74,83 = Linux; 56, 65 = Windows

        with open(p2m, 'r') as f:
            ber = 10**float(f.readlines()[-1].split('  ')[-2])#.split('\n')
        # if p2m == "D:\\projects\\wamicon24\\p2ms\\100_txrx\\comSys\\ber\\RFID_Reader.ber.t001_09.r001.p2m":
        #     print(prx)
        ber_array[rx_id][tx_id] += ber
    
    # for idx, ber in enumerate(prx_array):
    #     plt.plot(10**ber)
    
    # plt.show()
    return ber_array

def plotSNR(absorber):
    if absorber == 1:
        fp = "D:\\projects\\wamicon24\\p2ms\\mmWave_abs\\comSys\\noise\\"
        L = len("D:\\projects\\wamicon24\\p2ms\\mmWave_abs\\comSys\\noise\\RFID_Reader.noise.t001_xx.r")
    else:
        fp = "D:\\projects\\wamicon24\\p2ms\\mmWave\\comSys\\noise\\"
        L = len("D:\\projects\\wamicon24\\p2ms\\mmWave\\comSys\\noise\\RFID_Reader.noise.t001_xx.r")
    
    p2ms = glob(fp+"*.p2m")

    noise_array = np.zeros((N,8))
    snr_array = np.zeros((N,8))

    for p2m in p2ms:
        n = len(p2m) - L
        rx_id = int(p2m[-n:-4]) - 9
        tx_id = int(p2m[:L][-4:-2]) - 1

        with open(p2m, 'r') as f:
            params = f.readlines()[-1].split('  ')
            # if 'RFID_Reader.noise.t001_01.r009.p2m' in p2m:
            #     print(params)
            snr = float(params[-4])
            noise = float(params[-5])

            # if 'RFID_Reader.noise.t001_04.r545.p2m' in p2m:
            #     print('snr: ', snr)

            sir = float(params[-3])
            ebn0 = snr - 10*np.log10(1 + 10**((snr-sir)/10))
        noise_array[rx_id][tx_id] += ebn0
        snr_array[rx_id][tx_id] += snr 

    # for idx, snr in enumerate(noise_array):
    #     plt.plot(snr)
    # plt.show()
    
    return noise_array, snr_array


def plotCDF(absorber):
    states = []
    prx_array = plotPWR(absorber)
    for idx, pw in enumerate(prx_array):
        if alg == 'ap':
            state = adaptivePursuit(pw, idx) - 2
        if alg == 'eg':
            state = epsilonGreedy(pw, q)
            n[state] += 1
            q[state] += (1 / n[state]) * (1000 + pw[state] - q[state])
        
        if alg == 'r':
            state = np.random.randint(len(p))
        states.append(state+1)
    
    return states

if metric == 'pwr':
    prx_array = plotPWR()
    for pw in prx_array.T:
        pw_sm = savgol_filter(pw, 71, 3)
        plt.plot(pw_sm)
    plt.ylim(-65,-54)
    plt.show()

if metric == 'ber':
    ber_array_abs = plotBER(1)
    ber_array = plotBER(0)
    # snr_array, _ = plotSNR(absorber)
    # plt.scatter(snr_array, ber_array, s = 5)
    # plt.yscale('log')
    plt.plot(ber_array.T[7], c='g')
    plt.plot(ber_array_abs.T[7], c='r')

    plt.show()

if metric == 'snr':
    _ , snr_array = plotSNR(absorber)
    plt.plot(snr_array)

    plt.show()

if metric == 'cdf':
    states = plotCDF(0)
    states_abs = plotCDF(1)

    ber_abs = []
    ber = []
    ebn0_abs = []
    ebn0 = []
    snr = []
    snr_abs = []
    for i, st in enumerate(states_abs):
        if i+9 < 10:
            rx = '00{}'.format(i+9)
        if 10 <= i+9  < 100:
            rx = '0{}'.format(i+9)            
        if i+9 >= 100:
            rx = '{}'.format(i+9)
       
        p2m_abs = "D:\\projects\\wamicon24\\p2ms\\mmWave_abs2\\comSys\\noise\\RFID_Reader.noise.t001_0{}.r{}.p2m".format(st, rx)
        p2m_abs_ber = "D:\\projects\\wamicon24\\p2ms\\mmWave_abs2\\comSys\\ber\\RFID_Reader.ber.t001_0{}.r{}.p2m".format(st, rx)

        with open(p2m_abs, 'r') as f:
            params = f.readlines()[-1].split('  ')
            # if 'RFID_Reader.noise.t001_01.r009.p2m' in p2m:
            #     print(params)
            sr = float(params[-4])
            noise = float(params[-5])

            # if 'RFID_Reader.noise.t001_04.r545.p2m' in p2m_abs:
            #     print('snr: ', sr)

            sir = float(params[-3])
            eb = sr - 10*np.log10(1 + 10**((sr-sir)/10))
        
        with open(p2m_abs_ber, 'r') as f:
            br = 10**float(f.readlines()[-1].split('  ')[-2])

        ber_abs.append(br)
        ebn0_abs.append(eb)
        snr_abs.append(sr)

    for i, st in enumerate(states):
        if i+9 < 10:
            rx = '00{}'.format(i+9)
        if 10 <= i+9  < 100:
            rx = '0{}'.format(i+9)            
        if i+9 >= 100:
            rx = '{}'.format(i+9)
       
        p2m = "D:\\projects\\wamicon24\\p2ms\\mmWave2\\comSys\\noise\\RFID_Reader.noise.t001_0{}.r{}.p2m".format(st, rx)
        p2m_ber = "D:\\projects\\wamicon24\\p2ms\\mmWave2\\comSys\\ber\\RFID_Reader.ber.t001_0{}.r{}.p2m".format(st, rx)

        with open(p2m, 'r') as f:
            params = f.readlines()[-1].split('  ')
            # if 'RFID_Reader.noise.t001_01.r009.p2m' in p2m:
            #     print(params)
            sr = float(params[-4])
            noise = float(params[-5])

            # if 'RFID_Reader.noise.t001_04.r545.p2m' in p2m:
            #     print('snr: ', sr)

            sir = float(params[-3])
            eb = sr - 10*np.log10(1 + 10**((sr-sir)/10))
        
        with open(p2m_ber, 'r') as f:
            br = 10**float(f.readlines()[-1].split('  ')[-2])

        ber.append(br)
        ebn0.append(eb)
        snr.append(sr)

    snr.sort()
    snr_abs.sort()
    pr = []
    pr_abs = []

    snr = np.array(snr)

    snr_abs = np.array(snr_abs)

    snr = snr[snr > 0]
    snr_abs = snr_abs[snr_abs > 0]

    for c in snr:
        num = np.count_nonzero(snr <= c)
        pr.append(num/len(snr))

    for c in snr_abs:
        num = np.count_nonzero(snr_abs <= c)
        pr_abs.append(num/len(snr_abs))

    if alg == 'ap':
        X = Pmax
    if alg == 'eg':
        X = epsilon
    if alg == 'r':
        X = 'xx'

    np.save('D:\\projects\\wamicon24\\data\\2\\snr_{}_{}.npy'.format(alg, X), snr)
    np.save('D:\\projects\\wamicon24\\data\\2\\snr_abs_{}_{}.npy'.format(alg, X), snr_abs)
    np.save('D:\\projects\\wamicon24\\data\\2\\pr_{}_{}.npy'.format(alg, X), pr)
    np.save('D:\\projects\\wamicon24\\data\\2\\pr_abs_{}_{}.npy'.format(alg, X), pr_abs)

    fig, ax = plt.subplots()
    plt.plot(snr, pr, color = 'g')
    plt.plot(snr_abs, pr_abs, color = 'r')
    plt.xlabel('SNR (dB)')
    plt.ylabel('CDF of SNR')
    plt.grid(True, color='grey', linestyle='--', linewidth=0.3)
    ax.set_aspect(max(np.max(snr), np.max(snr_abs)), adjustable='box')
    plt.show()
    


if metric == 'all':
    ber_array_abs = plotBER(1)
    snr_array_abs = plotSNR(1)
    ber_array = plotBER(0)
    snr_array = plotSNR(0)

    diff_snr = snr_array_abs - snr_array
    print(diff_snr[0:20])

    plt.scatter(snr_array, ber_array, s = 5, c='r')
    plt.scatter(snr_array_abs, ber_array_abs, s = 5, c='g')
    # plt.yscale('log')

    plt.show()

