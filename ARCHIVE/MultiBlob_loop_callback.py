import image, omv, rpc, sensor, ustruct, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking

omv.disable_fb(True)
interface = rpc.rpc_usb_vcp_slave()

uart = pyb.UART(3)
uart.init(115200, bits=8, parity=None)

# Packets to Send
blob_packet = '<fff'

# Setup RED LED for easier debugging
red_led   = pyb.LED(1)
green_led = pyb.LED(2)
blue_led  = pyb.LED(3)

def snapshot():
    green_led.on()
    img = sensor.snapshot()

    threshold = (63, 79, -128, -16, 23, 127) # Default Threshold
    blobs = img.find_blobs([threshold], pixels_threshold=5, area_threshold=20)

    if blobs:
        blob_sort = sorted(blobs, key = lambda b: b.pixels(), reverse=True)
        blob_largest = blob_sort[:3]

        msg = "**".encode()
        uart.write(msg)
        for b in blob_largest:
            img.draw_rectangle(b.rect(), color = (255, 0, 0))
            img.draw_cross(b.cx(), b.cy(), color = (0, 255, 0))

            a = float(b.area())
            x_cnt = float(b.cx())
            y_cnt = float(b.cy())

            # Send the blob area and centroids over UART
            b = ustruct.pack(blob_packet, a, x_cnt, y_cnt)
            uart.write(b)

        img.compress(quality=20) # Compress in place
        green_led.off()

def jpeg_image_size(data):
    blue_led.on()
    img = sensor.get_fb()
    blue_led.off()
    return ustruct.pack("<I", img.size())
    
def jpeg_image_read_cb():
    red_led.on()
    interface.put_bytes(sensor.get_fb().bytearray(), 5000) # timeout
    red_led.off()

def jpeg_image_read(data):
    interface.schedule_callback(jpeg_image_read_cb)
    return bytes()

# Register call backs.
interface.setup_loop_callback(snapshot)
interface.register_callback(jpeg_image_size)
interface.register_callback(jpeg_image_read)

interface.loop(recv_timeout=5000, send_timeout=5000)