# Multi Color Blob Tracking
#
# This example shows off multi color blob tracking using the OpenMV Cam.

import sensor, image, time, math
import pyb, ustruct

# Define color thresholds:
thresholds = {} # Make a dictionary to store the threshold values

# The threshold tuples define minimum and maximum values for LAB colors.
# The order is:
# - (L Min, L Max, A Min, A Max, B Min, B Max)

thresholds["RED"] = (30, 100, 15, 127, 15, 127) # Generic red Threshold
thresholds["GREEN"] = (30, 100, -64, -8, -32, 32) # Generic green threshold
thresholds["BLUE"] = (0, 30, 0, 64, -128, 0) # Generic blue threshold
thresholds["ORANGE"] = (17, 30, 5, 62, 14, 42) # Custom Orange Threshold

# Make a list of thresholds that we want the camera to look for:
threshold = [thresholds["RED"]] # Default Threshold

# Setup RED LED for easier debugging
red_led   = pyb.LED(1)
green_led = pyb.LED(2)
blue_led  = pyb.LED(3)

# SETUP Communication over virtual comm port
vcp = pyb.USB_VCP()
vcp.init()

# Packets to Send
blob_packet = 'fff'
num_blobs_packet = 'B'

# Packets to Receive
threshold_packet = 'BBBBBB'
threshold_packet_size = ustruct.calcsize(threshold_packet)
num_thresholds_packet = 'B'
num_thresholds_packet_size = ustruct.calcsize(num_thresholds_packet)


# You may pass up to 16 thresholds above. However, it's not really possible to segment any
# scene with 16 thresholds before color thresholds start to overlap heavily.

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. Setting merge=True would merge the blobs.

while(True):
    red_led.on() # Waiting for Data
    cmd_data = vcp.recv(1)

    red_led.off() # Received Data

    if cmd_data == b"S":
        green_led.on() # Received Send command

        img = sensor.snapshot()

        blobs = img.find_blobs(threshold, pixels_threshold=5, area_threshold=20)

        # Send the number of blobs found
        num_blobs = len(blobs)
        vcp.send(ustruct.pack(num_blobs_packet, num_blobs))

        if blobs:
            # Sort the blobs by their area
            blob_areas = [b.area() for b in blobs] # Area of each blob
            sorted_indices = sorted(range(len(blob_areas)), key=(lambda i: blob_areas[i]), reverse=True) # Indices associated with each blob, sorted by area

            # Get the three largest blobs
            sorted_indices = sorted_indices[:3]


            for i in sorted_indices:
                blob = blobs[sorted_indices[i]]

                #img.draw_rectangle(blob.rect())
                #img.draw_cross(blob.cx(), blob.cy())

                a = blob.area()
                x_cnt = blob.cx()
                y_cnt = blob.cy()

                # Send the blob area and centroids over USB
                b = ustruct.pack(blob_packet, a, x_cnt, y_cnt)
                # b = f"A: {a}, X: {x_cnt}, Y: {y_cnt}\n".encode('UTF-8')
                vcp.send(b)
        green_led.off()
    elif cmd_data == b'T':
        blue_led.on() # Received "THRESHOLD" command

        num_thresholds_data = vcp.recv(num_thresholds_packet_size)
        num_thresholds = ustruct.unpack(num_thresholds_packet, num_thresholds_data)
        num_thresholds = num_thresholds[0] # Convert from tuple

        threshold = []
        for i in range(num_thresholds):
            green_led.on()
            time.sleep(0.25)

            threshold_data = vcp.recv(threshold_packet_size)  # receive Threshold Value
            threshold.append(ustruct.unpack(threshold_packet, threshold_data))

            green_led.off()
            time.sleep(0.25)

        time.sleep(1)
        blue_led.off()
    elif cmd_data == b'I':
        # Capture Image Command
        img = sensor.snapshot().compress(quality=100)
        vcp.send(ustruct.pack("<L", img.size()))
        vcp.send(img)

