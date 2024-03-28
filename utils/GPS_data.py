# using serial port to get GPS data
import serial

class SerialDataWriter:
    # window: COM3  Ubuntu : /dev/ttyUSB0
    def __init__(self, port='/dev/ttyUSB0', baudrate=115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1):
        """
        Initializes the SerialDataWriter object with specified serial port settings.
        """
        self.ser = serial.Serial(port, baudrate, timeout=timeout, parity=parity, rtscts=rtscts)

    def read_and_write_to_file(self, filename='/assets/ReadFiles/LLD.txt'):
        """
        Reads latest data from the serial port and writes it to the specified file.
        :param filename: The name of the file to write the data to.
        """
        t = ""
        while True:
            # Read characters from the serial port until newline is encountered
            cc = self.ser.read().decode('utf-8')
            t += cc
            if cc == '\n':
                # Check if the received data starts with "$GNRMC"
                if t.startswith('$GNRMC'):
                    # Split the data into fields using comma separator
                    data = t.split(',')
                    # Check if there are enough fields
                    if len(data) >= 8:
                        # Extract latitude and longitude and concatenate them
                        Lat = data[3] + " " + data[4]
                        Long = data[5] + " " + data[6]
                        LL_str = str(Lat) + "\n" + str(Long) + "\n"
                        # Extract track made good in degrees True
                        Deg = data[8]
                        Deg_str = Deg
                        # Write latest latitude, longitude, and track made good to file
                        with open(filename, 'w') as f:
                            f.write(LL_str)  # Write lat and lon to file
                            f.write(Deg_str)  # Write Track made good to file
                            f.flush
                        break  # Exit the loop once data is written to file
                t = ""

# Example usage:
# Create an instance of the SerialDataWriter class
# data_writer = SerialDataWriter()

# Call the read_and_write_to_file method to read latest data from serial port and write it to file
# data_writer.read_and_write_to_file()