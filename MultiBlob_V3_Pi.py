# Remote Control - As The Controller Device
#
# This script remotely controls an OpenMV Cam using the RPC library.
#
# This script is meant to talk to the "popular_features_as_the_remote_device.py" on the OpenMV Cam.

import io, pygame, rpc, serial, serial.tools.list_ports, struct, sys
import time

# Fix Python 2.x.
try: input = raw_input
except NameError: pass

# Setup Interface
interface = rpc.rpc_usb_vcp_master(port="/dev/ttyACM0")
print("Connected")

# Setup Screen
pygame.init()
screen_w = 640
screen_h = 480
try:
    screen = pygame.display.set_mode((screen_w, screen_h), flags=pygame.RESIZABLE)
except TypeError:
    screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Frame Buffer")
clock = pygame.time.Clock()

def find_blobs():
    result = interface.call("find_blobs")

def get_image_size():
    result = interface.call("jpeg_image_size")
    print(result)
    if result:
        size = struct.unpack("<I", result)[0]
    else:
        size=None
    return size

def get_frame_buffer():
    size = get_image_size()
    img = bytearray(size)
    # Before starting the cut through data transfer we need to sync both the master and the
    # slave device. On return both devices are in sync.
    result = interface.call("jpeg_image_read")
    if result:
        interface.get_bytes(img, 5000) # timeout
        return img
    else:
        return None

def display_image():
    sys.stdout.flush()
    img = get_frame_buffer()
    if img:
        try:
            screen.blit(pygame.transform.scale(pygame.image.load(io.BytesIO(img), "jpg"), (screen_w, screen_h)), (0, 0))
            pygame.display.update()
            clock.tick()
        except pygame.error: pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

while(True):
    time.sleep(1)
    print(get_image_size())