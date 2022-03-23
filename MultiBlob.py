import image, sensor, ustruct, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking

uart = pyb.UART(3)
uart.init(115200, bits=8, parity=None)

# Packets to Send
blob_packet = '<fff'

# Setup RED LED for easier debugging
red_led   = pyb.LED(1)
green_led = pyb.LED(2)
blue_led  = pyb.LED(3)

while True:
    green_led.on()
    img = sensor.snapshot()

    threshold = (63, 79, -128, -16, 23, 127) # Default Threshold
    blobs = img.find_blobs([threshold], pixels_threshold=5, area_threshold=20)

    if blobs:
        blob_sort = sorted(blobs, key = lambda b: b.pixels(), reverse=True)
        blob_largest = blob_sort[:3]
        blobs_found = len(blob_largest)

        msg = "**".encode()
        uart.write(msg)
        for i in range(3):
            if i < blobs_found:
                b = blob_largest[i]
                a = float(b.area())
                x_cnt = float(b.cx())
                y_cnt = float(b.cy())
            else:
                a = 0.0
                x_cnt = 0.0
                y_cnt = 0.0

            # Send the blob area and centroids over UART
            b = ustruct.pack(blob_packet, a, x_cnt, y_cnt)
            uart.write(b)

    green_led.off()