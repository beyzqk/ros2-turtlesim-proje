#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim_msgs.msg import Pose
from std_srvs.srv import SetBool
import csv
import os

class PoseLogger(Node):
    def __init__(self):
        super().__init__('pose_logger')
        
        self.subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )
        
        desktop_path = os.path.expanduser('~/Desktop')
        self.file_path = os.path.join(desktop_path, 'turtle_pose_log.csv')
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['x', 'y', 'theta', 'linear_velocity', 'angular_velocity'])
        self.recording = True
        self.srv = self.create_service(
            SetBool,
            '/pose_logger/set_recording',
            self.set_recording_callback
        )   
            
        self.get_logger().info('Pose Logger Başlatıldı!')
        
    def set_recording_callback(self, request, response):
        self.recording = request.data
        response.success = True
        if self.recording:
            response.message = 'Kayit devam ediyor'
        else:
            response.message = 'Kayit durduruldu'  
        self.get_logger().info(response.message)
        return response
  
    def pose_callback(self, msg):
        if not self.recording:
            return
        with open(self.file_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([msg.x, msg.y, msg.theta, msg.linear_velocity, msg.angular_velocity])

def main(args=None):
    rclpy.init(args=args)
    node = PoseLogger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
