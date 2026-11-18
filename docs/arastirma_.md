# ROS 2 Mimarisi

**Linux İşletim Sistemi Kullanımı ve Yönetimi – 3. Grup Proje Araştırması**

---

## ROS Nedir?

ROS, robot kontrol yazılımı geliştirmek için geliştirilmiş açık kaynaklı bir yazılımdır. İsminde "işletim sistemi" geçmesine rağmen bir işletim sistemi değildir.

Temel olarak şunların bütünüdür:

- İletişim altyapısı
- Çerçeve (framework) yazılımları ve araçlar
- Ekosistem

---

## ROS 2 Mimarisi

ROS 2, temelde **gerçek zamanlı dağıtık servis tabanlı mimari** üzerinde çalışmaktadır. Robotlarda sensörler, hareket kontrolörleri, algılama algoritmaları, yapay zeka algoritmaları vb. birer bileşen olarak yer alabilmekte ve bu bileşenler dağıtık ortamda veri alışverişi yaparak robot kontrolünü sağlamaktadır.

Veri alışverişi için ROS 2 ile seçilmiş olan **DDS ara katmanı**, bu bileşenlerin birbiri ile dağıtık ortamda haberleşmesini sağlamaktadır.

---

## ROS 2 İstemci Kütüphanesi

ROS 2 uygulamaları, **ROS Client Library (RCL)** istemci kütüphanesi üzerinden ROS 2 özelliklerine erişmektedir.

RCL kütüphanesi C dili ile yazılmıştır. Bunun üzerinde:

| Dil | İstemci Kütüphanesi |
|-----|---------------------|
| C++ | `rclcpp` |
| Python | `rclpy` |

---

## ROS 2 Çizge Yapısı

**Node**, **topic**, **mesaj yapısı** ve **keşif**, ROS 2'nin temel dağıtık mimarisini oluşturmaktadır. Bu yapı ROS 2 terminolojisinde **çizge (graph)** olarak adlandırılmaktadır.

---

## ROS 2'nin Düğüm, Konu, Mesaj ve Servis Kavramları

### Düğüm (Node)

Dağıtık uygulamalar, "düğüm (node)" olarak bilinen birimler olarak tasarlanmaktadır. Bir robot sisteminde sensörler, hareket kontrolörleri ve algoritma bileşenleri birer düğüm olabilmektedir.

ROS 2, düğüm kavramını işletim sistemi seviyesindeki görev yapısından ayırmıştır. İstendiğinde bir görev içinde birden fazla düğüm yaratılıp bu düğümler bağımsız şekilde diğer düğümlerle iletişim kurabilmektedir.

Sistemdeki bütün düğümler tek bir bilgisayarda çalışabileceği gibi, birden fazla bilgisayara dağıtık şekilde yerleştirilip çalıştırılabilirler.

### Konu, Servis ve Aksiyon (Topic, Service and Action)

Düğümler birbiri ile **konu**, **servis çağrıları** ve **aksiyon** ile haberleşir.

#### Konu (Topic)

Konu haberleşmesi **yayımla–abone ol (publish–subscribe)** mimarisi yardımıyla çalışır: bir düğümün ürettiği veri birden fazla düğüme iletilir ve benzer şekilde bir veri birden fazla düğüm tarafından üretilebilir. ROS 2'de tanımlı konular, DDS konularıyla birebir eşleşmektedir.

#### Servis (Service)

Servis çağrıları, uygulama geliştirici bakış açısıyla **uzaktan metot çağırma** yaklaşımını kullanmaktadır. Bu servis çağrıları da ROS 2'de DDS ara katmanı üzerinden **istek ve cevap** konusu olarak uygulanmaktadır.

#### Aksiyon (Action)

Aksiyonlar, **uzun süren servis çağrıları** için kullanılan bir yaklaşımdır. İstemci sunucudan bir aksiyon ister; sunucu uzun süren işlemi başlatır, ara sonuçları yayımlar ve aksiyon bittiğinde sonucu raporlar. Böylece hem performans açısından hem de hataya dayanıklılık açısından büyük avantaj sağlar.

### Mesajlar (Message)

Konu iletişiminde kullanılan veri tipleri **mesaj** olarak adlandırılır. Bu mesaj veri yapıları temelde DDS veri tipleri ile eşleşmektedir.

---

## Kaynakça

- [Robot İşletim Sistemi 2: ROS 2 Mimarisi – Medium](https://medium.com/yaz%C4%B1l%C4%B1m-mimarileri/robot-i%CC%87%C5%9Fletim-sistemi-2-ros-2-mimarisi-1345ae6c69dc)
