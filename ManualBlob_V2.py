# Untitled - By: prenk - Fri Jan 21 2022

import sensor, image, time
import pyb, ustruct


(30, 100, 15, 127, 15, 127)

# Define Threshold for LAB Channels
L_min = 30
L_max = 100

A_min = 15
A_max = 127

B_min = 15
B_max = 127

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking

# Make clock object to measure frames per second
clock = time.clock()

# Get the width and height of the image in pixels
W = sensor.width()
H = sensor.height()

while(True):
    clock.tick()
    img = sensor.snapshot()

    row_cnt = 0 # Accumulate along rows
    col_cnt = 0 # Accumulate along cols
    pixel_cnt = 0 # Number of pixels in threshold

    for i in range(W):
        for j in range(H):
            pixel_rgb = img.get_pixel(i,j, rgb_tuple=True)
            pixel_lab = image.rgb_to_lab(pixel_rgb)

            # Assign L,A,B channels in pixel_lab array to separate variables
            pixel_l = pixel_lab[0]
            pixel_a = pixel_lab[1]
            pixel_b = pixel_lab[2]

            # Check whether the pixel is in the threshold
            if (L_min < pixel_l < L_max) and (A_min < pixel_a < A_max) and (B_min < pixel_b < B_max): # All channels are in their thresholds

                # COMPLETE: Incrementing Counters
                #---------

                col_cnt += i # Increment the counters
                row_cnt += j
                pixel_cnt += 1

                #---------

                # Color the blob black
                img.set_pixel(i,j,(0,0,0))

    if pixel_cnt:
        # Calculate the centeroid detected pixels:
        # COMPLETE: Calculate Centroid
        #---------

        x_cnt = col_cnt // pixel_cnt
        y_cnt = row_cnt // pixel_cnt

        #---------

        # Draw a cross at the centroid
        img.draw_cross(x_cnt, y_cnt)

        # Print centroid to the terminal
        print(f"Centroid at: {x_cnt}, {y_cnt}")
    else:
        x_cnt = 0
        y_cnt = 0
        print("Blob not found")

    # Send centroid over UART
    # TODO
    # b = ustruct.pack('ff', x_cnt, y_cnt)
    # b = f"{x_cnt}, {y_cnt}\n".encode('UTF-8')
    # vcp.send(b)

    # Print FPS to the serial terminal
    print("FPS: ", clock.fps())

