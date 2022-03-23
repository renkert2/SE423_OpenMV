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

omv.disable_fb(True)
interface = rpc.rpc_usb_vcp_slave()

def jpeg_image_size(data):
    img = sensor.snapshot().compress(quality=90)
    return struct.pack("<I", img.size())

def jpeg_image_read_cb():
    interface.put_bytes(sensor.get_fb().bytearray(), 5000) # timeout

def jpeg_image_read(data):
    interface.schedule_callback(jpeg_image_read_cb)
    return bytes()

# Register call backs.

interface.register_callback(jpeg_image_size)
interface.register_callback(jpeg_image_read)


interface.loop()