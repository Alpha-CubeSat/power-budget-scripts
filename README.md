# Power Budget Scripts

Tools for power budget tests.

To see which serial ports are active, run `python get_ports.py`

To run the logging script in `serial_logger.py`:
1. Check that the serial ports for the Arduino Leonardo and the Teensy are properly set (lines 9 and 13, respectively).
2. Make sure that the power monitoring script on the Arduino Leonardo and the flight software on the Teensy are both uploaded and running.
3. Make sure there are no serial monitors open for the Arduino Leonardo or the Teensy.
4. Run `python serial_logger.py`.

(We loggin)
