import datetime, smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Report:

    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.today = datetime.date.today().day

    # Compose and send email if required
    def SendReport(self):
        # Need to send report?
        if self.db.DayOfLastReport() is self.today:
            print("Don't need to send report")
            return

        # Compose email
        msg = MIMEMultipart()
        msg['From'] = self.config.fromAddress
        msg['To'] = self.config.toAddress
        msg['Subject'] = "Daily ping report"
        msg.attach(MIMEText(self.composeMessage(), 'plain'))

        try:
            # Send email
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login(msg['From'], self.config.fromPassword)
            server.sendmail(msg['From'], msg['To'], msg.as_string())

            # Update db and drop table ready for new day of week
            self.db.UpdateDayOfLastReport(self.today)
            self.db.DeleteResults()
        except Exception as e:
            print("Error sending email: {}".format(e))
            sys.exit(1)

        server.quit()

    # Get values from DB and calculate averages/packet loss
    def composeMessage(self):
        packetsSent = {}
        packetsReceived = {}
        packetsLost = {}
        averageSpeeds = {}
        numberOfAverages = {}
        endMessage = ""

        for result in self.db.GetResults():

            # Packets sent
            if not result[1] in packetsSent:
                packetsSent[result[1]] = 0
            packetsSent[result[1]] += result[2]

            # Packets received
            if not result[1] in packetsReceived:
                packetsReceived[result[1]] = 0
            packetsReceived[result[1]] += result[3]

            # Packets lost
            if not result[1] in packetsLost:
                packetsLost[result[1]] = 0
            packetsLost[result[1]] += result[4]

            # Average
            if not result[1] in averageSpeeds:
                numberOfAverages[result[1]] = 0
                averageSpeeds[result[1]] = 0

            numberOfAverages[result[1]] += 1
            averageSpeeds[result[1]] += result[7]

        for key, value in packetsSent.items():
            if packetsLost[key] is not 0:
                lostPercentage = packetsLost[key] / packetsSent[key] * 100
            else:
                lostPercentage = 0

            if numberOfAverages[key] is not 0 and averageSpeeds[key] is not 0:
                averageSpeed = (int)(averageSpeeds[key] / numberOfAverages[key])
            else:
                averageSpeed = 0

            endMessage += "{} - Sent: {}, Received: {}, Lost: {} ({}% lost), Average speed: {}ms\r\n".format(key, packetsSent[key], packetsReceived[key], packetsLost[key], lostPercentage, averageSpeed)

        return endMessage



