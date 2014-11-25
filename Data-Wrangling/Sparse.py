import numpy as np
import re
file_path=r'C:\Users\swei\Desktop\unweighted_events.lhe'
f=open(file_path)

cnt=0
arr=[]

for piece in re.split('<event>',f.read()):
    cnt+=1
    if cnt>1:
        data=re.split('\s+',piece)
        results= data[33:59]
        arr.append([float(x)for x in results])
