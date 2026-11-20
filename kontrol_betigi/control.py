#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

def kayit_ayarla(acik):
   rclpy.init()
   node = Node('control_client')
   client = node.create_client(SetBool, '/pose_logger/set_recording')
   if not client.wait_for_service(timeout_sec=3.0):
       print('Servis bulunamadı, pose_logger calisiyor mu?')
       node.destroy_node()
       rclpy.shutdown()
       return
   istek = SetBool.Request()
   istek.data = acik
   gelecek = client.call_async(istek)
   rclpy.spin_until_future_complete(node, gelecek)
   print(gelecek.result().message)
   node.destroy_node()
   rclpy.shutdown()
   
   
def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ('durdur', 'devam'):
        print('Kullanim: control.py durdur|devam')
        return
    kayit_ayarla(sys.argv[1] == 'devam')
    
if __name__ == '__main__':
    main()
