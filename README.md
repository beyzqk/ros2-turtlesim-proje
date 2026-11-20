# ROS 2 Turtlesim Projesi

Bu projede ROS 2 ve turtlesim kullanarak ekrandaki kaplumbağaya kare ve
daire çizdirmeyi amaçladık. Ayrıca kaplumbağanın konum bilgilerini bir
CSV dosyasına kaydettik. Hareketi durdurmak ve tekrar devam ettirmek
için de servisler ekledik.

Projeyi yaparken ROS 2'de kullanılan düğüm, konu, servis ve parametre
gibi temel konuları uygulamalı olarak kullanmaya çalıştık.

## Projede Neler Var?

-   **Kare çizme:** Kaplumbağa önce ileri gider, sonra 90 derece döner.
    Bu hareketi tekrarlayarak kare çizer.
-   **Daire çizme:** Kaplumbağanın doğrusal ve açısal hızları
    ayarlanarak daire çizmesi sağlanır.
-   **Parametreler:** Çizilecek şekil, hız ve dairenin yarıçapı
    değiştirilebilir.
-   **Konumları kaydetme:** `pose_logger` düğümü kaplumbağanın konum
    bilgilerini takip eder ve CSV dosyasına kaydeder.
-   **Durdurma ve devam ettirme:** `/pause` servisiyle hareket
    durdurulur, `/resume` servisiyle tekrar başlatılır.
-   **Kolay çalıştırma:** `scripts/run_demo.sh` dosyası kullanılarak
    gerekli düğümler birlikte başlatılabilir.

## Sistemin Çalışma Mantığı

Projede iki temel düğüm bulunuyor:

-   `motion_node`: Kaplumbağanın hareket etmesini sağlar. Hareket
    komutlarını `/turtle1/cmd_vel` konusuna gönderir. Kaplumbağanın
    mevcut konumunu da `/turtle1/pose` üzerinden takip eder.
-   `pose_logger`: `/turtle1/pose` konusundan gelen konum bilgilerini
    alır ve CSV dosyasına yazar.

Durdurma ve devam ettirme işlemleri için `motion_node` içerisinde
`/pause` ve `/resume` servisleri kullanılır.

  --------------------------------------------------------------------------
  Düğüm             Yayınladığı konu     Dinlediği konu    Servis
  ----------------- -------------------- ----------------- -----------------
  `motion_node`     `/turtle1/cmd_vel`   `/turtle1/pose`   `/pause`,
                                                           `/resume`

  `pose_logger`     \-                   `/turtle1/pose`   \-
  --------------------------------------------------------------------------

## Klasör Yapısı

``` text
docs/             Rapor ve ekran görüntüleri
scripts/          Kurulum ve çalıştırma dosyaları
src/              ROS 2 paketinin kaynak kodları
results/          CSV kayıtları ve diğer çıktılar
test_sonuclari/   Test sonuçları
GOREV_DAGILIMI.md Görev dağılımı
README.md         Proje hakkında bilgiler
```

## Gerekli Programlar

Projeyi çalıştırmak için aşağıdakiler gereklidir:

-   Ubuntu
-   ROS 2 (Humble veya Jazzy gibi)
-   turtlesim paketi
-   Python 3
-   colcon

`turtlesim` yüklü değilse şu komutla yüklenebilir:

``` bash
sudo apt install ros-$ROS_DISTRO-turtlesim
```

## Kurulum

Öncelikle proje GitHub üzerinden indirilir:

``` bash
git clone https://github.com/beyzqk/ros2-turtlesim-proje.git
cd ros2-turtlesim-proje
```

Daha sonra ROS 2 ortamı ve proje derlenir:

``` bash
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
source install/setup.bash
```

Kurulum sırasında kontrol yapmak için `scripts/install_ros2.sh` dosyası
da kullanılabilir.

## Projeyi Çalıştırma

Projeyi tek seferde başlatmak için aşağıdaki komut kullanılabilir:

``` bash
./scripts/run_demo.sh
```

İstenirse programlar ayrı terminallerden de çalıştırılabilir.

**1. Terminal -- turtlesim'i açma:**

``` bash
ros2 run turtlesim turtlesim_node
```

**2. Terminal -- konum bilgilerini kaydetme:**

``` bash
ros2 run <paket_adi> pose_logger
```

**3. Terminal -- kaplumbağayı hareket ettirme:**

``` bash
ros2 run <paket_adi> motion_node --ros-args -p shape:=square -p speed:=1.0
```

Buradaki `<paket_adi>` yazan yere `src/` klasöründeki ROS 2 paketinin
adı yazılmalıdır.

## Kullanılabilen Parametreler

  Parametre   Ne işe yarar?                                     Örnek değer
  ----------- ------------------------------------------------- ---------------------
  `shape`     Çizilecek şekli belirler                          `square`, `circle`
  `speed`     Kaplumbağanın hızını belirler                     `0.5`, `1.0`, `2.0`
  `radius`    Daire çizilirken kullanılacak yarıçapı belirler   `1.5`

Daire çizdirmek için örnek komut:

``` bash
ros2 run <paket_adi> motion_node --ros-args -p shape:=circle -p speed:=1.0 -p radius:=2.0
```

## Hareketi Durdurma ve Devam Ettirme

Kaplumbağanın hareketini durdurmak için:

``` bash
ros2 service call /pause std_srvs/srv/Trigger
```

Tekrar hareket ettirmek için:

``` bash
ros2 service call /resume std_srvs/srv/Trigger
```

## Proje Çıktıları

Kaplumbağanın konum bilgileri `results/` klasörüne CSV dosyası olarak
kaydedilir. Dosya adında kayıt tarihi, çizilen şekil ve hız bilgileri
bulunur.

## Kontrol İçin Kullanılan Komutlar

Çalışma sırasında ROS 2 düğümlerini ve konuları kontrol etmek için şu
komutlardan yararlanılabilir:

``` bash
ros2 node list
ros2 topic echo /turtle1/pose
ros2 topic hz /turtle1/pose
ros2 node info /motion_node
rqt_graph
```

## Görev Dağılımı

-   **Beyza Nur Kerter** ([@beyzqk](https://github.com/beyzqk)): Kodlama
    ve sistemin hazırlanması
-   **Duru Kürekçi** ([@durusaakiii](https://github.com/durusaakiii)):
    Verilerin hazırlanması, testler ve belgeleme

Görevlerin daha ayrıntılı açıklaması `GOREV_DAGILIMI.md` dosyasında
bulunmaktadır.
