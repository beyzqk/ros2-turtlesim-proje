"""Hiz deneyi grafikleri.

Girdi : ~/Desktop/hiz_deneyi.csv        (daire + kare, yeni kod)
        ~/Desktop/hiz_deneyi_once.csv   (daire + kare, eski kod)
Cikti : ~/Desktop/grafikler/*.png
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DESK = os.path.expanduser("~/Desktop")
OUT = os.path.join(DESK, "grafikler")
os.makedirs(OUT, exist_ok=True)


def oku(dosya, sekil):
    satirlar = []
    with open(os.path.join(DESK, dosya)) as f:
        for r in csv.DictReader(f):
            if r["sekil"] == sekil:
                satirlar.append(r)
    satirlar.sort(key=lambda r: float(r["hiz"]))
    return satirlar


def sayi(satirlar, kolon):
    return [float(r[kolon]) for r in satirlar]


daire = oku("hiz_deneyi.csv", "daire")
kare_yeni = oku("hiz_deneyi.csv", "kare")
kare_eski = oku("hiz_deneyi_once.csv", "kare")

hizlar = [float(r["hiz"]) for r in daire]
xs = list(range(len(hizlar)))
etiket = [f"{h:g}" for h in hizlar]


def cizgi(dosya, baslik, ylabel, seriler):
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    for ad, y, stil in seriler:
        ax.plot(xs, y, stil, label=ad, linewidth=2, markersize=7)
        for x, v in zip(xs, y):
            ax.annotate(f"{v:g}", (x, v), textcoords="offset points",
                        xytext=(0, 7), ha="center", fontsize=8)
    ax.set_xticks(xs)
    ax.set_xticklabels(etiket)
    ax.set_xlabel("Hız (birim/sn)")
    ax.set_ylabel(ylabel)
    ax.set_title(baslik)
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, dosya), dpi=150)
    plt.close(fig)


# 1) Tur suresi
cizgi("grafik_sure.png", "Hıza göre tur süresi", "Süre (sn)", [
    ("Daire", sayi(daire, "sure_s"), "o-"),
    ("Kare (eski kod)", sayi(kare_eski, "sure_s"), "s--"),
    ("Kare (yeni kod)", sayi(kare_yeni, "sure_s"), "^-"),
])

# 2) Konum sapmasi (tur sonu baslangica uzaklik)
cizgi("grafik_sapma.png", "Hıza göre kapanma hatası (konum sapması)",
      "Başlangıca uzaklık (birim)", [
    ("Daire", sayi(daire, "kapanma_hatasi"), "o-"),
    ("Kare (eski kod)", sayi(kare_eski, "kapanma_hatasi"), "s--"),
    ("Kare (yeni kod)", sayi(kare_yeni, "kapanma_hatasi"), "^-"),
])

# 3) Daire yaricap hatasi
fig, ax = plt.subplots(figsize=(6.5, 4.2))
y = sayi(daire, "yaricap_hatasi_max")
ax.bar(xs, y, width=0.5, color="#4472C4")
for x, v in zip(xs, y):
    ax.annotate(f"{v:g}", (x, v), textcoords="offset points",
                xytext=(0, 4), ha="center", fontsize=9)
ax.set_xticks(xs)
ax.set_xticklabels(etiket)
ax.set_xlabel("Hız (birim/sn)")
ax.set_ylabel("En büyük yarıçap hatası (birim)")
ax.set_title("Dairede hıza göre yarıçap hatası")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "grafik_yaricap.png"), dpi=150)
plt.close(fig)

# 4) Kare kose hatasi: eski ve yeni kod
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
w = 0.35
for ax, kolon, baslik in [
        (axes[0], "kose_hatasi_ort_derece", "Ortalama köşe hatası"),
        (axes[1], "kose_hatasi_max_derece", "En büyük köşe hatası")]:
    e = [abs(v) for v in sayi(kare_eski, kolon)]
    n = [abs(v) for v in sayi(kare_yeni, kolon)]
    ax.bar([x - w / 2 for x in xs], e, w, label="Eski kod", color="#C0504D")
    ax.bar([x + w / 2 for x in xs], n, w, label="Yeni kod", color="#4472C4")
    for x, v in zip(xs, e):
        ax.annotate(f"{v:.2f}", (x - w / 2, v), textcoords="offset points",
                    xytext=(0, 3), ha="center", fontsize=8)
    for x, v in zip(xs, n):
        ax.annotate(f"{v:.2f}", (x + w / 2, v), textcoords="offset points",
                    xytext=(0, 3), ha="center", fontsize=8)
    ax.set_xticks(xs)
    ax.set_xticklabels(etiket)
    ax.set_xlabel("Hız (birim/sn)")
    ax.set_title(baslik)
    ax.grid(axis="y", alpha=0.3)
axes[0].set_ylabel("Hata (derece, mutlak değer)")
axes[0].legend()
fig.suptitle("Kare köşe hatası: eski ve yeni kod")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "grafik_kose.png"), dpi=150)
plt.close(fig)

print("Grafikler kaydedildi:", OUT)
for f in sorted(os.listdir(OUT)):
    print(" ", f)
