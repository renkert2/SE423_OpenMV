# Multi Color Blob Tracking Example
#
# This example shows off multi color blob tracking using the OpenMV Cam.

import sensor, image, time, math

# Define color thresholds:
thresholds = {} # Make a dictionary to store the threshold values

# The threshold tuples define minimum and maximum values for LAB colors.
# The order is:
# - (L Min, L Max, A Min, A Max, B Min, B Max)

thresholds["RED"] = (30, 100, 15, 127, 15, 127) # Generic red Threshold
thresholds["GREEN"] = (30, 100, -64, -8, -32, 32) # Generic green threshold
thresholds["BLUE"] = (0, 30, 0, 64, -128, 0) # Generic blue threshold

colors = {}
colors["RED"] = (255,0,0)
colors["GREEN"] = (0,255,0)
colors["BLUE"] = (0,0,255)

# Make a list of thresholds that we want the camera to look for:
find_colors = ["RED", "BLUE", "GREEN"]
threshold = [thresholds[x] for x in find_colors]

# You may pass up to 16 thresholds above. However, it's not really possible to segment any
# scene with 16 thresholds before color thresholds start to overlap heavily.

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. Setting merge=True would merge the blobs.

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs(threshold, pixels_threshold=200, area_threshold=200):
        # These values are stable all the time.
        color_code = blob.code()
        color_index = int(math.log2(color_code))
        color_mean = colors[find_colors[color_index]]
        #print("Blob Code: ", color_code, "Blob Index: ", color_index, "Blob Color: ", find_colors[color_index])

        img.draw_rectangle(blob.rect(), color=color_mean)
        img.draw_cross(blob.cx(), blob.cy(), color=color_mean)

    print("FPS: ", clock.fps())
