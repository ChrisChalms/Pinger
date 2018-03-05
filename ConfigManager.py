import configparser
import os, sys

class ConfigManager:

    def __init__(self):
        self.configFile = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "config.ini"))

        # Options to be overriden by ini file
        self.hostsToPing = []
        self.fromAddress = ""
        self.fromPassword = ""
        self.toAddress = ""

        # Load config
        if os.path.isfile(self.configFile):
            config = configparser.ConfigParser()
            config.read(self.configFile)
            self.verifyIni(config)
        else:
            print("Unable to find config file")
            sys.exit(1)

        self.setIniOptions(config)

    # Override default values from ini file
    def setIniOptions(self, config):
        # Settings
        self.hostsToPing = config.get("Settings", "hostsToPing").split(',')
        for i in range(len(self.hostsToPing)):
            self.hostsToPing[i] = self.hostsToPing[i].strip()

        # Email settings
        self.fromAddress = config.get("Email", "fromAddress").strip()
        self.fromPassword = config.get("Email", "fromPassword")
        self.toAddress = config.get("Email", "toAddress").strip()

    # Make sure all the options are present
    def verifyIni(self, config):
        settings = ["hostsToPing"]
        emailSettings = ["fromAddress", "fromPassword", "toAddress"]

        for val in settings:
            if not config.has_option("Settings", val):
                print("Missing value {} in config".format(val))
                sys.exit(1)

        for val in emailSettings:
            if not config.has_option("Email", val):
                print("Missing value {} in config".format(val))
                sys.exit(1)