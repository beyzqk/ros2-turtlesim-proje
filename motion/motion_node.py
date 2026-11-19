import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim_msgs.msg import Pose
from std_srvs.srv import Trigger


class MotionNode(Node):
    def __init__(self):
        super().__init__("motion_node")

        self.declare_parameter("sekil", "daire")
        self.declare_parameter("hiz", 0.5)
        self.declare_parameter("yaricap", 1.0)
        self.declare_parameter("kenar", 2.0)

        self.sekil = self.get_parameter("sekil").value
        self.hiz = self.get_parameter("hiz").value
        self.yaricap = self.get_parameter("yaricap").value
        self.kenar = self.get_parameter("kenar").value

        # kare icin durum bilgileri
        self.phase = "ileri"
        self.pose = None
        self.start_x = None
        self.start_y = None
        self.start_theta = 0.0

        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.timer = self.create_timer(0.02, self.tick)
        self.paused = False
        self.create_service(Trigger, "/pause", self.pause_callback)
        self.create_service(Trigger, "/resume", self.resume_callback)

        self.get_logger().info(
            f"basladi: sekil={self.sekil}, hiz={self.hiz}, "
            f"yaricap={self.yaricap}, kenar={self.kenar}")

    def pose_callback(self, msg):
        self.pose = msg

    def tick(self):
        if self.paused:
            self.pub.publish(Twist())
            return

        if self.sekil == "daire":
            msg.linear.x = self.hiz
            msg.angular.z = self.hiz / self.yaricap

        elif self.sekil == "kare":
            if self.pose is None:
                return

            if self.start_x is None:
                self.start_x = self.pose.x
                self.start_y = self.pose.y

            if self.phase == "ileri":
                mesafe = math.hypot(self.pose.x - self.start_x,
                                    self.pose.y - self.start_y)
                if mesafe < self.kenar:
                    msg.linear.x = self.hiz
                else:
                    self.phase = "dön"
                    self.start_theta = self.pose.theta
            else:
                fark = self.pose.theta - self.start_theta
                donen = math.atan2(math.sin(fark), math.cos(fark))
                if donen < math.pi / 2:
                    msg.angular.z = self.hiz
                else:
                    self.phase = "ileri"
                    self.start_x = self.pose.x
                    self.start_y = self.pose.y

        self.pub.publish(msg)

    def pause_callback(self, request, response):
        self.paused = True
        response.success = True
        response.mesage = "durduruldu"
        return response
    def resume_callback(self, request, response):
        self.paused = False
        response.success = True
        response.message = "devam ediyor"
        return response

def main():
    rclpy.init()
    node = MotionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


main()
