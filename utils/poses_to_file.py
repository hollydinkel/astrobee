#! /usr/bin/env python

import numpy as np
from pyquaternion import Quaternion
import os
import argparse
import cv2

# ROS libraries
from ros_numpy import numpify
import rosbag
from cv_bridge import CvBridge

# Message imports
from sensor_msgs.msg import Image as SensorImage
from sensor_msgs.msg import CameraInfo
from geometry_msgs.msg import Pose

def main():
    """Extract a folder of images from a rosbag.
    """ 

    parser = argparse.ArgumentParser(description="Process sequential poses.")
    parser.add_argument("survey", help="Indicate survey number")
    parser.add_argument("date", help="Dataset date.")

    args = parser.parse_args()

    bag_dir = f"./src/utils/data/{args.date}/bags/survey{args.survey}"
    print(bag_dir)

    output_dir = f"./src/utils/data/{args.date}/bayer/survey{args.survey}"
    output_dir_poses = f"./src/utils/data/{args.date}/pose/survey{args.survey}"
    try: os.mkdir(output_dir)
    except FileExistsError:
        print(f"{output_dir} already exists!")
    try: os.mkdir(output_dir_poses)
    except FileExistsError:
        print(f"{output_dir_poses} already exists!")

    bridge = CvBridge()

    # # nav_cam_tf = transform(vec3(0.1157+0.002, -0.0422, -0.0826), quat4(-0.46938154, -0.52978318, -0.5317378, -0.46504373))
    
    body_to_cam_trans = np.array([0.1157+0.002, -0.0422, -0.0826])
    body_to_cam_quat_xyzw = np.array([-0.46938154, -0.52978318, -0.5317378, -0.46504373])
    body_to_cam_quat_wxyz = Quaternion(w=body_to_cam_quat_xyzw[3],x=body_to_cam_quat_xyzw[0],y=body_to_cam_quat_xyzw[1],z=body_to_cam_quat_xyzw[2])
    body_to_cam_transf = body_to_cam_quat_wxyz.transformation_matrix
    body_to_cam_transf[0:3,3] = body_to_cam_trans.T

    for bag_file in os.listdir(bag_dir):
        bag = rosbag.Bag(os.path.join(bag_dir,bag_file),"r")

        data = {'pose': [],
                'pose_time': [],
                'image_time': []}
        for (topic, msg, t) in bag.read_messages(topics=['/ground_truth/gnc/ekf','/hw/cam_nav_bayer']):
            
            if topic == '/ground_truth/gnc/ekf':
                pose = msg.pose
                trans = np.array([pose.position.x, pose.position.y, pose.position.z])
                quat_xyzw = [pose.orientation.x,pose.orientation.y,pose.orientation.z,pose.orientation.w]
                quat_wxyz = Quaternion(w=quat_xyzw[3],x=quat_xyzw[0],y=quat_xyzw[1],z=quat_xyzw[2])
                transf = quat_wxyz.transformation_matrix
                transf[0:3,3] = trans.T
                data['pose'].append(transf)
                data['pose_time'].append(t)
            
            if topic == '/hw/cam_nav_bayer':
                cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
                rgb = cv2.cvtColor(cv_img, cv2.COLOR_BayerGBRG2RGB) 
                data['image_time'].append(t)
                cv2.imwrite(os.path.join(output_dir, f"{t}.jpg"), rgb)

        for image_t in data['image_time']:
            diff = []
            for pose_t, pose in zip(data['pose_time'],data['pose']):
                diff.append(abs(pose_t-image_t))
            i = np.argmin(diff)
            saved_pose = data['pose'][i]
            saved_t = data['pose_time'][i]
            np.savetxt(f'{output_dir_poses}/{saved_t}.txt', saved_pose@body_to_cam_transf)
            print(f"Wrote TF {saved_t}")

        bag.close()

if __name__ == "__main__":
    main()