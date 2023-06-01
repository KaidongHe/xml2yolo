#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Image
import os
import cv2
import glob
import numpy as np
import time
import threading


save_dir = '/home/ucar/ucar_ws/src/opencv_test/src/pictures_train/'
image_count = 0

def get_dir_number():
    global image_count
    image_types = ["*.jpg", "*.jpeg", "*.png", "*.bmp"] # 支持的图片类型

    for image_type in image_types:
        image_count += len(glob.glob(os.path.join(save_dir, image_type)))

    print("文件夹中共有%d张图片" % image_count)

class UcarCamera:
    def __init__(self):
        global image_count

        rospy.init_node("ucar_camera", anonymous=True)

        self.img_width=int(rospy.get_param('~image_width',default=1920))
        self.img_height=int(rospy.get_param('~image_height',default=1080))

        self.camera_topic_name=rospy.get_param('~cam_topic_name',default="/ucar_camera/image_raw")
        self.cam_pub=rospy.Publisher(self.camera_topic_name,Image,queue_size=1)          #定义发布器
        
        self.image_temp=Image()                    #创建一个ROS的用于发布图片的Image()消息
        self.image_temp.header.frame_id = 'opencv' #定义图片header里的id号
        self.image_temp.height=self.img_height        #定义图片高度
        self.image_temp.width=self.img_width          #定义图片宽度
        self.image_temp.encoding='rgb8'            #图片格式    
        self.image_temp.is_bigendian=True
        self.image_temp.step=self.img_width*3         #告诉ROS图片每行的大小 28是宽度3是3byte像素（rgb）
        ## 设置摄像头相关信息
        device_path=rospy.get_param('device_path',default="/dev/ucar_video")
        self.cap = cv2.VideoCapture(device_path)
        self.cap.set(3, self.img_width) 
        self.cap.set(4, self.img_height)
        codec = cv2.VideoWriter.fourcc('M', 'J', 'P', 'G')
        self.cap.set(cv2.CAP_PROP_FOURCC, codec)
        self.cam_pub_rate=int(rospy.get_param('~rate',default=25))
        ros_rate = rospy.Rate(self.cam_pub_rate)  #定义发布频率

        get_dir_number()
        i = image_count

        while not rospy.is_shutdown():
            ros_rate = rospy.Rate(self.cam_pub_rate)  #初始化发布频率
            # ret,frame_1 = self.cap.read()   ##ret 为布尔值表示是否可以获得图像    frame为获取的帧
            # frame_1 = cv2.flip(frame_1,1) 
            # self.frame = cv2.cvtColor(frame_1, cv2.COLOR_BGR2RGB) # 由OPENCV默认的BGR转为通用的RGB
            # self.image_temp.header = Header(stamp=rospy.Time.now())   #定义图片header
            # self.image_temp.data=np.array(self.frame).tostring()   #图片内容，这里要转换成字符串
            # self.cam_pub.publish(self.image_temp)
            
            if input('输入回车键以采集一次数据：') == '':
                for x in range(6):
                    ret ,frame1 = self.cap.read()  # 采集一帧图片
                frame1 = cv2.flip(frame1,1)     
                cv2.imwrite(save_dir + '%d.jpg' %i, frame1)  # 写入图片以及命名
                # cv2.namedWindow("miku",0)
                # cv2.resizeWindow("miku", 640, 480)
                # cv2.imshow("miku", frame)
                print('%05d.采集成功' %i)
                
                i += 1

            ros_rate.sleep()

    


    
       
if __name__ == '__main__':
    ucar_camera =  UcarCamera()


