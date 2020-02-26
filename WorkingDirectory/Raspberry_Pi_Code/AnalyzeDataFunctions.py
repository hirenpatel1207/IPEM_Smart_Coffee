"""
Brief:
    This script has various functions which analyse the data received through MQTT
    The mqtt subscriber should pass the timestamp and filepath to the predictNewDataPoint function which will pickup the
    file from the folder and start analyzing it.
"""

import os
from datetime import timedelta
from calculateParticularFeature import *
from ClipFunnelVibrationData import clipFunnelVibrationData
from FastFourierTrans import fastFourierTrans
from SqlDatabaseUtils import databaseUtils
from emailUtils import sendEmail


def predictNewDataPoint(currentFileTime, filePath , modelType):
    """
    This is the main function which can analyze the file based on data passed in it.
    It first check the min. length then extracts the features and applies predictive model on it.
    :param currentFileTime: the timestamp of file name in datetime.now() format
    :param filePath: the path relative to the directory in which code is placed and file is placed
    :param modelType: type of model to be used (pass None for now as it is unused for now)
    :return: None
    """

    fileName = currentFileTime.strftime("%Y_%m_%d_%H_%M_%S")   # getting string from timestamp
    # importing data reading the file
    import_file_path = os.path.join(filePath, fileName + ".txt")
    data = np.loadtxt(import_file_path)
    # print first few values for sanity check
    print("shape of a data" + str(data.shape) + "first few values are: " + str(data[0:5]) + "...")

    # process the imported data
    # if this is false data i.e. NOT a coffee then ignore
    if data.shape[0] < 15000:
        print("Not a coffee deleting the file")
        os.remove(import_file_path)    # uncomment only in deployment
        # pass
    else:
        # process the data and run predictive model on that
        # normalizing acc magnitude to remove gravity component
        data = data - 1000
        # create time vector of equally spacing of 3 ms
        time = np.ones((data.shape[0],), dtype=int)*3
        time = np.cumsum(time)
        sampleRate = 333.33
        # plt.plot(data)  # import matplotlib first if want to see that data
        # plt.show()

        # clipping funnel vibration data to process only that particular part
        frameSize = 2000
        clippedVibData = clipFunnelVibrationData(data, time, sampleRate, frameSize)

        # calculate the features from the clipped data
        print("Calculating features from clipped data...")
        featureVec = calculateFeatures(clippedVibData, sampleRate, 0)
        # print("The calculated feature Vec is:"+str(featureVec))

        # Normalizing the featureVec Using precomputed mean and variances
        normalizedVec = normalizeFeatures(featureVec, modelType)

        # append bias term with the feature vector
        normalizedVec = np.append(np.array([1]), normalizedVec,)
        # print("The Normalize Features final feature Vec is: " + str(normalizedVec))
        # predicting based on model
        outputPrediction = modelPredict(normalizedVec)

        # print on console according to model output
        if outputPrediction == 0:
            print("Coffee on the verge of getting empty")
        elif outputPrediction == 1:
            print("Coffee level Sufficient :)")
        else:
            print("Coffee level Almost Empty :) ")

        # call the update function which updates the files for GUI
        postProcessForUI(currentFileTime, outputPrediction)

        # end of function
    pass


def calculateFeatures(data, sampleRate , normalizeVal):
    """
     This function calls different feature functions and calculates feature vector
     The feature vector can then be used to predict state

    :param data: the actual data of acceleration values in numpy array format
    :param sampleRate: the rate at which data is collected
    :param normalizeVal: the normalization value of 'g' if present otherwise set it to '0'
    :return: vector of features of data
    """
    # creating numpy array of 5 elements to store the features
    featureVec = np.array([0.0, 0.0, 0.0, 0.0, 0.0])

    # calculating the time domain features
    featureVec[0] = calculateParticularFeatureFunc(data, 'Root Mean Square')
    featureVec[1] = calculateParticularFeatureFunc(data, 'Variance')
    featureVec[2] = calculateParticularFeatureFunc(data, 'Mean')
    # we need the frequency spectrum to calculate frequency domain features
    [f1, P1] = fastFourierTrans(data, sampleRate=sampleRate, normalizeVal=normalizeVal, windowType=None)
    # passing the spectrum data to get frequency domain of features
    featureVec[3] = calculateParticularFeatureFunc(P1, 'Sum Of Frequency Amplitudes')
    featureVec[4] = calculateParticularFeatureFunc(P1, 'Root Variance Of Frequency')

    return featureVec


def normalizeFeatures(featureVec, modelType):
    """
    This function is used to normalize the feature vector according to mean and variance calculated from training data.
    Place the normalization constants in a csv file in appropriate folder
    The first column of the csv file should contain mean values while second column should contain sigma
    :param featureVec: the original feature vec
    :param modelType: unused for now
    :return: the normalize feature vector
    """

    # importing the mu and sigma vectors from the csv file
    # change the below variable values if you are changing the folder or file name
    nomalizeValues = "normalizeValues.txt"
    filePath = "data/modelParameters"
    import_file_path = os.path.join(filePath, nomalizeValues)
    normalizingMat = np.loadtxt(import_file_path, delimiter=',')

    mu = normalizingMat[:, 0]
    sigma = normalizingMat[:, 1]
    normalizedVec = np.divide((featureVec - mu), sigma)

    return normalizedVec


def modelPredict(normalizedVec):
    """
    This function makes prediction based on normalized features and theta.
    this function requires theta vector to make predictions which should be placed in appropriate folder
    :param normalizedVec: the normalized feature vector
    :return: outputPrediction : model prediction which is an integer value
    """

    # load the theta vector
    thetaVecFile = "theta.txt"
    filePath = "data/modelParameters"
    import_file_path = os.path.join(filePath, thetaVecFile)
    thetaVec = np.loadtxt(import_file_path, delimiter=',')

    yPredict = np.dot(thetaVec, normalizedVec)

    if yPredict < 0.5:
        outputPrediction = 0
    elif yPredict > 0.5 and yPredict < 1.5:
        outputPrediction = 1
    else:
        outputPrediction = 2

    return outputPrediction


def postProcessForUI(currentFileTime, outputPrediction):
    """
    does the post processing of data
    store the data in database
    update the files of DisplayDataForWebPage for updating UI
    the updated files will be picked up by NodeRed
    :param currentFileTime: the timestamp of coffee which will be stored in database
    :param outputPrediction: integer value of mathematical model prediction
    :return: None
    """

    # initialize database class object to interact with the database
    dbObj = databaseUtils()

    # update the database with new entry. First we get the coffeeId, coffeeNumber that present coffee should get
    coffeeId, coffeeNumber = dbObj.getIdAndNumberFromDataBase(outputPrediction)

    dbObj.insert_data_task((coffeeId, currentFileTime.strftime("%Y-%m-%d %H:%M:%S"), outputPrediction , coffeeNumber))

    # we update three files required for the UI elements
    # 1. update DisplayLedData file
    # store red green or yellow in this file which will lightup the appropriate LED on UI
    f = open(os.path.join("DisplayDataForWebPage", "DisplayLedData.txt"), "w")

    if outputPrediction == 2:
        # store green
        f.write("led,GREEN")

    elif outputPrediction == 1:
        # store yellow-- led, YELLOW
        f.write("led,YELLOW")
    else:
        # store -- led, YELLOW
        f.write("led,RED")
    f.close()

    # 2. update DisplayCoffeeHistoryData file
    # here we store the data of last five coffees in a csv format
    dbObj.saveLastFiveCoffeeToFile(os.path.join("DisplayDataForWebPage", "DisplayCoffeeHistoryData.txt"))

    # 3. update DisplaySensorData file
    # to store the actual acceleration sensor values of the last coffee to make a plot
    # importing data reading the file
    fileName = currentFileTime.strftime("%Y_%m_%d_%H_%M_%S")
    import_file_path = os.path.join('data', fileName + ".txt")
    data = np.loadtxt(import_file_path)

    # create or update DisplaySensorData file with new data
    f = open(os.path.join("DisplayDataForWebPage", "DisplaySensorData.txt"), "w")
    for accData in data:
        t1 = timedelta(microseconds=3000)
        currentFileTime = currentFileTime + t1
        f.write(currentFileTime.strftime("%Y-%m-%d %H:%M:%S.%f")+"," + str(accData) + "\n")
    f.close()

    # handle email events
    # send email if coffee level is critical
    if outputPrediction == 0:

        sendEmail(outputPrediction)

    # end of function
    pass

