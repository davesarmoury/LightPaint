#!/usr/bin/env python3

import argparse
import rtde_control
import rtde_receive
import time
from gpiozero import RGBLED
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--IP", type=str, default="192.168.2.66", help="IP of the robot")
parser.add_argument("--Image", type=str, default="./mona_lisa.jpg", help="URI of the image file")
parser.add_argument("--Width", type=float, default=0.4, help="Width of the path (m)")
parser.add_argument("--Height", type=float, default=0.4, help="Height of the path (m)")
parser.add_argument("--Spacing", type=float, default=0.004, help="Spacing between parallel passes (m)")
parser.add_argument("--Rate", type=float, default=120.0, help="Poling rate (Hz)")
parser.add_argument("--Speed", type=float, default=0.075, help="Movement speed (m/s)")
parser.add_argument("--Distance", type=float, default=0.4, help="Distance from robot world (m)")
parser.add_argument("--Overhang", type=float, default=0.01, help="Overhang out the sides of the path (m)")
args = parser.parse_args()

def movementComplete(target, current_pose):
    if target != None:
        if abs( current_pose[2] - target[2] ) < 0.0005 and  abs( current_pose[0] - target[0] ) < 0.0005:
            return True
        else:
            return False
    else:
        return True

def nextMove(rtde_c, last_target, width, height, spacing, overhang, row_num):
    new_target = [0,0,0,0,0,0]
    if last_target:
        if row_num % 2 == 0:
            if last_target[1] < 0:
                new_target[1] = width + overhang
                new_target[2] = last_target[2]
            else:
                new_target[1] = width + overhang
                new_target[2] = last_target[2] - spacing
                row_num = row_num + 1
        else:
            if last_target[1] < 0:
                new_target[1] = -overhang
                new_target[2] = last_target[2] - spacing
                row_num = row_num + 1
            else:
                new_target[1] = -overhang
                new_target[2] = last_target[2]
    else:
        new_target[1] = -overhang

    image_complete = False
    if new_target[2] < -height:
        image_complete = True

    return new_target, image_complete, row_num

def updatePixel(current_pose, pose_to_pixel, im, led, shift):
    h = int(round( ( current_pose[0] + shift[0] ) * pose_to_pixel,0))
    v = int(round( ( current_pose[2] - shift[1] ) * pose_to_pixel * -1,0))
    if h >= 0 and v >= 0:
        try:
            r, g, b = im.getpixel((h, v))
            led.value = (r/255.0, g/255.0, b/255.0)
        except:
            led.value = (0, 0, 0)
    else:
        led.value = (0, 0, 0)

def main():
    rtde_c = rtde_control.RTDEControlInterface(args.IP)
    rtde_r = rtde_receive.RTDEReceiveInterface(args.IP)

    im = Image.open(args.Image)
    px = im.convert('RGB')

    pose_to_pixel = max(im.width / args.Width, im.height / args.Height)
    print(pose_to_pixel)
    led = RGBLED(23, 24, 25)
    rtde_c.setTcp([0,0,0,0,3.14159,0])

    image_complete = False
    current_target = None
    move_target = None
    row_num = 0
    while(True):
        current_pose = rtde_r.getActualTCPPose()
        updatePixel(current_pose, pose_to_pixel, px, led, [args.Width/2.0, args.Height/2.0])
        if movementComplete(move_target, current_pose):
            current_target, image_complete, row_num = nextMove(rtde_c, current_target, args.Width, args.Height, args.Spacing, args.Overhang, row_num)

            if not image_complete:
                move_target = rtde_c.poseTrans([-args.Width/2, -args.Distance, args.Height/2,0,0,-1.5707], current_target)
                rtde_c.moveL(move_target, args.Speed, 0.5, True)
            else:
                break

        time.sleep(1.0/args.Rate)

    rtde_c.stopScript()

main()
