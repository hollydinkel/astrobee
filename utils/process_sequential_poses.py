#! /usr/bin/env python3

import numpy as np
# from pyquaternion import Quaternion
import os


img_dir = "./src/utils/data/20230419/bayer/survey2"
poses_dir = "./src/utils/data/20230419/pose/survey2"

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
