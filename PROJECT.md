# devreyakan Araç Kutusu - Proje Özeti

## 📋 Genel Bilgi

**devreyakan Araç Kutusu** (OSE), elektronik mühendisleri, makerlar ve gömülü sistem geliştiricileri için geliştirilmiş **hepsi bir arada açık kaynaklı masaüstü yardımcı yazılımı**'dır.

- **Versiyon:** 0.0.1
- **Lisans:** MIT
- **Python Versiyonu:** 3.10+
- **GUI Framework:** PyQt6 6.10.2

## 🎯 Amaç

Elektronik tasarım ve geliştirme süreçlerinde ihtiyaç duyulan hesaplamaları, simülasyonları ve donanım araçlarını tek bir çatı altında toplayan modüler bir uygulama sağlamak.

## 🏗️ Proje Mimarisi

### Temel Bileşenler

```
devreyakan-arackutusu/
├── main.py                 # Ana giriş noktası
├── config.json            # Uygulama yapılandırması
├── core/                  # Temel modüller
│   ├── tool_manager.py    # Araç yönetim sistemi (Plugin mimarisi)
│   ├── integrity.py       # Veri bütünlüğü kontrolü
│   ├── localization.py    # Dil ve yerelleştirme
│   ├── updater.py         # Güncelleme yöneticisi
│   ├── version.py         # Versiyon yönetimi
│   └── web_server.py      # Web sunucusu
├── gui/                   # Kullanıcı arayüzü
│   ├── main_window.py     # Ana pencere
│   ├── settings_page.py   # Ayarlar sayfası
│   └── widgets/           # UI bileşenleri
├── tools/                 # 30+ araç modülü (Plugin sistemi)
├── localization/          # Dil dosyaları (EN, TR)
└── generate_signatures.py # İmza dosyası oluşturuyici
```

## 🔧 Araç Kategorileri (30+ Araç)

### 1. **Donanım ve Gömülü Sistem Araçları**
- **Hex Uploader:** AVR tabanlı kartlara (Arduino vb.) hex yükleme
- **Serial Tool:** Seri port iletişimi ve debug
- **ESP Tool:** Espressif çipleri için yardımcı araçlar
- **System Tool:** Sistem bilgileri

### 2. **Simülasyon ve Analiz**
- **Circuit Sim:** Nodal Analiz yöntemi (NumPy tabanında)
- **Filter Tool:** Aktif/pasif filtre tasarımı
- **PID Tool:** PID katsayı hesaplayıcı
- **OpAmp Tool:** Operasyonel amplifikatör devreleri

### 3. **Komponent Hesaplayıcıları**
- **Resistor Tool:** Direnç renk kodları & SMD
- **SMD Tool:** SMD bileşen bilgileri
- **Battery Tool:** Pil ömrü hesapları
- **LED Tool:** LED parametreleri
- **Capacitor/Coil:** Kapasitör & İndüktör
- **NTC Tool:** NTC termistör hesapları

### 4. **Güç ve Elektrik**
- **Regulator Tool:** Voltaj regülatörleri
- **ADC Tool:** ADC çözünürlük hesapları
- **Cable Tool:** Kablo kesit hesapları
- **Ohm Tool:** Ohm yasası hesaplamaları

### 5. **Harita ve RF**
- **RF Antenna Tool:** RF anten hesapları
- **QTH Tool:** Locator dönüştürücü
- **Circuit Sim:** Devre simülasyonu

### 7. **Mekanik ve Isı Yönetimi** ⭐ YENİ
- **Heat Sink Tool:** Soğutucu seçim ve termal direnç analizi
- **Mechanical Resonance Tool:** Doğal frekans ve rezonans analizi
- **Euler Column Tool:** Kolon kritik yük ve stabilite analizi
- **Gear Ratio Tool:** Dişli oranı ve moment hesaplamaları

### 8. **Tasarım Araçları**
- **PCB Tool:** PCB iz genişliği hesaplayıcı
- **Base Converter:** Taban çevirici
- **Checksum Tool:** Veri bütünlüğü doğrulama
- **Bit Tool:** Bit manipülasyon işlemleri
- **Struct Tool:** Veri yapısı analizi
- **Timer 555 Tool:** 555 Timer hesapları

## 🎨 Teknik Stack

### Bağımlılıklar
```
numpy==2.4.1           # Sayısal hesaplamalar & simülasyonlar
PyQt6==6.10.2         # GUI framework
pyserial==3.5         # Seri port iletişimi
```

### Tool Sayısı
- **Toplam:** 34+ modüler araç (4 yeni araç eklendi)
- **Kategoriler:** 10+ (Mekanik ve Isı Yönetimi kategorileri eklendi)

### İç Modüller
- **Tool Manager:** Dinamik araç yükleme ve eklenti mimarisi
- **Integrity Manager:** Veri doğrulama ve imza kontrolü
- **Localization:** Çok dilli destek (TR, EN)
- **Updater:** Otomatik güncelleme sistemi

## 📦 Modüler Eklenti Mimarisi

Proje **Tool Manager** sayesinde yeni araçları kolayca ekleyebilir:

```
tools/new_tool/
├── __init__.py         # Araç tanımı
├── logic.py           # İş mantığı
└── ui.py              # Kullanıcı arayüzü
```

Her araç otomatik olarak keşfedilir ve ana uygulamaya eklenir.

## 🌍 Yerelleştirme

- **Türkçe (TR):** Tam destek
- **İngilis (EN):** Tam destek
- Yeni diller kolayca eklenebilir (`localization/` klasöründe JSON dosyaları)

## 🚀 Başlangıç

```bash
# Gereksinimler yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
python main.py
```

Ek olarak **avrdude**, Hex Uploader modülü için sistem PATH'inde bulunmalıdır.

## 🔐 Güvenlik Özellikleri

- İmza tabanlı bütünlük kontrolü (`integrity.py`)
- İmza dosyası yönetimi (`signatures.json`)
- Veri doğrulama mekanizması

## 📝 Yapılandırma

`config.json` dosyasında uygulama ayarları yapılandırılır:
- Tema ve görünüm
- Varsayılan dil
- Araç ayarları

## 📄 Dosya Ağacı Özeti

| Bileşen | Açıklama |
|---------|----------|
| **core/** | Temel kütüphaneler ve altyapı |
| **gui/** | PyQt6 tabanlı kullanıcı arayüzü |
| **tools/** | 30+ modüler araç |
| **localization/** | Dil ve yerelleştirme dosyaları |
| **main.py** | Uygulama başlangıç noktası |
| **config.json** | Uygulama yapılandırması |
| **requirements.txt** | Python bağımlılıkları |

## 🤝 Katkı Sağlama

Yeni araçlar eklemek için:
1. `tools/` klasöründe yeni bir klasör oluşturun
2. `logic.py` (iş mantığı) ve `ui.py` (arayüz) yazın
3. ToolManager otomatik olarak araçı keşfedecektir

## 📊 Proje Özellikleri

- ✅ Modüler eklenti mimarisi
- ✅ 30+ önceden yüklenmiş araç
- ✅ Çok dilli destek (TR/EN)
- ✅ Dinamik araç keşfi
- ✅ Bütünlük kontrolü
- ✅ Otomatik güncelleme sistemi
- ✅ Modern PyQt6 UI

## 📄 Lisans

MIT License - Özgür ve açık kaynak

---

**Son Güncelleme:** Mart 2026
**Versiyon:** 0.0.1
