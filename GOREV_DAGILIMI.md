# Görev Dağılımı ve Yol Haritası

Proje: ROS 2 + turtlesim ile kare/daire hareketi, konum kaydı, durdur/yeniden başlat.
Ekip: **Beyza Nur Kerter** (@beyzqk) ve **Duru Kürekçi** (@durusaakiii)
Hedef: Tüm teslimler **22 Kasım 2026 (Pazar)** günü hazır. 23,24 Kasım prova. Sunum günü: 25 Kasım 2026 Çarşamba

## Klasör yapısı

```
docs/       rapor, poster, ilan ekran görüntüleri
scripts/    kurulum ve çalıştırma betikleri
src/        ROS 2 paketi (motion_node, pose_logger)
results/    CSV kayıtları, grafikler, ekran görüntüleri
README.md
```

## Beyza Nur Kerter: Kod ve sistem

| Tarih | Görev |
|---|---|
| 30 Eki – 1 Kas | Depo ve pano kurulumu; `scripts/install_ros2.sh` (sürüm ve ön koşul kontrolü); düğüm ve konu araştırması |
| 2 – 8 Kas | Paket iskeleti; `motion_node` (kare, daire, parametreler); `scripts/run_demo.sh` |
| 9 – 15 Kas | `/pause` ve `/resume` servisleri; hız parametreleri (0.5 / 1.0 / 2.0); hata yönetimi; kod dondurma |
| 16 – 21 Kas | README; rapor (giriş, düğüm/konu, kurulum, sistem yapısı); proje yönetim kayıtları; Türkiye'den iş ilanı |
| 22 – 24 Kas | Canlı demo ortamı, yedek plan, prova |

## Duru Kürekçi: Veri, test ve belgeleme

| Tarih | Görev |
|---|---|
| 30 Eki – 1 Kas |  Mesaj ve servis araştırması; yurt dışı iş ilanı; rapor iskeleti ve kaynakça |
| 2 – 8 Kas | `pose_logger` (CSV kaydı); `rqt_graph`, `topic echo`, `topic hz`, `node info` ekran görüntüleri |
| 9 – 15 Kas | Kontrol betiği; 4 test senaryosu; hız deneyi ve grafikler |
| 16 – 21 Kas | Rapor (mesaj/servis, testler, hız analizi, iş ilanı tablosu, kazanımlar); poster; uygulama videosu |
| 22 – 24 Kas | Prezi sunumu ve PDF kopyası; prova |

## Ortak işler

- iş ilanlarının incelenmesi
- Rapor, sunum, poster, video hazırlanması
- Raporun son okuması ve kaynakça
- Her kişinin kendi **bireysel katkı beyanı** (PR, issue ve commit kayıtlarına dayanarak)

## Kontrol noktaları

| Tarih | Kontrol |
|---|---|
| 1 Kas | Kurulum betiği iki bilgisayarda çalışıyor, araştırma notları var, iki iş ilanı seçildi |
| 8 Kas | Kare/daire + CSV kaydı uçtan uca çalışıyor |
| 15 Kas | Kod donduruldu, testler ve hız deneyi bitti |
| 21 Kas | Tüm teslimler hazır ve teslim alanına yüklendi |
| 22,23 Kas | Yedek gün: eksik, bozuk dosya ve link kontrolü |
| 24 Kas | Son prova |
