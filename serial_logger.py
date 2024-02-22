import serial
import csv
import keyboard
import time


# Change to match the desired serial ports
try:
    leonardoSerial = serial.Serial(port = 'COM8', baudrate=115200, timeout=1)
except: 
    leonardoSerial = None
try:
    teensySerial = serial.Serial(port = 'COM6', baudrate=9600, timeout=1)
except: 
    teensySerial = None


def read_monitors(teensyFileName, leonardoFileName, combinedFileName):

    # Create log files
    teensyFile = open(teensyFileName, "w")
    leonardoFile = open(leonardoFileName, "w")

    # Program stop flag
    keyPressed = False

    with open(combinedFileName, "w", newline='') as csvFile:
        # Create a CSV writer object  
        csvWriter = csv.writer(csvFile)  

        # Write the CSV rows
        csvWriter.writerow([
            "Time",
            "Current to/from Batteries (mA)",
            "Current to Satellite (mA)",
            "Current from Solar Panel (mA)",
            "Battery Voltage (TB)",
            "Satellite Voltage",
            "Solar Panel Voltage",
            "Power to/from Batteries (mW)",
            "Power consumbed by Sattelite (mW)",
            "Power from Solar Panel (mW)",
            "Current Mission Mode",
            "ACS Mode",
            "ACS On/Off",
            "Battery Voltage (Onboard)",
            "IMU On/Off",
            "Optical Sensor On/Off"
            "Solar Current (Onboard)",
            "RockBLOCK Sleeping/Awake",
            "RockBLOCK Mode",
        ])

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
        opticalSensorPowered = 0
        solarCurrentOB = 0
        rockblockSleeping = 0
        rockblockMode = 0

        while not keyPressed:

            # Flush serial lines
            teensySerial.reset_input_buffer()
            leonardoSerial.reset_input_buffer()

            # Wait until start of Teensy loop
            if (teensySerial is not None):
                while ("START LOOP" not in teensySerial.readline().decode()):
                    pass
            
            # Wait until start of Leonardo loop
            if (leonardoSerial is not None):
                # Eat the next loop if there are no teensy values to be read
                while ("Time" not in leonardoSerial.readline().decode()):
                    pass

            # Process flight software data from Teensy serial line
            if ((teensySerial is not None) and (teensySerial.inWaiting() > 0)):
                # Write timestamp to logs
                timestamp = round(time.time() * 1000)
                teensyFile.write("--------------------END LOOP--------------------\n")
                teensyFile.write("Timestamp: " + str(timestamp) + "\n")
                leonardoFile.write("Timestamp: " + str(timestamp) + "\n")
                
                # Process lines from the Teensy serial line for one loop
                teensyLine = teensySerial.readline().strip().decode()
                while ("START LOOP" not in teensyLine):
                    # Write the line to the Teensy text log
                    teensyFile.write(teensyLine) # new line is included already
                    # print(teensyLine)

                    # Parse desired values to place in CSV
                    lineSplitColon = teensyLine.split(":")

                    if len(lineSplitColon) == 2:
                        label, value = lineSplitColon
                        value = value.strip()

                        if label == "Current Mission Mode":
                            currentMissionMode = value
                        elif label == "ACS Mode":
                            ACSMode = value
                        elif label == "Battery Voltage":
                            batteryVoltageOB = value.split(" ")[0]
                        elif label == "RockBLOCK Mode":
                            rockblockMode = value
                    else:
                        lineSplitSpace = teensyLine.split(" ")

                        if (len(lineSplitSpace) == 2):
                            label, value = lineSplitSpace
                            value = value.strip()

                            if label == "ACS":
                                ACSOnOff = value
                            elif label == "IMU":
                                if value == "powered" or value == "UNpowered":
                                    IMUPowered = value
                            elif label == "RockBLOCK":
                                rockblockSleeping = value

                    # Read the next line
                    teensyLine = teensySerial.readline().decode()

            # Process power data from Leonardo serial line
            if ((leonardoSerial is not None) and (leonardoSerial.inWaiting() > 0)):

                # Process lines from the Leonardo line for one loop
                leonardoLine = leonardoSerial.readline().strip().decode()
                while ("Time" not in leonardoLine):

                    # Write the line to the Leonardo text log
                    leonardoFile.write(leonardoLine)
                    # print(leonardoLine)

                    # Parse desired values to place in CSV
                    lineSplit = leonardoLine.split(":")
                    
                    if len(lineSplit) == 2:
                        label, value = lineSplit
                        value = value.strip()

                        if label == "Current to/from Batteries":
                            currentBatteries = value.split(" ")[0]
                        elif label == "Current to Satellite":
                            currentSatellite = value.split(" ")[0]
                        elif label == "Current from Solar Panel":
                            currentSolarPanel = value.split(" ")[0]
                        elif label == "Battery Voltage":
                            batteryVoltageTB = value.split(" ")[0]
                        elif label == "Satellite Voltage (from Charge Controller)":
                            satelliteVoltage = value.split(" ")[0]
                        elif label == "Solar Panel Voltage":
                            solarPanelVoltage = value.split(" ")[0]
                        elif label == "Power to/from Batteries":
                            powerBatteries = value.split(" ")[0]
                        elif label == "Power consumed by Satellite":
                            powerSatellites = value.split(" ")[0]
                        elif label == "Power from Solar Panel":
                            powerSolarPanel = value.split(" ")[0]

                    # Read the next line
                    leonardoLine = leonardoSerial.readline().decode()

            # Write all the values to the CSV file
            csvWriter.writerow([
                timestamp,
                currentBatteries,
                currentSatellite,
                currentSolarPanel,
                batteryVoltageTB,
                satelliteVoltage,
                solarPanelVoltage,
                powerBatteries,
                powerSatellites,
                powerSolarPanel,
                currentMissionMode,
                ACSMode,
                ACSOnOff,
                batteryVoltageOB,
                IMUPowered,
                rockblockSleeping,
                rockblockMode,
            ])

            # Shut down program if "a" key is pressed
            if keyboard.is_pressed("a"):
                keyPressed = True
                teensyFile.close()
                leonardoFile.close()


def main():
    if leonardoSerial == None:
        print("No Leonardo serial line detected!")
    if teensySerial == None:
        print("No Teensy serial line detected!")
    else:
        testName = input("Enter name of this test run: ")

        teensyFileName = "logs/" + testName + "_teensy.txt"
        leonardoFileName = "logs/" + testName + "_leonardo.txt"
        combinedFileName = "logs/" + testName + "_combined.csv"

        print("Files will be saved to the 'power-budget-scripts/logs' directory")
        print("Hold 'a' to stop logging")

        read_monitors(teensyFileName, leonardoFileName, combinedFileName)

        print("Program stopped!")

if __name__ == "__main__":
    main()