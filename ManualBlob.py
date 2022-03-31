# Untitled - By: prenk - Fri Jan 21 2022

import sensor, image, time
import pyb, ustruct


# Define color thresholds:
thresholds = {} # Make a dictionary to store the threshold values

# The threshold tuples define minimum and maximum values for LAB colors.
# The order is:
# - (L Min, L Max, A Min, A Max, B Min, B Max)
# 
thresholds["RED"] = (30, 100, 15, 127, 15, 127) # Generic red Threshold
thresholds["GREEN"] = (30, 100, -64, -8, -32, 32) # Generic green threshold
thresholds["BLUE"] = (0, 30, 0, 64, -128, 0) # Generic blue threshold

threshold = thresholds["RED"]; # Set the current color threshold to look for

# Instead of multiple thresholds, use
#L_min, L_max
# A_min, A_max, ... separate variables

# SETUP Communication over virtual comm port
vcp = pyb.USB_VCP()
vcp.init()

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
            #pixel_l = pixel_lab[0]
            #pixel_a = pixel_lab[1]...

            # Check whether the pixel is in the threshold
            in_threshold_flag = True
            for (k, val) in enumerate(pixel_lab):
                min = threshold[2*k]
                # TODO: 
                max = threshold[2*k + 1]

                # This 
                if val <= min or val >= max: # If any LAB value is outside the threshold
                    in_threshold_flag = False

            if in_threshold_flag: # If the pixel is within the threshold,
                # They will add this code
                # --------
                col_cnt += i # Increment the counters
                row_cnt += j
                pixel_cnt += 1
                # ---------

                # Color the blob black
                img.set_pixel(i,j,(0,0,0))

    if pixel_cnt:
        # Calculate the centeroid detected pixels:
        # they do this
        # ---------
        x_cnt = col_cnt // pixel_cnt
        y_cnt = row_cnt // pixel_cnt
        # ---------
        # Draw a cross at the centroid
        img.draw_cross(x_cnt, y_cnt)

        # Print centroid to the terminal
        # print(f"Centroid at: {x_cnt}, {y_cnt}")
    else:
        x_cnt = 0
        y_cnt = 0
        # print("Blob not found")

    # Send centroid over Virtual Comm Port
    # b = ustruct.pack('ff', x_cnt, y_cnt)
    # b = f"{x_cnt}, {y_cnt}\n".encode('UTF-8')
    # vcp.send(b)

    # Print FPS to the serial terminal
    # print("FPS: ", clock.fps())

    # Print centroid
    # print(f"Centroid: {x_cnt}, {y_cnt}") 

