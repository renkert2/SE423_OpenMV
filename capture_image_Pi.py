import struct
import serial
import time
from PIL import Image
from io import BytesIO
import os

### 
# Run this script to take and save a snapshot to find the threshold values in MATLAB

port = 'COM4'
omv = serial.Serial(port, baudrate=115200)

image_size_packet = "<L"
image_size_packet_size = struct.calcsize(image_size_packet)


# Enter "IMAGE" mode
omv.write(b'I') # enter Set Threshold mode

image_size = struct.unpack(image_size_packet, omv.read(size=image_size_packet_size))[0]
image_data = omv.read(image_size)

# Process Image Data
image_data_file = BytesIO(image_data)
img = Image.open(image_data_file)

img.show()

save_path = os.path.join(os.path.dirname(__file__), "snapshot.jpeg")
img.save(save_path)

