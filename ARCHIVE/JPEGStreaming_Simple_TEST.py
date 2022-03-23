# Image Transfer - As The Remote Device
#
# This script is meant to talk to the "image_transfer_jpg_as_the_controller_device.py" on your computer.
#
# This script shows off how to transfer the frame buffer to your computer as a jpeg image.

import image, omv, rpc, sensor, struct, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking


omv.disable_fb(True)
interface = rpc.rpc_usb_vcp_slave()

# Setup RED LED for easier debugging
red_led   = pyb.LED(1)
green_led = pyb.LED(2)
blue_led  = pyb.LED(3)

def snapshot(data):
    green_led.on()

    img = sensor.snapshot()
    # x = sensor.width() // 2
    # y = sensor.height() // 2
    # img.draw_circle(x,y,100,thickness=10)

    threshold = (52, 100, -36, 10, -128, 127) # Default Threshold
    #blobs = img.find_blobs(threshold, pixels_threshold=5, area_threshold=20)
    blobs = img.find_blobs([threshold]) # Threshold must be an iterable!

    if not blobs: return bytes() # No detections.
    
    for b in blobs:
        img.draw_rectangle(b.rect(), color = (255, 0, 0))
        img.draw_cross(b.cx(), b.cy(), color = (0, 255, 0))

    # if blobs:
    #     # Sort the blobs by their area
    #     blob_areas = [b.area() for b in blobs] # Area of each blob
    #     sorted_indices = sorted(range(len(blob_areas)), key=(lambda i: blob_areas[i]), reverse=True) # Indices associated with each blob, sorted by area

    #     # Get the three largest blobs
    #     sorted_indices = sorted_indices[:3]

    #     for i in sorted_indices:
    #         blob = blobs[sorted_indices[i]]

    #         img.draw_rectangle(blob.rect())
    #         img.draw_cross(blob.cx(), blob.cy())
    
    img.compress(quality=50) # Compress in place

    green_led.off()
    return bytes()

def jpeg_image_size(data):
    blue_led.on()
    img = sensor.get_fb()
    blue_led.off()
    return struct.pack("<I", img.size())
    
def jpeg_image_read_cb():
    red_led.on()
    interface.put_bytes(sensor.get_fb().bytearray(), 5000) # timeout
    red_led.off()

def jpeg_image_read(data):
    interface.schedule_callback(jpeg_image_read_cb)
    return bytes()

# Register call backs.

interface.register_callback(snapshot)
interface.register_callback(jpeg_image_size)
interface.register_callback(jpeg_image_read)

interface.loop(recv_timeout=5000, send_timeout=5000)