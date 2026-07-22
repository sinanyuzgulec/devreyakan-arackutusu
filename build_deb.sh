#!/usr/bin/env bash
# ==============================================================================
# devreyakan Araç Kutusu - Otomatik .deb Paketi Üretici Script
# ==============================================================================

set -e

PKG_NAME="devreyakan-arackutusu"
VERSION="${RELEASE_VERSION:-0.0.3}"
# Baştaki 'v' harfini kaldır (v0.0.3 -> 0.0.3)
VERSION="${VERSION#v}"
ARCH="all"
BUILD_DIR="build_deb"
OUTPUT_DEB="${PKG_NAME}_${VERSION}_${ARCH}.deb"

echo "=== 📦 .deb Paketi Oluşturuluyor: ${OUTPUT_DEB} ==="

# 1. Temizlik ve Klasör Yapısı Oluşturma
rm -rf "$BUILD_DIR"
rm -f "$OUTPUT_DEB"

mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/usr/share/$PKG_NAME"
mkdir -p "$BUILD_DIR/usr/bin"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/pixmaps"

# 2. Control Dosyası Yazma (Paket Metadata)
cat <<EOF > "$BUILD_DIR/DEBIAN/control"
Package: $PKG_NAME
Version: $VERSION
Architecture: $ARCH
Maintainer: Sinan Yüzgüleç
Depends: python3, python3-pyqt6, python3-numpy, python3-serial
Section: utils
Priority: optional
Homepage: https://github.com/sinanyuzgulec/devreyakan-arackutusu
Description: Elektronik mühendisleri ve gömülü sistem geliştiricileri için hepsi bir arada araç kutusu.
 Modüler yapısı ile 37+ hesaplama ve donanım aracı içerir.
EOF

# 3. Proje Dosyalarını Kopyalama (.git, venv ve temp dosyalar hariç)
echo "--> Proje dosyaları kopyalanıyor..."
cp -r core gui localization tools *.py requirements.txt README.md signatures.json "$BUILD_DIR/usr/share/$PKG_NAME/" 2>/dev/null || true

# 4. /usr/bin Başlatıcı Scripti Oluşturma
cat <<EOF > "$BUILD_DIR/usr/bin/$PKG_NAME"
#!/bin/sh
exec python3 /usr/share/$PKG_NAME/main.py "\$@"
EOF
chmod +x "$BUILD_DIR/usr/bin/$PKG_NAME"

# 5. Masaüstü Kısayolu (.desktop) Oluşturma
cat <<EOF > "$BUILD_DIR/usr/share/applications/$PKG_NAME.desktop"
[Desktop Entry]
Name=devreyakan Araç Kutusu
Comment=Elektronik ve Gömülü Sistem Yardımcı Yazılımı
Exec=/usr/bin/$PKG_NAME
Icon=$PKG_NAME
Terminal=false
Type=Application
Categories=Development;Engineering;Electronics;
EOF

# 6. Paketleme Yapma (dpkg-deb)
echo "--> dpkg-deb çalıştırılıyor..."
dpkg-deb --build --root-owner-group "$BUILD_DIR" "$OUTPUT_DEB"

# 7. Temizlik
rm -rf "$BUILD_DIR"

echo "=== ✅ BAŞARILI: ${OUTPUT_DEB} dosyası oluşturuldu! ==="
echo "Kurmak için: sudo dpkg -i ${OUTPUT_DEB}"
