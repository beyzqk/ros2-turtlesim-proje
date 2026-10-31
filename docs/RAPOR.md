# ROS 2 ile Robot Hareket Kontrolü - Proje Raporu

**Grup:** 3  
**Tarih:** Kasım 2026  

---

## 1. Giriş ve Amaç
Bu projenin amacı, ROS 2 (Robot Operating System 2) ortamında temel robotik kavramlarını (düğüm, konu, mesaj, servis) kavramak ve `turtlesim` simülasyonu üzerinde robot hareket kontrolü, konum kaydı ve durdur/devam et işlevselliklerini gerçekleştirmektir.

---

## 2. Sistem Mimarisi ve İletişim Altyapısı
ROS 2 mimarisi, DDS (Data Distribution Service) ara katmanı üzerinde çalışan dağıtık düğümlerden oluşur. 

* **Düğüm (Node):** Belirli bir işlevi yerine getiren bağımsız çalışma birimleri.
* **Konu (Topic):** Düğümler arası sürekli ve tek yönlü veri akışını sağlayan Yayımla-Abone Ol (Publisher-Subscriber) yapısı.
* **Mesaj (Message):** Konular üzerinde taşınan veri yapıları.
* **Servis (Service):** İstemci-Sunucu (Client-Server) mimarisi ile istek üzerine (RPC) çalışan çift yönlü haberleşme mekanizması.

---

## 3. Kurulum ve Ortam Hazırlığı
* **İşletim Sistemi:** Ubuntu Linux
* **ROS 2 Sürümü:** ROS 2 (Humble/Jazzy/Rolling)
* **Simülasyon:** `turtlesim`
* Otomatik kurulum işlemleri için `install.sh` betiği hazırlanmıştır.

---

## 4. Geliştirilen Uygulamalar ve Düğümler

### 4.1. Hareket Kontrol Düğümü (`motion_node`)
`turtlesim` kaplumbağasına kare ve daire hareketlerini yaptırmak için doğrusal (linear) ve açısal (angular) hız komutlarını hazırlar ve `/turtle1/cmd_vel` konusuna yayımlar.

### 4.2. Konum Kayıt Düğümü (`pose_logger`)
Kaplumbağanın `/turtle1/pose` konusundan gelen anlık konum verilerini (`x`, `y`, `theta`, `linear_velocity`, `angular_velocity`) dinler ve analiz edilmek üzere bir CSV dosyasına kaydeder.

### 4.3. Durdur / Devam Et Kontrol Mekanizması
Robotun hareketini durdurmak ve kaldığı yerden devam ettirmek için servis mimarisi kullanılmıştır.

---

## 5. Test Senaryoları ve Sonuçlar
*(Geliştirme aşamasında test sonuçları, ekran görüntüleri ve grafikler eklenecektir.)*

---

## 6. Mesleki Kazanımlar ve İş İlanları İncelemesi
*(Grup üyelerinin mesleki kazanımları ve Türkiye/yurt dışı iş ilanları incelemeleri eklenecektir.)*

---

## 7. Sonuç
Proje kapsamında ROS 2 ekosisteminde temel düğüm yönetimi, mesajlaşma ve servis kontrolü başarıyla gerçekleştirilmiştir.
