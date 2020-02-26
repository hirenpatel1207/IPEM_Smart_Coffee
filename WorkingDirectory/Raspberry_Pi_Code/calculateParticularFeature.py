"""
Brief:
this file calculates particular features passed in the argument.
Calculate various features to generate the feature vector which can be used for prediction
"""
import numpy as np


# Note: pass the feature name correctly to avoid error
def calculateParticularFeatureFunc(x, featureName):
    # calculateParticularFeature This function calculates various features based on arguments
    #   X is column vector which has the given data
    #   featureName is the name of feature the user wants to calculate
    featureVal = 0

    if(featureName =='Root Mean Square'):
        featureVal = np.sqrt(np.mean(np.square(x)))

    if (featureName == 'Variance'):
        featureVal = np.var(x)

    if (featureName == 'Mean'):
        featureVal = np.mean(x)

    if (featureName == 'Sum Of Frequency Amplitudes'):
        featureVal = np.sum(x)

    if (featureName == 'Root Variance Of Frequency'):
        featureVal = np.sqrt( np.var(x))

    # return the featureValue
    return featureVal



