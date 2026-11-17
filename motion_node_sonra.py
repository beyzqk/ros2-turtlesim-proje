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

        self.shape = self.get_parameter("sekil").value
        self.speed = self.get_parameter("hiz").value
        self.radius = self.get_parameter("yaricap").value
        self.side = self.get_parameter("kenar").value

        # kare icin durum bilgileri
        self.phase = "ileri"
        self.pose = None
        self.start_x = None
        self.start_y = None
        self.heading = None

        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.timer = self.create_timer(0.02, self.tick)
        self.paused = False
        self.create_service(Trigger, "/pause", self.pause_callback)
        self.create_service(Trigger, "/resume", self.resume_callback)

        self.get_logger().info(
            f"basladi: sekil={self.shape}, hiz={self.speed}, "
            f"yaricap={self.radius}, kenar={self.side}")

    @staticmethod
    def norm(a):
        return math.atan2(math.sin(a), math.cos(a))

    def pose_callback(self, msg):
        self.pose = msg

    def tick(self):
        msg = Twist()
        if self.paused:
            self.pub.publish(msg)
            return

        if self.shape == "daire":
            msg.linear.x = self.speed
            msg.angular.z = self.speed / self.radius

        elif self.shape == "kare":
            if self.pose is None:
                return

            if self.start_x is None:
                self.start_x = self.pose.x
                self.start_y = self.pose.y
                self.heading = self.pose.theta

            if self.phase == "ileri":
                mesafe = math.hypot(self.pose.x - self.start_x,
                                    self.pose.y - self.start_y)
                if mesafe < self.side:
                    msg.linear.x = self.speed
                else:
                    self.phase = "don"
                    # hedef aci sabit: onceki hedef + 90 derece
                    self.heading = self.norm(self.heading + math.pi / 2)
            else:
                hata = self.norm(self.heading - self.pose.theta)
                if abs(hata) > 0.01:
                    msg.angular.z = max(-self.speed,
                                        min(self.speed, 3.0 * hata))
                else:
                    self.phase = "ileri"
                    self.start_x = self.pose.x
                    self.start_y = self.pose.y

        self.pub.publish(msg)

    def pause_callback(self, request, response):
        self.paused = True
        response.success = True
        response.message = "durduruldu"
        return response

    def resume_callback(self, request, response):
        self.paused = False
        response.success = True
        response.message = "devam ediyor"
        return response


def main(args=None):
    rclpy.init(args=args)
    node = MotionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
