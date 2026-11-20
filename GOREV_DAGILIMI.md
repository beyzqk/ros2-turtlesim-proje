# Görev Dağılımı ve Yol Haritası

Proje: ROS 2 + turtlesim ile kare/daire hareketi, konum kaydı, durdur/yeniden başlat.
Ekip: **Beyza Nur Kerter** (@beyzqk) ve **Duru Kürekçi** (@durusaakiii)
Hedef: Tüm teslimler **22 Kasım 2026 (Pazar)** günü hazır. 23,24 Kasım prova. Sunum günü: 25 Kasım 2026 Çarşamba

## Klasör yapısı

```
docs/       araştırma, rapor, poster, ilan ekran görüntüleri, Kaynakça
scripts/    kurulum ve çalıştırma betikleri
src/     ROS 2 paketi (motion_node, pose_logger)
results/    CSV kayıtları, grafikler, ekran görüntüleri
test_sonucları/ yapılan testler ve ekran görüntüleri
README.md
```

## Beyza Nur Kerter: Kod ve sistem

| Tarih | Görev |
|---|---|
| 30 Eki – 1 Kas | Depo ve pano kurulumu; `scripts/install_ros2.sh` (sürüm ve ön koşul kontrolü); düğüm ve konu araştırması |
| 2 – 8 Kas | Paket iskeleti; `motion_node` (kare, daire, parametreler); |
| 9 – 15 Kas | `/pause` ve `/resume` servisleri; hız parametreleri (0.5 / 1.0 / 2.0); hata yönetimi; |
| 16 – 22 Kas | README; rapor (giriş, düğüm/konu, kurulum, sistem yapısı);|
| 22 – 24 Kas | prova |

## Duru Kürekçi: Veri, test ve belgeleme

| Tarih | Görev |
|---|---|
| 30 Eki – 1 Kas |  Mesaj ve servis araştırması; rapor iskeleti ve kaynakça |
| 2 – 8 Kas | `pose_logger` (CSV kaydı); `rqt_graph`, `topic echo`, `topic hz`, `node info` ekran görüntüleri |
| 9 – 15 Kas | Kontrol betiği; 4 test senaryosu; hız deneyi ve grafikler |
| 16 – 21 Kas | Rapor (mesaj/servis, testler, hız analizi, iş ilanı tablosu, kazanımlar);|
| 22 – 24 Kas | prova|

## Ortak işler
- Rapor, sunum, poster, video hazırlanması
- Raporun son okuması ve kaynakça
- Her kişinin kendi **bireysel katkı beyanı**
- Türkiye'den ve yurtdışından iş ilanlarının incelenmesi.

