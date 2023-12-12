import serial
import csv
import keyboard
import time


# Change to match the desired serial ports
try:
    leonardoSerial = serial.Serial(port = '/dev/ttyACM1', baudrate=115200, timeout=1)
except: 
    leonardoSerial = None
try:
    teensySerial = serial.Serial(port = '/dev/ttyACM2', baudrate=9600, timeout=1)
except: 
    teensySerial = None

def read_loop(teensyFileName, leonardoFileName, combinedFileName):

    teensyFile = open(teensyFileName, "w")
    leonardoFile = open(leonardoFileName, "w")

    # Eat all values until the beginning of a teensy loop
    if ((teensySerial is not None) and (teensySerial.inWaiting() > 0)):
        while (teensySerial.readline().decode() != "--------------------START LOOP--------------------"):
            pass

    keyPressed = False

    with open(combinedFileName, "w") as csvFile:
        # Create a CSV writer object  
        csvWriter = csv.writer(csvFile)  

        # Writing the CSV
        csvWriter.writerow([
            "Time",
            "Current to/from Batteries",
            "Current to Satellite",
            "Current from Solar Panel",
            "Battery Voltage (TB)",
            "Satellite Voltage",
            "Solar Panel Voltage",
            "Power to/from Batteries",
            "Power consumbed by Sattelite",
            "Power from Solar Panel",
            "Current Mission Mode",
            "ACS Mode",
            "ACS On/Off",
            "Battery Voltage (Onboard)",
            "IMU On/Off",
            "RockBLOCK Sleeping/Awake",
            "RockBLOCK Mode",
        ])

        while not keyPressed:

            timestamp = round(time.time() * 1000)
            currentBatteries = 0
            currentSatellite = 0
            currentSolarPanel = 0
            batteryVoltageTB = 0
            satelliteVoltage = 0
            solarPanelVoltage = 0
            powerBatteries = 0
            powerSatellites = 0
            powerSolarPanel = 0
            currentMissionMode = 0
            ACSMode = 0
            ACSOnOff = 0
            batteryVoltageOB = 0
            IMUPowered = 0
            rockblockSleeping = 0
            rockblockMode = 0

            teensyFile.write("Timestamp: " + str(timestamp) + "\n")
            leonardoFile.write("Timestamp: " + str(timestamp) + "\n")

            if ((teensySerial is not None) and (teensySerial.inWaiting() > 0)):
                # There are teensy characters to read

                timestamp = round(time.time() * 1000)       
                teensyFile.write("Timestamp: " + str(timestamp) + "\n")
                leonardoFile.write("Timestamp: " + str(timestamp) + "\n")

                teensyLine = teensySerial.readline().decode()
                
                while (teensyLine != "--------------------START LOOP--------------------"):
                    teensyFile.write(teensyLine + "\n")
                    lineSplit = teensyLine.split(":")

                    if len(lineSplit) == 2:
                        label, value = lineSplit

                        if label == "Current Mission Mode":
                            currentMissionMode = value.strip()
                        elif label == "ACS Mode":
                            ACSMode = value.strip()
                        elif label == "Battery Voltage":
                            batteryVoltageOB = value.strip().split(" ")[0]
                        elif label == "RockBLOCK Mode":
                            rockblockMode = value.strip()
                    else:
                        label, value = teensyLine.split(" ")

                        if label == "ACS":
                            ACSOnOff = value
                        elif label == "IMU":
                            IMUPowered = value.strip()
                        elif label == "RockBLOCK":
                            rockblockSleeping = value.strip()

                    teensyLine = teensySerial.readLine().decode()

                if ((leonardoSerial is not None) and (leonardoSerial.inWaiting() > 0)):
                    leonardoLine = leonardoSerial.readline().decode()
                    while (leonardoSerial.readline().decode()[0:5] != "Time:"):
                        leonardoFile.write(leonardoLine + "\n")
                        lineSplit = leonardoLine.split(":")
                        
                        if len(lineSplit) == 2:
                            label, value = lineSplit

                            if label == "Current to/from Batteries":
                                currentBatteries = value.strip().split(" ")[0]
                            elif label == "Current to Satellite":
                                currentSatellite = value.strip().split(" ")[0]
                            elif label == "Current from Solar Panel":
                                currentSolarPanel = value.strip().split(" ")[0]
                            elif label == "Battery Voltage":
                                batteryVoltageTB = value.strip().split(" ")[0]
                            elif label == "Satellite Voltage (from Charge Controller)":
                                satelliteVoltage = value.strip().split(" ")[0]
                            elif label == "Solar Panel Voltage":
                                solarPanelVoltage = value.strip().split(" ")[0]
                            elif label == "Power to/from Batteries":
                                powerBatteries = value.strip().split(" ")[0]
                            elif label == "Power consumed by Satellite":
                                powerSatellites = value.strip().split(" ")[0]
                            elif label == "Power from Solar Panel":
                                powerSolarPanel = value.strip().split(" ")[0]
                        else:
                            pass

                        leonardoLine = leonardoSerial.readline().decode() 

            elif ((leonardoSerial is not None) and (leonardoSerial.inWaiting() > 0)):
                # Eat the next loop if there are no teensy values to be read
                while (leonardoSerial.readline().decode()[0:5] != "Time:"):
                    pass

            if keyboard.is_pressed("a"):  # check if the A key is pressed
                keyPressed = True
                teensyFile.close()
                leonardoFile.close()


def main():
    testName = input("Enter name of this test run: ")

    teensyFileName = "logs/" + testName + "_teensy.txt"
    leonardoFileName = "logs/" + testName + "_leonardo.txt"
    combinedFileName = "logs/" + testName + "_combined.csv"

    print("Files will be saved to 'power-budget-scripts/logs' directory")
    print("Hold 'a' to stop logging")

    read_loop(leonardoFileName, teensyFileName, combinedFileName)

    print("Program stopped!")

if __name__ == "__main__":
    main()