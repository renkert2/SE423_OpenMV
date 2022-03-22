# Image Transfer - As The Remote Device
#
# This script is meant to talk to the "image_transfer_jpg_as_the_controller_device.py" on your computer.
#
# This script shows off how to transfer the frame buffer to your computer as a jpeg image.

import image, network, omv, rpc, sensor, struct

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking

omv.disable_fb(True)
interface = rpc.rpc_usb_vcp_slave()

# The threshold tuples define minimum and maximum values for LAB colors.
# The order is:
# - (L Min, L Max, A Min, A Max, B Min, B Max)
threshold = (30, 100, 15, 127, 15, 127) # Default Threshold

def find_blobs_cb():
    print("Finding Blobs")
    img = sensor.snapshot()    

    # x = sensor.width() // 2
    # y = sensor.height() // 2
    # img.draw_circle(x,y,100,thickness=10)

    blobs = img.find_blobs(threshold, pixels_threshold=5, area_threshold=20)

    if blobs:
        # Sort the blobs by their area
        blob_areas = [b.area() for b in blobs] # Area of each blob
        sorted_indices = sorted(range(len(blob_areas)), key=(lambda i: blob_areas[i]), reverse=True) # Indices associated with each blob, sorted by area

        # Get the three largest blobs
        sorted_indices = sorted_indices[:3]

        for i in sorted_indices:
            blob = blobs[sorted_indices[i]]

            img.draw_rectangle(blob.rect())
            img.draw_cross(blob.cx(), blob.cy())

    img.compress(quality=90) # Compress in place
    
def find_blobs(data):
    interface.schedule_callback(find_blobs_cb)
    return bytes

def jpeg_image_size(data):
    img = sensor.get_fb()
    return struct.pack("<I", img.size())

def jpeg_image_read_cb():
    interface.put_bytes(sensor.get_fb().bytearray(), 5000) # timeout

def jpeg_image_read(data):
    interface.schedule_callback(jpeg_image_read_cb)
    return bytes()

# Register call backs.
interface.register_callback(find_blobs)
interface.register_callback(jpeg_image_size)
interface.register_callback(jpeg_image_read)


interface.loop()