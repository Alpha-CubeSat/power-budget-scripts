# Power Budget Scripts

Data collection and plotting tools for power budget tests. These can be repurposed to a general serial monitor scraper and plotting tool.

To see which serial ports are active, run `python get_ports.py` in the terminal.

To run the logging script in `serial_logger.py`:
1. Check that the serial ports for the Arduino Leonardo and the Teensy are properly set (lines 9 and 13, respectively).
2. Make sure that the power monitoring script on the Arduino Leonardo and the flight software on the Teensy are both uploaded and running.
3. Make sure there are no serial monitors open for the Arduino Leonardo or the Teensy.
4. Run `python serial_logger.py` in the terminal.

To create a plot for a test run, create a new `html` file from `template.html` in the `graphs` directory and complete all the "FILL IN..." prompts.

To see the plots:
1. Run `cd graphs` in the terminal.
2. Run `python -m http.server 8000` in the terminal.
3. Go to http://localhost:8000 in browser.
4. Select the test run you wish to view.
