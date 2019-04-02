
#===============================SnoringAnalysis=================================#

def SnoringAnalysis(x1,fs,SleepTime):
    L1=len(x1)
    count1=0
    count2=0
    Apnea_count=0
    x2=np.flip(x1)
    for i in range(1,L1):
        if x1[i]==0:
            count1=count1+1
        else:
            break
    for i in range(1,L1):
        if x2[i]==0:
            count2=count2+1
        else:
            break
        
    signal=x1[count1+1:-count2]
    L2=len(signal)
    duration=10*fs
    k=1
    p=1
    for i in range(1,L2):
        if signal(p+1,p+duration)==0:
            if k==1:
                Apnea_count = Apnea-count + 1
                k=0

        if k==1:
            for j in range(p+1,p+duration):
                if signal(j)!=0:
                    k=1
                    p=j
                    break
        else:
            for j in range(duration+p,L2-duration-1):
                if signal(j)!=0:
                    k=1
                    p=j
                    break
        if p>=L2-duration:
            break
    AHI=(Apnea_count*3600)/SleepTime
    return AHI
