"""Hiz deneyi olcumu.

Kullanim:  python3 olcum.py daire 0.5
           python3 olcum.py kare 1.0
Sonuc ~/Desktop/hiz_deneyi.csv dosyasina eklenir.
"""
import csv
import math
import os
import signal
import subprocess
import sys
import time

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
from turtlesim_msgs.msg import Pose
from turtlesim_msgs.srv import TeleportAbsolute

X0, Y0, TH0 = 5.5, 5.5, 0.0   # baslangic noktasi
R = 1.0                        # daire yaricapi (motion_node varsayilani)
TIMEOUT = 120.0                # saniye


def norm(a):
    return math.atan2(math.sin(a), math.cos(a))


class Olcum(Node):
    def __init__(self):
        super().__init__("olcum")
        self.samples = []
        self.create_subscription(Pose, "/turtle1/pose", self.cb, 10)
        self.tp = self.create_client(TeleportAbsolute,
                                     "/turtle1/teleport_absolute")
        self.clr = self.create_client(Empty, "/clear")

    def cb(self, m):
        self.samples.append((time.monotonic(), m.x, m.y, m.theta,
                             m.linear_velocity, m.angular_velocity))

    def call(self, client, req):
        client.wait_for_service(timeout_sec=5.0)
        fut = client.call_async(req)
        rclpy.spin_until_future_complete(self, fut, timeout_sec=5.0)

    def reset(self):
        req = TeleportAbsolute.Request()
        req.x, req.y, req.theta = X0, Y0, TH0
        self.call(self.tp, req)
        self.call(self.clr, Empty.Request())
        end = time.monotonic() + 0.5
        while time.monotonic() < end:
            rclpy.spin_once(self, timeout_sec=0.05)
        self.samples.clear()


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("daire", "kare"):
        print("Kullanim: python3 olcum.py daire|kare HIZ   (ornek: daire 0.5)")
        return
    sekil = sys.argv[1]
    hiz = float(sys.argv[2])

    rclpy.init()
    node = Olcum()
    node.reset()

    proc = subprocess.Popen(
        ["ros2", "run", "my_py_pkg", "motion_node", "--ros-args",
         "-p", f"sekil:={sekil}", "-p", f"hiz:={hiz}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    t0 = None
    idx = 0
    prev_th = TH0
    cum = 0.0
    max_r_err = 0.0
    turning = False
    corners = []
    sure = None
    sapma = None
    baslangic = time.monotonic()

    while sure is None and time.monotonic() - baslangic < TIMEOUT:
        rclpy.spin_once(node, timeout_sec=0.1)
        while idx < len(node.samples) and sure is None:
            t, x, y, th, lin, ang = node.samples[idx]
            idx += 1
            if t0 is None:
                if abs(lin) > 0.01 or abs(ang) > 0.01:
                    t0 = t
                else:
                    continue
            if sekil == "daire":
                cum += norm(th - prev_th)
                prev_th = th
                r = math.hypot(x - X0, y - (Y0 + R))
                max_r_err = max(max_r_err, abs(r - R))
                if cum >= 2 * math.pi:
                    sure = t - t0
                    sapma = math.hypot(x - X0, y - Y0)
            else:
                now_turning = abs(ang) > 0.01
                if turning and not now_turning:
                    k = len(corners) + 1
                    ideal = norm(TH0 + k * math.pi / 2)
                    corners.append(math.degrees(norm(th - ideal)))
                    if len(corners) == 4:
                        sure = t - t0
                        sapma = math.hypot(x - X0, y - Y0)
                turning = now_turning

    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
    node.destroy_node()
    rclpy.shutdown()

    if sure is None:
        print("HATA: tur tamamlanamadi (zaman asimi). Turtlesim acik mi?")
        return

    if sekil == "daire":
        yaricap_hata = f"{max_r_err:.4f}"
        kose_ort = kose_max = ""
    else:
        yaricap_hata = ""
        kose_ort = f"{sum(abs(c) for c in corners) / 4:.3f}"
        kose_max = f"{max(abs(c) for c in corners):.3f}"

    yol = os.path.expanduser("~/Desktop/hiz_deneyi.csv")
    yeni = not os.path.exists(yol)
    with open(yol, "a", newline="") as f:
        w = csv.writer(f)
        if yeni:
            w.writerow(["sekil", "hiz", "sure_s", "kapanma_hatasi",
                        "yaricap_hatasi_max", "kose_hatasi_ort_derece",
                        "kose_hatasi_max_derece"])
        w.writerow([sekil, hiz, f"{sure:.3f}", f"{sapma:.4f}",
                    yaricap_hata, kose_ort, kose_max])

    print(f"{sekil} hiz={hiz}: sure={sure:.2f} s, "
          f"kapanma hatasi={sapma:.3f} birim")
    if sekil == "daire":
        print(f"  en buyuk yaricap hatasi={max_r_err:.4f} birim")
    else:
        print("  kose hatalari (derece):",
              ", ".join(f"{c:.2f}" for c in corners))
    print("Kaydedildi:", yol)


main()
