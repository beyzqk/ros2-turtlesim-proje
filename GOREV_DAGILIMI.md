# Görev Dağılımı ve Yol Haritası

Proje: ROS 2 + turtlesim ile kare/daire hareketi, konum kaydı, durdur/yeniden başlat.
Ekip: **Beyza Nur Kerter** (@beyzqk) ve **Duru Kürekçi** (@durusaakiii)
Hedef: Tüm teslimler **22 Kasım 2026 (Pazar)** günü hazır. 23 Kasım yedek gün, 24 Kasım prova. İlk sunum günü: 25 Kasım 2026 Çarşamba 09.30.

## Çalışma kuralları

- Her görev için ayrı branch açılır, birleştirme pull request ile yapılır ve diğer kişi inceler.
- Görevler GitHub Issues / Projects üzerinden takip edilir. Süreç baştan kayıtlıdır.
- Kod en geç **19 Kasım**'da donar. Sonrası sadece hata düzeltme.
- Haftada bir 30 dakikalık kısa görüşme yapılır.

## Klasör yapısı

```
docs/       rapor, poster, ilan ekran görüntüleri
scripts/    kurulum ve çalıştırma betikleri
src/        ROS 2 paketi (motion_node, pose_logger)
results/    CSV kayıtları, grafikler, ekran görüntüleri
README.md
```

## Kişi A: Kod ve sistem

| Tarih | Görev |
|---|---|
| 30 Eki – 5 Kas | Depo ve pano kurulumu; `scripts/install_ros2.sh` (sürüm ve ön koşul kontrolü); düğüm ve konu araştırması |
| 6 – 12 Kas | Paket iskeleti; `motion_node` (kare, daire, parametreler); `scripts/run_demo.sh` |
| 13 – 19 Kas | `/pause` ve `/resume` servisleri; hız parametreleri (0.5 / 1.0 / 2.0); hata yönetimi; kod dondurma |
| 20 – 22 Kas | README; rapor (giriş, düğüm/konu, kurulum, sistem yapısı); proje yönetim kayıtları; Türkiye'den iş ilanı |
| 23 – 24 Kas | Canlı demo ortamı, yedek plan, prova |

## Kişi B: Veri, test ve belgeleme

| Tarih | Görev |
|---|---|
| 30 Eki – 5 Kas | Kurulum betiğini ikinci bilgisayarda test; mesaj ve servis araştırması; yurt dışı iş ilanı; rapor iskeleti ve kaynakça |
| 6 – 12 Kas | `pose_logger` (CSV kaydı); `rqt_graph`, `topic echo`, `topic hz`, `node info` ekran görüntüleri |
| 13 – 19 Kas | Kontrol betiği; 4 test senaryosu; hız deneyi ve grafikler |
| 20 – 22 Kas | Rapor (mesaj/servis, testler, hız analizi, iş ilanı tablosu, kazanımlar); poster; uygulama videosu (en fazla 5 dk) |
| 23 – 24 Kas | Prezi sunumu ve PDF kopyası; prova |

## Ortak işler

- Prezi sunumu (her ikiniz de konuşacak, toplam en fazla 13 dk + 2 dk soru-cevap)
- Raporun son okuması ve kaynakça
- Her kişinin kendi **bireysel katkı beyanı** (PR, issue ve commit kayıtlarına dayanarak)

## Kontrol noktaları

| Tarih | Kontrol |
|---|---|
| 5 Kas | Kurulum betiği iki bilgisayarda çalışıyor, araştırma notları var, iki iş ilanı seçildi |
| 12 Kas | Kare/daire + CSV kaydı uçtan uca çalışıyor |
| 19 Kas | Kod donduruldu, testler ve hız deneyi bitti |
| 22 Kas | Tüm teslimler hazır ve teslim alanına yüklendi |
| 23 Kas | Yedek gün: eksik, bozuk dosya ve link kontrolü |
| 24 Kas | Son prova |
