import struct
import serial
import time

port = '/dev/ttyACM0'
omv = serial.Serial(port, baudrate=115200)

### Preset Color Thresholds ###
# The threshold tuples define minimum and maximum values for LAB colors.
# The order is:
# - (L Min, L Max, A Min, A Max, B Min, B Max)

thresholds = {} # Make a dictionary to store the threshold values
thresholds["RED"] = (30, 100, 15, 127, 15, 127) # Generic red Threshold
thresholds["GREEN"] = (30, 100, -64, -8, -32, 32) # Generic green threshold
thresholds["BLUE"] = (0, 30, 0, 64, -128, 0) # Generic blue threshold

thresholds["GOLF_REDORANGE"] = (0, 100, 22, 127, 31, 127)
thresholds["GOLF_PINK"] = (0, 100, 27, 127, -128, 15)
thresholds["GOLF_TEAL"] = (0, 100, -34, -21, -17, 7)
thresholds["GOLF_BLUE"] = (0, 100, -128, 127, -128, -25)

### Packets to Send ###
threshold_packet = 'BBBBBB'
num_thresholds_packet = 'B'

### Packets to Receive ###
num_blobs_packet = 'B'
num_blobs_packet_size = struct.calcsize(num_blobs_packet) # Size of the packet containing an unsigned short with the number of blobs

blob_packet = 'fff' # Three floating-point values: Blob Area, Blob X Centroid, Blob Y Centroid
blob_packet_size = struct.calcsize(blob_packet)

### Initialization ###

# Set the thresholds we want the OMV cam to look for
omv.write(b'T') # enter Set Threshold mode

find_thresholds = [thresholds["GOLF_REDORANGE"]] # Look for both RED and ORANGE
num_thresholds_data = struct.pack(num_thresholds_packet, len(find_thresholds))
omv.write(num_thresholds_data) # Send the number of thresholds
for threshold in find_thresholds:
    threshold_data = struct.pack(threshold_packet, *threshold)
    omv.write(threshold_data) # Send each threshold

time.sleep(3)

while True:
    # Ask for blob data
    omv.write(b'S')

    # Receive the number of blobs
    num_blobs = struct.unpack(num_blobs_packet, omv.read(size=num_blobs_packet_size))
    num_blobs = num_blobs[0]
    print(f"Received {num_blobs} Blobs")

    blob_data = []
    for i in range(num_blobs):
        b = omv.read(size=blob_packet_size)
        data = struct.unpack(blob_packet, b)
        blob_data.append(data)
    
    print("Received Blobs: ")
    for data in blob_data:
        print(f'A: {data[0]}, C_x: {data[1]}, C_y: {data[2]}')
    print()

    time.sleep(2)