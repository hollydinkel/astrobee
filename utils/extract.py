#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2016 Massachusetts Institute of Technology

"""Extract images from a rosbag.
"""
import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("date", help="Dataset date.")
    parser.add_argument("image_topic", help="Image topic.")

    args = parser.parse_args()
    
    output_dir = f"{os.getcwd()}/{args.date}/bayer"
    try: os.mkdir(output_dir)
    except FileExistsError:
        print(f"{output_dir} already exists!")

    print("Extract images from %s on topic %s" % (args.bag_file,
                                                          args.image_topic))

    bag = rosbag.Bag(args.bag_file, "r")
    bridge = CvBridge()
    count = 3631
    for topic, msg, t in bag.read_messages(topics=[args.image_topic]):
        cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")

        cv2.imwrite(os.path.join(output_dir, "%03i.jpg" % count), cv_img)
        print("Wrote image %i" % count)

        count += 1

    bag.close()

    return

if __name__ == '__main__':
    main()