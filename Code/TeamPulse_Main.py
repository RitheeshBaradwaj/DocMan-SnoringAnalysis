 #=========================MAIN FUNCTION===========================#


from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np
import soundfile as sf
[fs,y] = wavfile.read('C:\\Users\\ritheesh\\Desktop\\snore.wav') #filename.wav
print(len(y))
print(fs)
[m, n] = y.shape
print(m)
print(n)
if n <=1:
    if (len(y))%2!= 0:
        y=[y,0]
    k=length(y)/2
    y=y.reshape(k,2)
    [m,n]=y.shape

IS=round(0.3*fs)
info = sf.SoundFile('C:\\Users\\ritheesh\\Desktop\\snore.wav')
print('samples = {}'.format(len(info)))
print('sample rate = {}'.format(info.samplerate))
print('seconds = {}'.format(len(info) / info.samplerate))
#ploting the .WAV file
print(fs)
print(y.size/float(fs))
plt.plot(y)
plt.xlabel('time (s)')
plt.ylabel('amplitude')
plt.show()   
    
#================input data and analysis===========================#

            
#[Fs, Input] = aIO.readAudioFile('C:\\Users\\ritheesh\\Desktop\\snore.wav')       

#info = sf.SoundFile('C:\\Users\\akhil\\Desktop\\snore.wav')
#print('samples = {}'.format(len(info)))
#print('sample rate = {}'.format(info.samplerate))
#print('seconds = {}'.format(len(info) / info.samplerate))  


#==============Calling preprocessing function===============#
esTSNR=WienerNoiseReduction1(y,fs,IS)

#===============Calling segmentation function================#
y2=Segmentation1(esTSNR,fs,0.1)


Fs=fs  
name=input("enter name :")
print(name)
sex=imput("enter sex(M/F) :")
print(sex)
age= input("enter age :");
Height=input("Height(cms) :")
Weight=input("Weight(kgs) :")
BMI=(Weight/(Height**2))*10000
SleepTime =(length(y)/fs)

#===================Calling SnoringAnalysis function ======================#

AHI=SnoringAnalysis(y2,fs,SleepTime)


TEST_AHI=AHI
if AHI<5:
   print("RESULT : NORMAL(NO SLEEP APNEA")
elif AHI>=5 and AHI<15:
    print("RESULT : MILD SLEEP APNEA")
elif AHI>=15 and AHI<30:
    print("RESULT : MODERATE SLEEP APNEA")
elif AHI>=30:
    print("RESULT : SEVERE SLEEP APNEA")
   