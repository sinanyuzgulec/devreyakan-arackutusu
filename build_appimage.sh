#!/usr/bin/env bash
# AppImage paketleme scripti (appimagetool & python-appimage kullanarak)

set -e

APP_NAME="devreyakan-arackutusu"
VERSION="${RELEASE_VERSION:-0.0.4}"
VERSION="${VERSION#v}"
APP_DIR="AppDir"
OUTPUT_APPIMAGE="${APP_NAME}_${VERSION}-x86_64.AppImage"

echo "Building AppImage..."

rm -rf "$APP_DIR" "$OUTPUT_APPIMAGE"
mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/share/$APP_NAME"

# Dosyalari kopyala
cp -r core gui localization tools *.py requirements.txt signatures.json "$APP_DIR/usr/share/$APP_NAME/" 2>/dev/null || true

# AppRun scripti
cat <<EOF > "$APP_DIR/AppRun"
#!/bin/sh
HERE="\$(dirname "\$(readlink -f "\${0}")")"
export PATH="\$HERE/usr/bin:\$PATH"
export PYTHONPATH="\$HERE/usr/share/$APP_NAME:\$PYTHONPATH"
exec python3 "\$HERE/usr/share/$APP_NAME/main.py" "\$@"
EOF
chmod +x "$APP_DIR/AppRun"

# Desktop dosyasi
cat <<EOF > "$APP_DIR/$APP_NAME.desktop"
[Desktop Entry]
Name=devreyakan Araç Kutusu
Exec=AppRun
Icon=icon
Type=Application
Categories=Development;Electronics;
EOF

# Gecici icon
touch "$APP_DIR/icon.png"

# appimagetool derle/çalıştır
if [ -d "squashfs-root" ]; then
    ARCH=x86_64 ./squashfs-root/AppRun "$APP_DIR" "$OUTPUT_APPIMAGE"
elif command -v appimagetool >/dev/null 2>&1; then
    ARCH=x86_64 appimagetool "$APP_DIR" "$OUTPUT_APPIMAGE"
else
    echo "Downloading appimagetool..."
    curl -sL "https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage" -o appimagetool
    chmod +x appimagetool
    ./appimagetool --appimage-extract
    ARCH=x86_64 ./squashfs-root/AppRun "$APP_DIR" "$OUTPUT_APPIMAGE"
fi

rm -rf "$APP_DIR"
echo "AppImage created: $OUTPUT_APPIMAGE"
