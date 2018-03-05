import sqlite3, os

class DBManager:

    def __init__(self):
        self.connection = sqlite3.connect(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "results.db")))
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS Info (ID INTEGER PRIMARY KEY AUTOINCREMENT, DayOfLastReport INTEGER NOT NULL)")
        self.connection.commit()
        self.cursor.execute("INSERT OR IGNORE INTO Info VALUES(NULL, '{}')".format(-1))
        self.connection.commit()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS Results (ID INTEGER PRIMARY KEY AUTOINCREMENT, Host INTEGER NOT NULL, PacketsSent INTEGER NOT NULL, PacketsReceived INTEGER NOT NULL, PacketsLost INTEGER NOT NULL, Minimum INTEGER NOT NULL, Maximum INTEGER NOT NULL, Average INTEGER NOT NULL)")
        self.connection.commit()

    # Returns the last day a report was sent
    def DayOfLastReport(self):
        return self.cursor.execute("SELECT DayOfLastReport FROM Info").fetchone()[0]

    # Updates the day value of the Info table
    def UpdateDayOfLastReport(self, day):
        self.cursor.execute("UPDATE Info SET DayOfLastReport='{}'".format(day))
        self.connection.commit()

    # Adds a ping result to the DB
    def AddToResults(self, host, packetValues, speedValues):
        self.cursor.execute("INSERT OR IGNORE INTO Results VALUES(NULL, '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(host, packetValues[0], packetValues[1], packetValues[2], speedValues[0], speedValues[1], speedValues[2]))
        self.connection.commit()

    # Returns the Results table as one
    def GetResults(self):
        return self.cursor.execute("SELECT * FROM Results").fetchall()

    # Deletes results table
    def DeleteResults(self):
        self.cursor.execute("DROP TABLE IF EXISTS Results")
        self.connection.commit()

    # Prints the Results table, used for testing
    def PrintResultsTable(self):
        for row in self.cursor.execute("SELECT * FROM Results"):
            print(row)