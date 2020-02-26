from AnalyzeDataFunctions import *
import datetime
import os
from SqlDatabaseUtils import databaseUtils
from AnalyzeDataFunctions import postProcessForUI
fileName = "CoffeeData.txt"
filePath = "data"
#predictNewDataPoint(fileName, filePath, None)

# for testing only
#featureVec = np.array([2.45181119e+02,5.98623192e+04,1.58575550e+01,7.69603723e+03,
 #7.84227743e+00])
#normalzedVec = normalizeFeatures(featureVec, None)

filePath = os.path.join(filePath, fileName)
# data = np.loadtxt(import_file_path)
#
# presentTime = datetime.datetime(2000, 1, 1)
# arr = np.array([presentTime + datetime.timedelta(seconds=i*0.001) for i in range(data.shape[0])])
# #arr = np.array([base + datetime.timedelta(seconds=i) for i in range(24)])
#
# arr = np.array((data.shape[0], 2))
# for i in range (data.shape[0]):
#     arr[i, 0] =presentTime
#     arr[i,1] = data[i]
#     presentTime = presentTime +  datetime.timedelta(seconds=3)

dbObj = databaseUtils();
#dbObj.create_table()
timeNow = datetime.datetime.now()

insertInitialData = False  # to create first few entries of table artificially
if insertInitialData:
    # create tasks

    task_1 = (1, timeNow.strftime("%Y-%m-%d %H:%M:%S"), 2)
    task_2 = (2, timeNow.strftime("%Y-%m-%d %H:%M:%S"), 2)
    task_3 = (3, timeNow, 1)
    task_4 = (4, timeNow, 1)
    task_5 = (5, timeNow, 0)
    i = dbObj.insert_data_task( task_1)
    i = dbObj.insert_data_task( task_2)
    i = dbObj.insert_data_task( task_3)
    i = dbObj.insert_data_task( task_4)
    i = dbObj.insert_data_task( task_5)

#id = dbObj.getLastIdFromDataBase()
#dbObj.insert_data_task((id+1, timeNow.strftime("%Y-%m-%d %H:%M:%S"), 2))
#dbObj.getLastFiveCoffeeFromDataBase()
#dbObj.saveLastFiveCoffeeToFile(os.path.join("DisplayDataForWebPage", "DisplayCoffeeHistoryData.txt"))
currentFileTime = datetime.datetime.now() - timedelta(minutes=3)
os.rename(os.path.join("data", "temp.txt"), os.path.join("data", str(currentFileTime.strftime("%Y_%m_%d_%H_%M_%S"))+".txt"))
postProcessForUI(currentFileTime,)