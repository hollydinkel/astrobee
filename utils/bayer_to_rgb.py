#!/usr/bin/env python
import os
import cv2
import sys
import numpy as np

width = 1280
height = 960

dir = str(sys.argv[1])
dir_list = os.listdir(dir)
try: os.mkdir(f"{dir}/rgb")
except: print("Dir exists!")

for file in dir_list[1:]:
    path = f"{dir}/{file}"
    print(path)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    rgb = cv2.cvtColor(img, cv2.COLOR_BayerGBRG2RGB) 
    cv2.imwrite(f"{dir}/rgb/{file}",rgb)