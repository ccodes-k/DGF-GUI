# using serial port to get GPS data
import serial

def nmea_to_decimal_degrees(coord_str, direction):
    if coord_str:
        if '.' in coord_str:
            decimal_point_index = coord_str.index('.')
            degrees = float(coord_str[:decimal_point_index - 2])
            minutes = float(coord_str[decimal_point_index - 2:])
        
            decimal_degrees = degrees + (minutes / 60.0)
        
            if direction == 'S' or direction == 'W':
                decimal_degrees = -decimal_degrees
        
            return decimal_degrees
    
    return None

class SerialDataWriter:
    def __init__(self, port='COM3', baudrate=115200, timeout=0.5):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def read_and_write_to_file(self, filename='./assets/ReadFiles/LLD.txt'):
        with open(filename, 'w') as f:
            while True:
                line = self.ser.readline().decode('utf-8').strip()
                if line.startswith('$GNRMC'):
                    data = line.split(',')
                    if len(data) >= 8:
                        Lat = data[3]
                        Lat_dir = data[4]
                        Long = data[5]
                        Long_dir = data[6]
                        Deg = data[8]
                        
                        latitude = nmea_to_decimal_degrees(Lat, Lat_dir)
                        longitude = nmea_to_decimal_degrees(Long, Long_dir)
                        
                        if latitude is not None and longitude is not None:
                            f.write(f'{latitude}\n{longitude}\n{Deg}')
                            f.flush()
                            break

# Example usage:
# if __name__ == '__main__':
#     data_writer = SerialDataWriter(port='COM3', baudrate=115200)
#     data_writer.read_and_write_to_file()