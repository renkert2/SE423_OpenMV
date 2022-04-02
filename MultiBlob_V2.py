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
threshold = (30, 100, 15, 127, 15, 127) # Default Threshold

# Setup RED LED for easier debugging
red_led   = pyb.LED(1)
green_led = pyb.LED(2)
blue_led  = pyb.LED(3)

# SETUP Communication over virtual comm port
# vcp = pyb.USB_VCP()
# vcp.init()
# SETUP Communication over UART3
uart = pyb.UART(3)
uart.init(115200, bits=8, parity=None)


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
    red_led.on() # Running Main Loop
    
    img = sensor.snapshot()

    blobs = img.find_blobs(threshold, pixels_threshold=5, area_threshold=20)

    # Send the number of blobs found
    num_blobs = len(blobs)
    
    # vcp.send(ustruct.pack(num_blobs_packet, num_blobs))
    blue_led.on()
    uart.write(ustruct.pack(num_blobs_packet, num_blobs))
    blue_led.off()

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
            
            green_led.on()
            #vcp.send(b)
            uart.write(b)
            green_led.off()

