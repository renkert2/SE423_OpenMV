# Untitled - By: prenk - Fri Jan 21 2022

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

x = sensor.width()//2
y = sensor.height()//2
print(f"X: {x}")
print(f"Y: {y}")

time.sleep(3)

while(True):
    clock.tick()
    img = sensor.snapshot()
    tup = img.get_pixel(x,y,rgbtuple=True)
    # Print the value of the image center
    img.draw_cross(x,y, size=10, thickness=2)


    print(tup)
    #print(f"The center color is {tup}")
