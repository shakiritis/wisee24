import os
import sys

file_id1 = sys.argv[1]
file_id2 = sys.argv[2]

fp = "D:\\projects\\wamicon24\\changes\\"

f1 = os.path.join(fp, 'RFID_Reader.mWave{}.xml'.format(file_id1))
f2 = os.path.join(fp, 'RFID_Reader.mWave{}.xml'.format(file_id2))

def matchorNot(text1, text2):
    flag = 1
    mismatch = -5
    if len(text1) != len(text2):
        flag *= 0
        for i in range(len(text1)):
            if text1[i] != text2[i]:
                mismatch = i+1
                break
        return flag, mismatch
        
    else:
        for i in range(len(text1)):
            if text1[i] == text2[i]:
                flag *= 1
            else:
                flag *= 0
            
            if flag == 0:
                return flag, mismatch
    
    return flag, mismatch


with open(f1, 'r') as f:
    text1 = f.readlines()

with open(f2, 'r') as f:
    text2 = f.readlines()
    
print(text1[1115] == text2[1115])

flag, mismatch = matchorNot(text1, text2)

if flag == 0:
    print("Mismatch @ line --> ", mismatch)
else:
    print("Match!!")