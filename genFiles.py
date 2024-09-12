import os
import sys
import numpy as np

fp = "D:\\projects\\wamicon24\\changes\\"
r = 2
N = 1000
center_x = 2.5
center_y = 2.5

mode = sys.argv[1]

if mode == 'txrx':
    with open (fp + 'txrx.txt', 'r') as f:
        text = f.readlines()

    # print(text[-1])
    for i in range(N):
        x = str(np.round(center_x + r*np.cos((2*np.pi*i/N)), 12))
        y = str(np.round(center_y + r*np.sin((2*np.pi*i/N)), 12))
        z = '1.000000000000'
        text[0] = 'begin_<points> RX Point{}\n'.format(i+9)
        text[1] = 'project_id {}\n'.format(i+9)
        text[24] = '{} {} {}\n'.format(x, y, z)

        if i == 0:
            text.append('\n')
        
        with open (fp + 'full_txrx.txrx', 'a') as f:
            f.writelines(text)

if mode == 'xml':
    with open (fp + 'body.txt', 'r') as f:
        text = f.readlines()
    # print(text[-1])
    for i in range(N):
        x = str(np.round(center_x + r*np.cos((2*np.pi*i/N)), 12))
        y = str(np.round(center_y + r*np.sin((2*np.pi*i/N)), 12))
        text[10] = '                          <remcom::rxapi::Double Value="{}"/>\n'.format(x)
        text[13] = '                          <remcom::rxapi::Double Value="{}"/>\n'.format(y)
        text[23] = '                  <remcom::rxapi::Integer Value="{}"/>\n'.format(i+9)
        text[26] = '                  <remcom::rxapi::String Value="TX Point{}"/>\n'.format(i+9)
        
        if i == 0:
            text.append('\n')

        with open (fp + 'fullxml.xml','a') as f:
            f.writelines(text)

if mode == 'setup':
    with open (fp + 'setup.txt', 'r') as f:
        text = f.readlines()