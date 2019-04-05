#================================SEGMENTATION============================#   
    
def segmentation(Y,fs,n):
    y=Y
    if np.isnan(y[1]):
        y=y[:,2]
    else:
        y=y.reshape((2*len(y)),1)
    a=(math.floor(n*fs))*(math.floor(length(y)/(n*fs)))
    y=y[1:a]
    y1=y.reshape((floor(n*fs)),floor(len(y)/(n*fs)))
    y2=np.zeros(n*fs,(len(y)/(n*fs)))
    Sd=np.std(y1)
    Avg_sd=np.mean(Sd)
    
    [k1,k2]=y1.shape
    M=np.zeros(1,len(k2))
    for i in range(1,k2):
        M[i]=np.mean(y1[:,i])
    for i in range(1,k2):
        M[i]=np.mean(y1[:,i])
    for i in range(1,k2):
        if abs(math.floor(M[i]))>(6*Avg_sd):
            y2[:,i]=y1[:,i]
    
    y2=y2.reshape((k2*k1),1)
    y3=np.zeros(1,len(y2))
    p=0
    for i in range(1,(len(y2)-(math.floor(0.5*fs)))):
        for j in range(1,(math.floor(0.5*fs))):
            if y2[i]>0 and y2(i+j)>0:
                y3[i:i+j]=max(y2)/2
    
    y4=np.zeros(1,len(y2))
    for i in range(1,len(y3)):
        if y3[i]==(max(y2)/2):
            p=p+1
        if p>0 and y3[i]==0:
            if p>0.3*fs and p<2*fs:
                y4[i-p-1:p]
                p=0

    return y2
