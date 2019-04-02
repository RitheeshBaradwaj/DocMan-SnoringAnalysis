"""import numpy as np
import math
from scipy.io import wavfile
from matplotlib import pyplot as plt
import soundfile as sf
import pandas as pd """

#===========================PREPROCESSING=========================#

def tsnrFilter(signal, oldmag, averageFrqSpec, NFFT, hanwin):
    alpha=0.98
    winy=np.multiply(signal,hanwin)
    ffty = np.fft(winy,NFFT)
    phasey = np.angle(ffty)
    magy=abs(ffty)
    postsnr = ((magy**2)/averageFrqSpec)-1
    postsnr=max(postsnr,0.01)
    eta = alpha*((oldmag**2)/averageFrqSpec)+(1-alpha)*postsnr
    newmag=(eta/(eta+1))*magy
    tsnr = (newmag**2)/averageFrqSpec
    Gtsnr = tsnr/(tsnr+1)
    Gtsnr = gaincontrol(Gtsnr,math.floor(NFFT/2))
    newmag = Gtsnr*magy
    ffty = newmag*(math.exp((1j)*phasey))
    return [newmag, ffty] 

def gaincontrol(Gain,ConstraintInLength):
    meanGain = np.mean(Gain**2)
    [NFFT, nSignals] = Gain.shape
    win1 = np.hanning(ConstraintInLength)
    win=win1
    for n in range(2,nSignals):
        win=[win,win1]
    
    ImpulseR=np.real(np.fft.ifft(Gain))
    ImpulseR2=np.concatenate(np.multiply((ImpulseR[1:(math.floor(ConstraintInLength/2)),:]),(win[1+1+floor(ConstraintInLength/2):ConstraintInLength,:])),np.zeros(NFFT-ConstraintInLength,nSignals),np.multiply(ImpulseR[NFFT-floor(ConstraintInLength/2)+1:NFFT,:],win[1:floor(ConstraintInLength/2),:]))
    
    NewGain=abs(np.fft(ImpulseR2,NFFT))
    meanNewGain=np.mean(NewGain**2)
    gainNormalize = np.sqrt(meanGain/meanNewGain)
   for n in range(2,nSignals):
       NewGain1 = [NewGain1 ,(np.multiply(NewGain[:,n],gainNormalize[:,n]))]

   NewGain = NewGain1
   
   return NewGain

def WienerNoiseReduction(ns,fs,IS):
    [nValues,nSignals]=ns.shape
    wl=round(fs*0.25)
    NFFT=2*wl
    hanwin1=np.hanning(wl)
    hanwin=hanwin1
    for n in range(n,nsignals):
        hanwin=[hanwin,hanwin1]
    SP = 0.01
    normFactor = 1/SP    
    overlap = round((1-SP)*wl)
    offset = wl - overlap
    max_m = round((nValues-NFFT)/offset)
    oldmag = np.zeros((NFFT, nSignals))
    news = np.zeros((nValues, nSignals))
    count = 0
    nsum =np.zeros(NFFT, nSignals)
    for m in range(0,(IS-wl)):
        nwin = np.multiply(ns(m+1,m+wl),hanwin)
        nsum = nsum+(abs(np.fft(nwin,NFFT))**2)
        count = count + 1
    averageFrqSpec = (nsum)/count
    
    for m in range(0,max_m):
        begin =(m*offset)+1
        iend = (m*offset)+w
        signal=ns[begin:iend,:]
        [newmag,ffty]=tsnrFilter(signal, oldmag, averageFrqSpec, NFFT, hanwin)
        oldmag = abs(newmag)
        news[begin:begin+NFFT-1,:]=news[begin:begin+NFFT-1,:]+((np.real(np.fft.ifft(ffty,NFFT)))/normFactor)
    esTSNR=news
    return esTSNR
        
