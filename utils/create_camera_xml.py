# Creating XML Document in Python
# from xml.dom import minidom
import xml.etree.ElementTree as ET
import os
from numpy import loadtxt

poses_dir = './src/data/20230419/pose/survey2/'
poses = os.listdir(poses_dir)

tree = ET.parse('cameras.xml')
root = tree.getroot()
separator = " "

for i,pose in enumerate(poses):
    with open(f"{poses_dir}/{pose}",'r') as f:
        content = f.readlines()
        l = []
        for line in content:
            row = line.split()
            val = [str(a) for a in row]
            l.append(val)
        print(l)
        listed = [item for val in l for item in val]

    root[0][1][i].set('id',f'{i}')
    root[0][1][i].set('label',f'Image{i}.JPG')
    root[0][1][i].set('sensor_id','0')
    root[0][1][i].set('enabled','true')
    root[0][1][i][0].text = separator.join(listed)

tree.write('test.xml')    
