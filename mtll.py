#!/usr/bin/env python3
import math
import re
import time
import time

# Function to write coordinates to lat_long.txt
def write_coordinates(latitude, longitude):
    with open('./assets/ReadFiles/RLL.txt', 'w') as file:
        file.write(f'{latitude} {longitude}')
r_earth = 6378137  # Earth radius

# original coordinate
# latitude = 1.2930760216666668
# longitude = 103.75099283666667

latitude = 1.2930760216666668
longitude = 103.75099283666667

theta = 170
# theta = 309.4

#Offset in meters
tx = 0
ty = 0

with open('./assets/ReadFiles/CameraTrajectory1.txt', 'r') as f:
    for line in f:
        # Regex is corrected to match the decimal values only
        list_line = re.findall(r"[-+]?\d*\.\d+|\d+", line)

        # Error condition handled where the values are not found
        if len(list_line) < 2:
            continue

        # Indexes are corrected below
        tx = (float(list_line[1]) * -1.0)  # Appends second column
        ty = (float(list_line[2]) * -1.0)  # Appends third column

        coord_x = tx * math.cos(math.radians(theta)) - ty * math.sin(math.radians(theta))
        coord_y = tx * math.sin(math.radians(theta)) - ty * math.cos(math.radians(theta))

        new_latitude = (latitude + (coord_x/ r_earth) * (180 / math.pi))
        new_longitude = (longitude + (coord_y / r_earth) * (180 / math.pi) / math.cos(latitude * math.pi / 180))

        # Write the updated coordinates to lat_long.txt
        write_coordinates(new_latitude, new_longitude)
        # print(tx, ty)
        # print(f'Coordinates updated: {new_latitude}, {new_longitude}')

        time.sleep(0.1)


