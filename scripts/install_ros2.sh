#!/usr/bin/env bash
# ROS 2 kurulum betiği (turtlesim dahil)
# Kullanım: ./scripts/install_ros2.sh
#
# Ubuntu sürümüne göre ROS 2 dağıtımı seçilir:
#   Ubuntu 26.04 -> Lyrical Luth
#   Ubuntu 24.04 -> Jazzy Jalisco
#   Ubuntu 22.04 -> Humble Hawksbill
# ROS 2 zaten kuruluysa kurulum atlanır, sadece eksikler tamamlanır.

set -euo pipefail

# ---------- Yardımcı fonksiyonlar ----------
hata() { echo "HATA: $1" >&2; exit 1; }
bilgi() { echo "==> $1"; }

# ---------- 1. Ön koşul kontrolleri ----------
if [ "$(id -u)" -eq 0 ]; then
  hata "Bu betiği root olarak değil, normal kullanıcıyla çalıştırın (gerektiğinde sudo şifre ister)."
fi

[ -r /etc/os-release ] || hata "/etc/os-release bulunamadı. Bu betik sadece Ubuntu içindir."
. /etc/os-release

[ "${ID:-}" = "ubuntu" ] || hata "Bu betik sadece Ubuntu için yazıldı. Sisteminiz: ${ID:-bilinmiyor}"

case "${VERSION_ID:-}" in
  26.04) ROS_DISTRO_ADI="lyrical" ;;
  24.04) ROS_DISTRO_ADI="jazzy" ;;
  22.04) ROS_DISTRO_ADI="humble" ;;
  *) hata "Desteklenmeyen Ubuntu sürümü: ${VERSION_ID:-bilinmiyor}. Desteklenenler: 22.04, 24.04, 26.04." ;;
esac

ARCH="$(dpkg --print-architecture)"
case "$ARCH" in
  amd64|arm64) ;;
  *) hata "Desteklenmeyen mimari: $ARCH (amd64 veya arm64 gerekir)." ;;
esac

command -v sudo >/dev/null 2>&1 || hata "sudo bulunamadı."

bilgi "Ubuntu $VERSION_ID algılandı -> ROS 2 dağıtımı: $ROS_DISTRO_ADI"

# İnternet kontrolü
if ! curl -fsI https://packages.ros.org >/dev/null 2>&1 && ! sudo apt-get update -qq >/dev/null 2>&1; then
  hata "İnternet bağlantısı yok gibi görünüyor. Bağlantınızı kontrol edip tekrar deneyin."
fi

# ---------- 2. Temel paketler ve locale ----------
bilgi "Temel paketler kuruluyor"
sudo apt-get update
sudo apt-get install -y software-properties-common curl locales

sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

bilgi "Universe deposu etkinleştiriliyor"
sudo add-apt-repository -y universe

# ---------- 3. ROS 2 apt deposu ----------
if [ ! -f /opt/ros/"$ROS_DISTRO_ADI"/setup.bash ]; then
  bilgi "ROS 2 apt deposu ekleniyor"
  if ! dpkg -s ros2-apt-source >/dev/null 2>&1; then
    ROS_APT_SOURCE_VERSION="$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')"
    [ -n "$ROS_APT_SOURCE_VERSION" ] || hata "ros-apt-source sürümü alınamadı (GitHub'a erişilemiyor olabilir). Biraz sonra tekrar deneyin."
    curl -fL -o /tmp/ros2-apt-source.deb \
      "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.${UBUNTU_CODENAME:-$VERSION_CODENAME}_all.deb" \
      || hata "ros2-apt-source paketi indirilemedi."
    sudo dpkg -i /tmp/ros2-apt-source.deb
  fi

  # ---------- 4. ROS 2 kurulumu ----------
  bilgi "ROS 2 $ROS_DISTRO_ADI kuruluyor (bu işlem birkaç dakika sürebilir)"
  sudo apt-get update
  sudo apt-get upgrade -y
  sudo apt-get install -y ros-dev-tools "ros-${ROS_DISTRO_ADI}-desktop"
else
  bilgi "ROS 2 $ROS_DISTRO_ADI zaten kurulu, bu adım atlanıyor"
fi

# ---------- 5. turtlesim ----------
bilgi "turtlesim kuruluyor"
sudo apt-get install -y "ros-${ROS_DISTRO_ADI}-turtlesim"

# ---------- 6. Ortam ayarı (.bashrc) ----------
SATIR="source /opt/ros/${ROS_DISTRO_ADI}/setup.bash"
if ! grep -qxF "$SATIR" "$HOME/.bashrc"; then
  bilgi ".bashrc dosyasına ROS 2 ortam ayarı ekleniyor"
  echo "$SATIR" >> "$HOME/.bashrc"
fi

# ---------- 7. Doğrulama ----------
bilgi "Kurulum doğrulanıyor"
set +u
# shellcheck disable=SC1090
. "/opt/ros/${ROS_DISTRO_ADI}/setup.bash"
set -u

command -v ros2 >/dev/null 2>&1 || hata "ros2 komutu bulunamadı. Kurulum tamamlanmamış olabilir."
ros2 pkg list | grep -qx turtlesim || hata "turtlesim paketi bulunamadı."

echo
echo "Kurulum tamam."
echo "ROS_DISTRO : $ROS_DISTRO_ADI"
echo "Deneme için yeni bir terminal açıp şunu yazın:  ros2 run turtlesim turtlesim_node"
