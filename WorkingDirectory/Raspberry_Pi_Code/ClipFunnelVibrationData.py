"""
Brief:
    # function to clip part of data when funnel vibrates
    clipFunnelVibrationData Clip part of data when funnel vibrates
    xClipped = clipFunnelVibrationData ( magnitude, time,sampleRate, frameSize)
    clip length is the desired size of the cut to be made
"""
from calculateParticularFeature import *
from FastFourierTrans import fastFourierTrans
import numpy as np


def clipFunnelVibrationData( magnitude, time,sampleRate, frameSize):
    """
    This function takes the input acc data and runs fourier transformation on clipped data according to frameSize
    from the fourier transform data it finds the point of highest magnitudes which corresponds to coffee funnel
    vibrating
    :param magnitude: the acc data in numpy array
    :param time: time vector
    :param sampleRate: the rate ot which data is collected
    :param frameSize: the size of the frame
    :return: the clipped part of data where the coffee funnel vibrates
    """

    L = magnitude.shape[0]
    # eliminate any value which is out of +-800 to remove out-liners
    for i in range(0, L):
        if magnitude[i] > 800:
            magnitude[i] = 800
        elif magnitude[i] < -800:
            magnitude[i] = -800

    frameStart = 0
    frameEnd = frameStart + frameSize

    selectedFrameStart = 0
    selectedFrameRMS = 0

    # scan through the data successively and get the instance at which funnel vibrates
    while frameEnd < L:

        sliceMagnitude = magnitude[frameStart:frameEnd]
        # sliceMagnitude = rms(sliceMagnitude);
        [f1, P1] = fastFourierTrans(sliceMagnitude, sampleRate, 0, None)

        # if highest lies in the start of spectrum then dont consider that
        # frame since it might be just noise
        ind = np.where(P1 == np.amax(P1))
        ind = ind[0]
        if True:  # ind > (5*frameSize/(2*166.5)):
            sliceMagnitude = calculateParticularFeatureFunc(P1, 'Sum Of Frequency Amplitudes')

            if sliceMagnitude > selectedFrameRMS:
                selectedFrameStart = frameStart
                selectedFrameRMS = sliceMagnitude

        frameStart = frameEnd - 1900
        frameEnd = frameStart + frameSize

    # print(selectedFrameStart)
    xClipped = magnitude[selectedFrameStart: (selectedFrameStart + frameSize)]
    return xClipped


