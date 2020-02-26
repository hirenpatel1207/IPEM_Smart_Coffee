"""
Brief:
     This script provides with additional methods required
     for processing of the data.
     This method stores the data passed in dataString in filename
"""

import os
script_dir = os.path.dirname(__file__)


def store_data (fileName, dataString):
    """
    To store the data in the file.
    :param fileName: the name of the file (Time stamp string)
    :param dataString: the string of data that is supposed to store or append to existing file
    :return: None
    """
    rel_path = "data/" + (fileName) + ".txt"
    filePath = os.path.join(script_dir, rel_path)
    f = open(filePath, 'a')
    f.write(str(dataString))
    f.close()

    pass



