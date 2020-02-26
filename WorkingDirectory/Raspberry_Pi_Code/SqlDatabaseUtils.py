"""
Brief:
     This file handles sqlite database utilities
     Read each function description properly to get its usage
     Keep the database file in the same directory or else change the path accordingly
"""
import sqlite3
from sqlite3 import Error


# this is a class that wraps all the functions
# instantiate an object of this class and use the functions accordingly
class databaseUtils:

    def __init__(self,):

        # !!! change the path according to place where database is placed !!!!!!!!!
        # database = r"E:\ENGG\Mechatronics\Univesity_Work_WHB\IPEM_Sensor_Work\Rasberry\PyCharmLocalDev\CoffeeDataBase.db"
        # database = r"/home/pi/IPEM/SmartCoffeeMQTT"
        database = r"CoffeeDataBase.db"       # if database is present in same folder as the script
        self.conn = self.create_connection(database)
        self.sql_create_coffee_table = """ CREATE TABLE IF NOT EXISTS coffeehistory (
                                                id INTEGER PRIMARY KEY,
                                                coffeetime TIMESTAMP NOT NULL,
                                                status INTEGER NOT NULL 
                                                coffeenumber INTEGER 

                                            ); """

    def create_connection(self, database):
        """
         create a database connection to a SQLite database
        :param database: the path of the database which has to be connected to
                          refer class constructor to set that
        :return: conn variable
        """
        conn = None
        try:
            conn = sqlite3.connect(database)
            print(sqlite3.version)
        except Error as e:
            print(e)

        return conn

    def create_table(self,):
        """
        create a table from the create_table_sql statement
        connection object
         Set this variable correctly -> create_table_sql: a CREATE TABLE statement
        :return: None
        """

        try:
            c = self.conn.cursor()
            c.execute(self.sql_create_coffee_table)
        except Error as e:
            print(e)
        pass


    def insert_data_task(self, task):
        """
        define insert task to add the coffee data to database
        to insert values into the table passed as task
        :param task: tuple of the data to be inserted
        :return:
        """


        sql = ''' INSERT INTO coffeehistory(id ,coffeetime,  status, coffeeNumber) VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()
        return cur.lastrowid

    # to get last 5 coffees from the database
    def getLastFiveCoffeeFromDataBase(self,):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return: the rows of the data obtained
        """
        cur = self.conn.cursor()
        cur.execute("SELECT coffeeNumber,coffeetime,status FROM coffeehistory  ORDER  BY id DESC LIMIT 5")
        # cur.execute("""SELECT * FROM( SELECT * FROM  coffeehistory  ORDER BY id
        # DESC LIMIT 3) ORDER  BY id ASC""")
        rows = cur.fetchall()
        # print("[Info] Querrying database and obtaining data")
        # for row in rows:
        #   print(row)

        return rows

    def saveLastFiveCoffeeToFile(self , filePath):
        """
        save last five coffees to a file for displaying it to database
        :param filePath:
        :return: None
        """
        data = self.getLastFiveCoffeeFromDataBase()
        f = open(filePath, "w")

        for row in data:
            f.write(str(row[0]) + ",")
            f.write(str(row[1]) + ",")
            if row[2] == 2:
                f.write("Full" + ",")
            elif row[2] == 1:
                f.write("Ok" + ",")
            else:
                f.write("Empty" + ",")
            # for t in row:
            #    f.write(str(t) + ",")
            f.write("\n")
        f.close()

        pass

    # To get the Id and coffee number that present coffee should be assigned to
    def getIdAndNumberFromDataBase(self, outputPrediction):
        """
        This function gets the Id (which is a unique number given to each coffee)
        and coffee number since the last time coffee was filled
        :param outputPrediction : the prediction of present coffee
        :param conn: the Connection object (present in class variables)
        :return:
        """
        # get the details of last coffee
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM coffeehistory  ORDER  BY id DESC LIMIT 1")

        rows = cur.fetchall()
        # print("[Info] Getting last id from database")
        #print(rows[0])
        lastCoffeeId = rows[0][0]
        lastCoffeeStatus = rows[0][2]
        lastCoffeeNumber =rows[0][3]

        # determining the details of present coffee
        presentCoffeeId = lastCoffeeId + 1
        if lastCoffeeStatus == 0 and outputPrediction == 2 :
            presentCoffeeNumber = 1
        else:
            presentCoffeeNumber = lastCoffeeNumber + 1

        return presentCoffeeId, presentCoffeeNumber

    # close the present connection in destructor
    def __del__(self):
        """ closes present connection"""
        self.conn.close()
        pass

# # only for internal use during development
# def main():
#
#
#
#
#
#     # create a database connection
#     conn = create_connection(database)
#
#     # create tables
#     if conn is not None:
#         # create coffee table
#         #create_table(conn, sql_create_coffee_table)
#         pass
#
#     else:
#         print("Error! cannot create the database connection.")
#
#     insertInitialData = False         # to create first few entries of table artificially
#     if insertInitialData:
#
#         # create tasks
#         timeNow = datetime.datetime.now()
#         task_1 = (1,timeNow, 2)
#         task_2 = (2, timeNow, 2)
#         task_3 = (3, timeNow, 1)
#         task_4 = (4, timeNow, 1)
#         task_5 = (5, timeNow, 0)
#         i = insert_data_task(conn, task_1)
#         i = insert_data_task(conn, task_2)
#         i = insert_data_task(conn, task_3)
#         i = insert_data_task(conn, task_4)
#         i = insert_data_task(conn, task_5)
#
#     # to get last 5 entires of data from the table
#     getLastIdFromDataBase(conn)
#     getLastFiveCoffeeFromDataBase(conn)
#     close_connection(conn)
#
#
# # comment out this line to avoid running main
# if __name__ == '__main__':
#     main()
