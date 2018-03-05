import subprocess, platform, sys
from ConfigManager import ConfigManager
from DBManager import DBManager
from Report import Report

class Pinger:

    def __init__(self):
        self.config = ConfigManager()
        self.db = DBManager()
        self.report = Report(self.config, self.db)

        if self.config.hostsToPing[0] is '' and len(self.config.hostsToPing) is 1:
            print("No hosts to ping")
            sys.exit()

        # Perform pings
        for host in self.config.hostsToPing:
           self.ping(host)

        # self.db.PrintResultsTable() # Used for testing
        self.report.SendReport() # Send report if needed

    # Ping and parse results
    def ping(self, host):
        # Create command based on platform
        pingStr = "-n 3" if platform.system().lower() == "windows" else "-c 3"
        args = "ping  {} {}".format(pingStr, host)
        need_sh = False if platform.system().lower() == "windows" else True

        # Run command and parse results
        print("Pinging {}".format(host))
        process = subprocess.Popen(args, shell=need_sh, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        packetValues = [0, 0, 0]
        speedValues = [0, 0, 0]
        while True:
            try:
                line = process.stdout.readline().decode()
            except Exception as e:
                print("Error decoding line: {}".format(e))
                continue

            if line == '' and process.poll() is not None:
                break

            # Parse result line by line - should probably use regex
            if "Sent" in line:
                equalPositions = [pos for pos, char in enumerate(line) if char == '=']
                commaPositions = [pos for pos, char in enumerate(line) if char == ',']
                for i in range(len(equalPositions)):
                    packetValues[i] = line[equalPositions[i] + 1:commaPositions[i]].strip()

                    if "(" in packetValues[i]:  # There got to be a better way
                        packetValues[i] = packetValues[i].split(' ')[0]

            if "Minimum" in line:
                line = line.strip()
                line += ","  # Make this better
                equalPositions = [pos for pos, char in enumerate(line) if char == '=']
                commaPositions = [pos for pos, char in enumerate(line) if char == ',']
                for i in range(len(equalPositions)):
                    speedValues[i] = line[equalPositions[i] + 1:commaPositions[i] - 2].strip()

        self.db.AddToResults(host, packetValues, speedValues)


if __name__ == "__main__":
    Pinger()