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

        self.phase = "ileri"
        self.pose = None
        self.start_x = None
        self.start_y = None
        self.hedef_theta = None

        if self.sekil not in ("daire", "kare"):
            self.get_logger().error(
                f"Gecersiz sekil: '{self.sekil}'. 'daire' veya 'kare' yazin."
            )
            raise SystemExit(1)

        if self.hiz <= 0:
            self.get_logger().error("hiz 0'dan buyuk olmali.")
            raise SystemExit(1)

        if self.yaricap <= 0 or self.kenar <= 0:
            self.get_logger().error("yaricap ve kenar 0'dan buyuk olmali.")
            raise SystemExit(1)

        self.pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 10)
        self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10)
        self.timer = self.create_timer(0.02, self.tick)

        self.paused = False

        self.create_service(Trigger, "/pause", self.pause_callback)
        self.create_service(Trigger, "/resume", self.resume_callback)

        self.get_logger().info(
            f"basladi: sekil={self.sekil}, hiz={self.hiz}, "
            f"yaricap={self.yaricap}, kenar={self.kenar}"
        )

    def pose_callback(self, msg):
        self.pose = msg

    @staticmethod
    def norm(a):
        return math.atan2(math.sin(a), math.cos(a))

    def tick(self):
        if self.pub.get_subscription_count() == 0:
            self.get_logger().warning(
                "turtlesim bulunamadi. Baska bir terminalde "
                "'ros2 run turtlesim turtlesim_node' calistirin.",
                throttle_duration_sec=3.0
            )
            return

        if self.paused:
            self.pub.publish(Twist())
            return

        msg = Twist()

        if self.sekil == "daire":
            msg.linear.x = self.hiz
            msg.angular.z = self.hiz / self.yaricap

        elif self.sekil == "kare":
            if self.pose is None:
                return

            if self.start_x is None:
                self.start_x = self.pose.x
                self.start_y = self.pose.y
                self.hedef_theta = self.pose.theta

            if self.phase == "ileri":
                mesafe = math.hypot(
                    self.pose.x - self.start_x,
                    self.pose.y - self.start_y
                )

                if mesafe < self.kenar:
                    msg.linear.x = self.hiz
                else:
                    self.phase = "don"
                    self.hedef_theta = self.norm(
                        self.hedef_theta + math.pi / 2
                    )

            else:
                hata = self.norm(
                    self.hedef_theta - self.pose.theta
                )

                if abs(hata) > 0.05:
                    msg.angular.z = 1.0 if hata > 0 else -1.0
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


def main():
    rclpy.init()
    node = MotionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
