#! /usr/bin/env python3

import numpy as np
import os
import argparse


parser = argparse.ArgumentParser(description="Process sequential poses.")
parser.add_argument("survey", help="Indicate survey number")
parser.add_argument("date", help="Dataset date.")

args = parser.parse_args()

img_dir = f"./src/utils/data/{args.date}/bayer/survey{args.survey}"
poses_dir = f"./src/utils/data/{args.date}/pose/survey{args.survey}"

pose_list = [int(os.path.splitext(file)[0]) for file in os.listdir(poses_dir)]
img_list = [int(os.path.splitext(file)[0]) for file in os.listdir(img_dir)]

save = []
for img in img_list:
    diff = []
    for pose in pose_list:
        diff.append(abs(pose-img))
    i = np.argmin(diff)
    save.append(f'{pose_list[i]}.txt')

remove = list(set(os.listdir(poses_dir)).difference(save))

for file in remove:
    os.remove(os.path.join(poses_dir,file))
