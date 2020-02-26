import numpy as np
#import matplotlib.pyplot as plt
import os,math
from calculateParticularFeature import *
from ClipFunnelVibrationData import clipFunnelVibrationData
from emailUtils import sendEmail
from AnalyzeDataFunctions import predictNewDataPoint
from SqlDatabaseUtils import databaseUtils
import datetime
#fileName = "Tempfortest2.txt"
#filePath = "data"


#import_file_path = os.path.join(filePath, fileName)
#data = np.loadtxt(import_file_path)
# print first few values for sanity check
#print(str(data[1:10]) + "\n")


#normMagnitude = data - np.average(data)
#clipped = clipFunnelVibrationData( normMagnitude, 0,333, 2000)
#print(np.sum(clipped))
#plt.plot(data)
#plt.show()
dbObj = databaseUtils()
coffeeId, coffeeNumber = dbObj.getIdAndNumberFromDataBase(2)

print("id" +str(coffeeId) + "number" + str(coffeeNumber))
currentFileTime  = datetime.datetime.now()
dbObj.insert_data_task((coffeeId, currentFileTime.strftime("%Y-%m-%d %H:%M:%S"), 2 , coffeeNumber))

dbObj.saveLastFiveCoffeeToFile(os.path.join("DisplayDataForWebPage", "DisplayCoffeeHistoryData.txt"))