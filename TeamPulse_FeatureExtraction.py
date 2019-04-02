from __future__ import print_function
import argparse
import os
import numpy as np
import glob
import matplotlib.pyplot as plt
from pyAudioAnalysis import audioFeatureExtraction as aF
from pyAudioAnalysis import audioTrainTest as aT
from pyAudioAnalysis import audioSegmentation as aS
from pyAudioAnalysis import audioVisualization as aV
from pyAudioAnalysis import audioBasicIO
from scipy.io import wavfile

import matplotlib.patches


#---------------------BASIC PLOT OF AN AUDIO--------------------#

sr, data = wavfile.read('T:\\snore.wav')
times = np.arange(len(data))/float(sr)
plt.figure(figsize=(30, 4))
plt.fill_between(times, data[:,0], data[:,1], color='k') 
plt.xlim(times[0], times[-1])
plt.xlabel('time (s)')
plt.ylabel('amplitude')
plt.savefig('plot.png', dpi=100)
plt.show()

#directory=""
#--------------------FILE CONVERSIONS--------------------------#
def dirMp3toWavWrapper(directory, samplerate, channels):
    if not os.path.isdir(directory):
        raise Exception("Input path not found!")

    useMp3TagsAsNames = True
    audioBasicIO.convertDirMP3ToWav(directory, samplerate, channels,
                                    useMp3TagsAsNames)

def dirWAVChangeFs(directory, samplerate, channels):
    if not os.path.isdir(directory):
        raise Exception("Input path not found!")

    audioBasicIO.convertFsDirWavToWav(directory, samplerate, channels)

#------------------FEATURE EXTRACTION----------#


def featureExtractionFileWrapper(wav_file, out_file, mt_win, mt_step,
                                 st_win, st_step):
    if not os.path.isfile(wav_file):
        raise Exception("Input audio file not found!")

    aF.mtFeatureExtractionToFile(wav_file, mt_win, mt_step, st_win,
                                 st_step, out_file, True, True, True)


def beatExtractionWrapper(wav_file, plot):
    if not os.path.isfile(wav_file):
        raise Exception("Input audio file not found!")
    [fs, x] = audioBasicIO.readAudioFile(wav_file)
    F, _ = aF.stFeatureExtraction(x, fs, 0.050 * fs, 0.050 * fs)
    bpm, ratio = aF.beatExtraction(F, 0.050, plot)
    print("Beat: {0:d} bpm ".format(int(bpm)))
    print("Ratio: {0:.2f} ".format(ratio))


def featureExtractionDirWrapper(directory, mt_win, mt_step, st_win, st_step):
    if not os.path.isdir(directory):
        raise Exception("Input path not found!")
    aF.mtFeatureExtractionToFileDir(directory, mt_win, mt_step, st_win,
                                    st_step, True, True, True)




#------------------VISUALIZATIONS---------------------#


def featureVisualizationDirWrapper(directory):
    if not os.path.isdir(directory):
        raise Exception("Input folder not found!")
    aV.visualizeFeaturesFolder(directory, "pca", "")
    #aV.visualizeFeaturesFolder(directory, "lda", "artist")


def fileSpectrogramWrapper(wav_file):
    if not os.path.isfile(wav_file):
        raise Exception("Input audio file not found!")
    [fs, x] = audioBasicIO.readAudioFile(wav_file)
    x = audioBasicIO.stereo2mono(x)
    specgram, TimeAxis, FreqAxis = aF.stSpectogram(x, fs, round(fs * 0.040),
                                                   round(fs * 0.040), True)


def fileChromagramWrapper(wav_file):
    if not os.path.isfile(wav_file):
        raise Exception("Input audio file not found!")
    [fs, x] = audioBasicIO.readAudioFile(wav_file)
    x = audioBasicIO.stereo2mono(x)
    specgram, TimeAxis, FreqAxis = aF.stChromagram(x, fs, round(fs * 0.040),
                                                   round(fs * 0.040), True)


#----------------------FEATURE EXTRACTION----------------#

def silenceRemovalWrapper(inputFile, smoothingWindow, weight):
    if not os.path.isfile(inputFile):
        raise Exception("Input audio file not found!")

    [fs, x] = audioBasicIO.readAudioFile(inputFile)
    segmentLimits = aS.silenceRemoval(x, fs, 0.05, 0.05,
                                      smoothingWindow, weight, True)
    for i, s in enumerate(segmentLimits):
        strOut = "{0:s}_{1:.3f}-{2:.3f}.wav".format(inputFile[0:-4], s[0], s[1])
        wavfile.write(strOut, fs, x[int(fs * s[0]):int(fs * s[1])])


def trainHMMsegmenter_fromfile(wavFile, gtFile, hmmModelName, mt_win, mt_step):
    if not os.path.isfile(wavFile):
        print("Error: wavfile does not exist!")
        return
    if not os.path.isfile(gtFile):
        print("Error: groundtruth does not exist!")
        return

    aS.trainHMM_fromFile(wavFile, gtFile, hmmModelName, mt_win, mt_step)


def trainHMMsegmenter_fromdir(directory, hmmModelName, mt_win, mt_step):
    if not os.path.isdir(directory):
        raise Exception("Input folder not found!")
    aS.trainHMM_fromDir(directory, hmmModelName, mt_win, mt_step)


def speakerDiarizationWrapper(inputFile, numSpeakers, useLDA):
    if useLDA:
        aS.speakerDiarization(inputFile, numSpeakers, plot_res=True)
    else:
        aS.speakerDiarization(inputFile, numSpeakers, lda_dim=0, plot_res=True)
        


def segmentclassifyFileWrapper(inputWavFile, model_name, model_type):
    if not os.path.isfile(model_name):
        raise Exception("Input model_name not found!")
    if not os.path.isfile(inputWavFile):
        raise Exception("Input audio file not found!")
    gtFile = ""
    if inputWavFile[-4::]==".wav":
        gtFile = inputWavFile.replace(".wav", ".segments")
    if inputWavFile[-4::]==".mp3":
        gtFile = inputWavFile.replace(".mp3", ".segments")
    aS.mtFileClassification(inputWavFile, model_name, model_type, True, gtFile)


def segmentclassifyFileWrapperHMM(wavFile, hmmModelName):
    gtFile = wavFile.replace(".wav", ".segments")
    aS.hmmSegmentation(wavFile, hmmModelName, plot_res=True,
                       gt_file_name=gtFile)


def speakerDiarizationWrapper(inputFile, numSpeakers, useLDA):
    if useLDA:
        aS.speakerDiarization(inputFile, numSpeakers, plot_res=True)
    else:
        aS.speakerDiarization(inputFile, numSpeakers, lda_dim=0, plot_res=True)
#------------------TRAINING THE CLASSIFIER AND CLASSIFYING THE AUDIO SOUNDS--------------#
    

def classifyFileWrapper(inputFile, model_type, model_name):
    if not os.path.isfile(model_name):
        raise Exception("Input model_name not found!")
    if not os.path.isfile(inputFile):
        raise Exception("Input audio file not found!")

    [Result, P, classNames] = aT.fileClassification(inputFile, model_name,
                                                    model_type)
    print("{0:s}\t{1:s}".format("Class", "Probability"))
    for i, c in enumerate(classNames):
        print("{0:s}\t{1:.2f}".format(c, P[i]))
    print("Winner class: " + classNames[int(Result)])    

def trainClassifierWrapper(method, beat_feats, directories, model_name):
    if len(directories) < 2:
        raise Exception("At least 2 directories are needed")
    aT.featureAndTrain(directories, 1, 1, aT.shortTermWindow, aT.shortTermStep,
                       method.lower(), model_name, compute_beat=beat_feats)
    
    
def classifyFolderWrapper(inputFolder, model_type, model_name,
                          outputMode=False):
    if not os.path.isfile(model_name):
        raise Exception("Input model_name not found!")
    types = ('*.wav', '*.aif',  '*.aiff', '*.mp3')
    wavFilesList = []
    for files in types:
        wavFilesList.extend(glob.glob((inputFolder + files)))
    wavFilesList = sorted(wavFilesList)
    if len(wavFilesList) == 0:
        print("No WAV files found!")
        return
    Results = []
    for wavFile in wavFilesList:
        [Result, P, classNames] = aT.fileClassification(wavFile, model_name,
                                                        model_type)
        Result = int(Result)
        Results.append(Result)
        if outputMode:
            print("{0:s}\t{1:s}".format(wavFile, classNames[Result]))
    Results = numpy.array(Results)

    # print distribution of classes:
    [Histogram, _] = numpy.histogram(Results,
                                     bins=numpy.arange(len(classNames) + 1))
    for i, h in enumerate(Histogram):
        print("{0:20s}\t\t{1:d}".format(classNames[i], h))
        
def speakerDiarizationWrapper(inputFile, numSpeakers, useLDA):
    if useLDA:
        aS.speakerDiarization(inputFile, numSpeakers, plot_res=True)
    else:
        aS.speakerDiarization(inputFile, numSpeakers, lda_dim=0, plot_res=True)
def thumbnailWrapper(inputFile, thumbnailWrapperSize):
    st_window = 0.5
    st_step = 0.5
    if not os.path.isfile(inputFile):
        raise Exception("Input audio file not found!")

    [fs, x] = audioBasicIO.readAudioFile(inputFile)
    if fs == -1:    # could not read file
        return

    [A1, A2, B1, B2, Smatrix] = aS.musicThumbnailing(x, fs, st_window, st_step,
                                                     thumbnailWrapperSize)

    # write thumbnailWrappers to WAV files:
    if inputFile.endswith(".wav"):
        thumbnailWrapperFileName1 = inputFile.replace(".wav", "_thumb1.wav")
        thumbnailWrapperFileName2 = inputFile.replace(".wav", "_thumb2.wav")
    if inputFile.endswith(".mp3"):
        thumbnailWrapperFileName1 = inputFile.replace(".mp3", "_thumb1.mp3")
        thumbnailWrapperFileName2 = inputFile.replace(".mp3", "_thumb2.mp3")
    wavfile.write(thumbnailWrapperFileName1, fs, x[int(fs * A1):int(fs * A2)])
    wavfile.write(thumbnailWrapperFileName2, fs, x[int(fs * B1):int(fs * B2)])
    print("1st thumbnailWrapper (stored in file {0:s}): {1:4.1f}sec" \
          " -- {2:4.1f}sec".format(thumbnailWrapperFileName1, A1, A2))
    print("2nd thumbnailWrapper (stored in file {0:s}): {1:4.1f}sec" \
          " -- {2:4.1f}sec".format(thumbnailWrapperFileName2, B1, B2))

    # Plot self-similarity matrix:
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect="auto")
    plt.imshow(Smatrix)
    # Plot best-similarity diagonal:
    Xcenter = (A1 / st_step + A2 / st_step) / 2.0
    Ycenter = (B1 / st_step + B2 / st_step) / 2.0

    e1 = matplotlib.patches.Ellipse((Ycenter, Xcenter),
                                    thumbnailWrapperSize * 1.4, 3, angle=45,
                                    linewidth=3, fill=False)
    ax.add_patch(e1)

    plt.plot([B1/ st_step, Smatrix.shape[0]], [A1/ st_step, A1/ st_step], color="k",
             linestyle="--", linewidth=2)
    plt.plot([B2/ st_step, Smatrix.shape[0]], [A2/ st_step, A2/ st_step], color="k",
             linestyle="--", linewidth=2)
    plt.plot([B1/ st_step, B1/ st_step], [A1/ st_step, Smatrix.shape[0]], color="k",
             linestyle="--", linewidth=2)
    plt.plot([B2/ st_step, B2/ st_step], [A2/ st_step, Smatrix.shape[0]], color="k",
             linestyle="--", linewidth=2)

    plt.xlim([0, Smatrix.shape[0]])
    plt.ylim([Smatrix.shape[1], 0])

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    plt.xlabel("frame no")
    plt.ylabel("frame no")
    plt.title("Self-similarity matrix")

    plt.show()