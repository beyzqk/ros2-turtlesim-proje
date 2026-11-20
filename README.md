# ROS 2 Turtlesim Projesi

Bu projede ROS 2 ve turtlesim kullanarak ekrandaki kaplumbağaya kare ve
daire çizdirmeyi amaçladık. Ayrıca kaplumbağanın konum bilgilerini bir
CSV dosyasına kaydettik. Hareketi durdurmak ve tekrar devam ettirmek
için de servisler ekledik.

Projeyi yaparken ROS 2'de kullanılan düğüm, konu, servis ve parametre
gibi temel konuları uygulamalı olarak kullanmaya çalıştık.

## Projede Neler Var?

-   **Kare çizme:** Kaplumbağa önce ileri gider, sonra 90 derece döner.
    Bu hareketi tekrarlayarak kare çizer. Gidilen mesafeyi ve yönü
    `/turtle1/pose` konusundan gelen gerçek konuma bakarak kontrol eder.
    Her köşede hedef yön 90 derece artırılır ve kaplumbağa bu yöne
    dönene kadar döner.
-   **Daire çizme:** Kaplumbağanın doğrusal ve açısal hızları
    ayarlanarak daire çizmesi sağlanır.
-   **Parametreler:** Çizilecek şekil, hız, dairenin yarıçapı ve karenin
    kenar uzunluğu değiştirilebilir.
-   **Konumları kaydetme:** `pose_logger` düğümü kaplumbağanın konum
    bilgilerini takip eder ve CSV dosyasına kaydeder.
-   **Durdurma ve devam ettirme:** `/pause` servisiyle hareket
    durdurulur, `/resume` servisiyle tekrar başlatılır. Konum kaydı da
    `kontrol_betigi/control.py` ile durdurulup devam ettirilebilir.
-   **Hata mesajları:** Geçersiz şekil, hız 0 veya negatif, yarıçap ya
    da kenar 0 veya negatif olursa ve turtlesim açık değilse program
    anlaşılır bir mesaj verir.
-   **Hız deneyi:** Şekiller 0.5, 1.0 ve 2.0 hızlarında denendi, sonuçlar
    `results/` klasöründe.

## Sistemin Çalışma Mantığı

Projede iki temel düğüm bulunuyor:

-   `motion_node`: Kaplumbağanın hareket etmesini sağlar. Hareket
    komutlarını `/turtle1/cmd_vel` konusuna gönderir. Kaplumbağanın
    mevcut konumunu da `/turtle1/pose` üzerinden takip eder.
-   `pose_logger`: `/turtle1/pose` konusundan gelen konum bilgilerini
    alır ve CSV dosyasına yazar.

Durdurma ve devam ettirme işlemleri için `motion_node` içerisinde
`/pause` ve `/resume` servisleri, `pose_logger` içerisinde kayıt için
`/pose_logger/set_recording` servisi kullanılır.

  ---------------------------------------------------------------------------------------
  Düğüm             Yayınladığı konu     Dinlediği konu    Servis
  ----------------- -------------------- ----------------- ------------------------------
  `motion_node`     `/turtle1/cmd_vel`   `/turtle1/pose`   `/pause`, `/resume`
                                                           (`std_srvs/Trigger`)

  `pose_logger`     \-                   `/turtle1/pose`   `/pose_logger/set_recording`
                                                           (`std_srvs/SetBool`)
  ---------------------------------------------------------------------------------------

## Klasör Yapısı

``` text
docs/             Araştırmalar, rapor ve kaynakça
scripts/          Kurulum betiği, hız deneyi ölçüm ve grafik betikleri
src/              Kaynak kodlar (motion_node.py, pose_logger.py)
kontrol_betigi/   Konum kaydını durdurup başlatan control.py
results/          Hız deneyi sonuçları, grafikler, rqt_graph, topic ve node çıktıları
test_sonuclari/   Test sonuçları ve ekran görüntüleri
GOREV_DAGILIMI.md Görev dağılımı
README.md         Proje hakkında bilgiler
```

## Gerekli Programlar

Projeyi çalıştırmak için aşağıdakiler gereklidir:

-   Ubuntu (26.04, 24.04 veya 22.04)
-   ROS 2 (Ubuntu 26.04 için Lyrical, 24.04 için Jazzy, 22.04 için Humble)
-   turtlesim paketi
-   Python 3

Hepsi `scripts/install_ros2.sh` betiğiyle kurulur. Proje Ubuntu 26.04 ve
ROS 2 Lyrical üzerinde denenmiştir.

## Kurulum

Öncelikle proje GitHub üzerinden indirilir:

``` bash
git clone https://github.com/beyzqk/ros2-turtlesim-proje.git
cd ros2-turtlesim-proje
```

Daha sonra kurulum betiğine çalıştırma izni verilir ve betik başlatılır:

``` bash
chmod +x scripts/install_ros2.sh
./scripts/install_ros2.sh
```

Betik önce Ubuntu sürümünü ve gerekli ön koşulları kontrol eder, bir
sorun varsa nedenini yazarak durur. ROS 2 ve turtlesim kurulumunu yapar,
ROS 2 ayarını `~/.bashrc` dosyasına ekler. Kurulum bittikten sonra **yeni
bir terminal açın**. Kontrol için:

``` bash
echo $ROS_DISTRO
```

komutu `lyrical` (ya da kurduğunuz sürüm) yazmalıdır.

## Projeyi Çalıştırma

Programlar üç ayrı terminalde çalıştırılır. Her terminalde önce proje
klasörüne girin (`cd ros2-turtlesim-proje`).

**1. Terminal -- turtlesim'i açma:**

``` bash
ros2 run turtlesim turtlesim_node
```

**2. Terminal -- konum bilgilerini kaydetme (isteğe bağlı):**

``` bash
python3 src/pose_logger.py
```

**3. Terminal -- kaplumbağayı hareket ettirme:**

``` bash
python3 src/motion_node.py --ros-args -p sekil:=kare -p hiz:=1.0
```

Programı durdurmak için terminalde `Ctrl+C` basılır. Kaplumbağayı ve
çizgileri başa almak için:

``` bash
ros2 service call /reset std_srvs/srv/Empty
```

## Kullanılabilen Parametreler

  Parametre   Ne işe yarar?                              Varsayılan   Örnek değer
  ----------- ------------------------------------------ ------------ ---------------------
  `sekil`     Çizilecek şekli belirler                   `daire`      `kare`, `daire`
  `hiz`       Kaplumbağanın hızını belirler (0'dan büyük) `0.5`       `0.5`, `1.0`, `2.0`
  `yaricap`   Daire çizilirken kullanılacak yarıçap      `1.0`        `1.5`
  `kenar`     Kare çizilirken kenar uzunluğu             `2.0`        `3.0`

Sayıları `1.0` gibi ondalıklı yazın ve `:=` işaretinin iki yanında
boşluk bırakmayın.

Daire çizdirmek için örnek komut:

``` bash
python3 src/motion_node.py --ros-args -p sekil:=daire -p hiz:=1.0 -p yaricap:=2.0
```

Kare için kenar uzunluğunu değiştirmek:

``` bash
python3 src/motion_node.py --ros-args -p sekil:=kare -p hiz:=1.0 -p kenar:=3.0
```

## Hareketi Durdurma ve Devam Ettirme

`motion_node` çalışırken başka bir terminalde, kaplumbağanın hareketini
durdurmak için:

``` bash
ros2 service call /pause std_srvs/srv/Trigger
```

Tekrar hareket ettirmek için:

``` bash
ros2 service call /resume std_srvs/srv/Trigger
```

Konum kaydını durdurmak ve devam ettirmek için (`pose_logger` çalışıyor
olmalı):

``` bash
python3 kontrol_betigi/control.py durdur
python3 kontrol_betigi/control.py devam
```

## Proje Çıktıları

`pose_logger` konum bilgilerini masaüstündeki `~/Desktop/turtle_pose_log.csv`
dosyasına yazar. Sütunlar: `x`, `y`, `theta`, `linear_velocity`,
`angular_velocity`. Program her açıldığında aynı dosyanın sonuna ekleme
yapar, yeni bir kayıt için dosyayı silin veya adını değiştirin. Örnek bir
kayıt `results/pose_log_ornek.csv` dosyasındadır.

Diğer çıktılar:

-   `results/hiz_deneyi.csv`: 0.5, 1.0 ve 2.0 hızlarında kare ve daire
    için süre ve sapma ölçümleri
-   `results/grafikler/`: bu ölçümlerin grafikleri
-   `results/rqt_graph.png`, `topic_echo.txt`, `topic_hz.txt`,
    `node_info_*.txt`: düğümlerin haberleştiğini gösteren kayıtlar
-   `test_sonuclari/`: test senaryolarının ekran görüntüleri ve tablosu

Hız deneyini tekrarlamak için `scripts/olcum.py` ve `scripts/grafik.py`
kullanılır. `olcum.py` hareket düğümünü `ros2 run my_py_pkg motion_node`
ile başlattığı için `kontrol_betigi/` içindeki paketin bir ROS 2 çalışma
alanında derlenmiş olması gerekir. Normal çalıştırma için bu gerekmez.

## Kontrol İçin Kullanılan Komutlar

Çalışma sırasında ROS 2 düğümlerini ve konuları kontrol etmek için şu
komutlardan yararlanılabilir:

``` bash
ros2 node list
ros2 topic echo /turtle1/pose
ros2 topic hz /turtle1/pose
ros2 node info /motion_node
ros2 service list
rqt_graph
```

## Bilinen Sınırlar

-   Kare tam kapanmayabilir. Konum bilgisi komuttan biraz geç geldiği
    için kaplumbağa kenarı hedeften azıcık uzun gider. Dönüşte de 0.05
    radyan (yaklaşık 3 derece) tolerans bırakılmıştır. Her köşede bir
    önceki hedef yöne 90 derece eklenir, bu yüzden dönüş hataları
    birbirine eklenmez.
-   Kare çizerken dönüş hızı sabittir (1.0 rad/sn). `hiz` parametresi
    yalnızca düz giden kısımları etkiler.
-   Sanal makinede simülasyon gerçek zamandan yavaş çalışabilir, süre
    ölçümleri buna bağlıdır.

## Yapay Zekâ Kullanımı

Projede yapay zekâ (Claude) kurulum betiği, `motion_node` kodu ve
konuların anlaşılması aşamalarında yardımcı olarak kullanılmıştır. Kodları
adım adım birlikte yazıp test ettik. Ayrıntısı raporda belirtilmiştir.

## Görev Dağılımı

-   **Beyza Nur Kerter** ([@beyzqk](https://github.com/beyzqk)): Kodlama
    ve sistemin hazırlanması
-   **Duru Kürekçi** ([@durusaakiii](https://github.com/durusaakiii)):
    Verilerin hazırlanması, testler ve belgeleme

Görevlerin daha ayrıntılı açıklaması `GOREV_DAGILIMI.md` dosyasında
bulunmaktadır.
