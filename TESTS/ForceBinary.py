# Untitled - By: prenk - Fri Jan 21 2022

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

W = sensor.width()
H = sensor.height()


while(True):
    clock.tick()
    img = sensor.snapshot()
    stats = img.get_statistics()
    m = stats.mean()
    for i in range(W):
        for j in range(H):
            l = img.get_pixel(i,j)
            if l > m:
                img.set_pixel(i,j,255)
            else:
                img.set_pixel(i,j,0)
    print(clock.fps())

