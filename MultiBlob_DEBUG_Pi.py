# Remote Control - As The Controller Device
#
# This script remotely controls an OpenMV Cam using the RPC library.
#
# This script is meant to talk to the "popular_features_as_the_remote_device.py" on the OpenMV Cam.

import io, pygame, rpc, serial, serial.tools.list_ports, struct, sys
import time

# Setup Interface
interface = rpc.rpc_usb_vcp_master(port="/dev/ttyACM0")
print("Connected")

# Setup Screen
pygame.init()
screen_w = 480
screen_h = 800

# QVGA: 320x240
image_w = 480
image_h = int(480*(3/4))
try:
    screen = pygame.display.set_mode((screen_w, screen_h), flags=pygame.RESIZABLE)
except TypeError:
    screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Frame Buffer")
clock = pygame.time.Clock()

def snapshot():
    result = interface.call("snapshot", send_timeout=5000, recv_timeout=5000)
    if result is not None:
        try:
            result = struct.unpack('<fffffffff', result)
            print("Received Blobs:")
            for i in (0,3,6):
                print(f"A = {result[i]}, col = {result[i+1]}, row = {result[i+2]}")
        except:
            print("Failed to unpack blobs: received {result}")
    return result
    
def get_image_size():
    result = interface.call("jpeg_image_size", send_timeout=5000, recv_timeout=5000)
    if result is not None:
        size = struct.unpack("<I", result)[0]
    return size

def get_frame_buffer():
    size = get_image_size()
    img = bytearray(size)
    # Before starting the cut through data transfer we need to sync both the master and the
    # slave device. On return both devices are in sync.
    result = interface.call("jpeg_image_read", send_timeout=5000, recv_timeout=5000)
    if result is not None:
        interface.get_bytes(img, 5000) # timeout
        return img
    else:
        return None

def display_image():
    sys.stdout.flush()
    snapshot()
    img = get_frame_buffer()
    if img is not None:
        try:
            screen.blit(pygame.transform.scale(pygame.image.load(io.BytesIO(img), "jpg"), (image_w, image_h)), (0, 0))
            pygame.display.update()
            clock.tick()
        except pygame.error: pass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

while(True):
    display_image()