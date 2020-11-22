#!/usr/bin/env python3

import argparse
import rtde_control
import rtde_receive
import time

parser = argparse.ArgumentParser()
parser.add_argument("--IP", type=str, default="192.168.2.66", help="IP of the robot")
parser.add_argument("--Image", type=str, default="./img.jpg", help="URI of the image file")
parser.add_argument("--Width", type=float, default=500.0, help="Width of the path (mm)")
parser.add_argument("--Height", type=float, default=500.0, help="Height of the path (mm)")
parser.add_argument("--Spacing", type=float, default=2.0, help="Spacing between parallel passes (mm)")
parser.add_argument("--Rate", type=float, default=100.0, help="Poling rate (Hz)")
parser.add_argument("--Speed", type=float, default=0.5, help="Movement speed (m/s)")
parser.add_argument("--Distance", type=float, default=500.0, help="Distance from robot world (mm)")
parser.add_argument("--Overhang", type=float, default=10.0, help="Overhang out the sides of the path (mm)")
args = parser.parse_args()

def movementComplete(target):
    if target != None:
        current_pose = rtde_r.getActualTCPPose()
        if abs( current_pose[3] - target[3] ) < 1.0 and  abs( current_pose[1] - target[1] ) < 1.0:
            return True
        else:
            return False
    else:
        return True

def nextMove(rtde_c, last_target, width, height, distance, spacing, overhang):
    new_target = [distance,0,0,0,0,0]
    if last_target[2] % (spacing * 2) == 0: #even rows
        if last_target[1] < 0:
            new_target[1] = width + overhang
            new_target[2] = last_target[2]
        else:
            new_target[1] = width + overhang
            new_target[2] = last_target[2] - spacing
    else:
        if last_target[1] > 0:
            new_target[1] = -overhang
            new_target[2] = last_target[2]
        else:
            new_target[1] = -overhang
            new_target[2] = last_target[2] - spacing

    print(new_target)

    image_complete = False
    if new_target[2] < -height:
        image_complete = True

    return target, image_complete

def updatePixel():
    current_pose = rtde_r.getActualTCPPose()

def main():
    rtde_c = rtde_control.RTDEControlInterface(args.IP)
    rtde_r = rtde_receive.RTDEReceiveInterface(args.IP)

    im = Image.open(args.Image)
    px = im.load()

    rtde_c.setTcp([0,0,0,3.14159,0,0])

    image_complete = False
    current_target = None
    while(True):
        if movementComplete(current_target):
            current_target, image_complete = nextMove(rtde_c, current_target, args.Width, args.Height, args.Distance, args.Spacing, args.Overhang)

            if not image_complete:
                move_target = poseTrans([-args.Width/2,args.Distance, args.Height/2,0,0,-1.5707], current_target)
                rtde_c.moveL(current_target, args.Speed, 0.5, True)
                break

            time.sleep(1/args.Rate)

    rtde_c.stopScript()

main()
