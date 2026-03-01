# 🛣️ Araçlar Yol Haritası (Tools Roadmap)

Planlanan ve gelecekte eklenecek araçların listesi. Tamamlanan araçlar ✅ işareti alır.

## 📊 Durum Özeti

| Kategori | Yapılan | Planlanmış | Toplam |
|----------|---------|-----------|--------|
| **Mekanik & Isı** | 4/4 ✅ | - | 4 |
| **Devre Analiz** | 1 | 4 | 5 |
| **Mikro & Yazılım** | 0 | 5 | 5 |
| **Güç Elektronikleri** | 0 | 5 | 5 |
| **Test & Ölçüm** | 0 | 5 | 5 |
| **Veri & İletişim** | 0 | 5 | 5 |
| **Tıbbi Elektronik** | 0 | 4 | 4 |
| **Görüntü İşleme** | 0 | 3 | 3 |
| **Üniversal Araçlar** | 0 | 5 | 5 |
| **Donanım Erişimi** | 0 | 3 | 3 |
| **TOPLAM** | **5** | **39** | **44** |

---

## ✅ Tamamlanan Araçlar (v0.0.2)

### Mekanik & Isı Yönetimi
- [x] **Heat Sink Tool** - Soğutucu seçim ve termal direnç analizi
- [x] **Mechanical Resonance Tool** - Doğal frekans ve rezonans analizi
- [x] **Euler Column Tool** - Kritik yük ve yapısal stabilite
- [x] **Gear Ratio Tool** - Dişli oranı, torque ve güç hesabı

---

## 📋 Planlanmış Araçlar

### 🔌 Devre Analiz & Simülasyon

- [ ] **Fourier Analiz Aracı**
  - Sinyal/frekans spektrumu analizi
  - Harmonik hesaplamaları
  - FFT visualizasyon

- [ ] **İmpedans Hesaplayıcı**
  - RC, RL, RLC devreler
  - Kompleks sayı hesaplamaları
  - Faz açısı

- [ ] **Rezonans Frekansı Aracı**
  - LC devreler
  - Uydu anten tasarımı
  - Q faktörü hesabı

- [ ] **Transmission Line Aracı**
  - İmpedans eşitleme
  - S parametreleri
  - Yansıma katsayısı

- [ ] **Smith Chart Generator**
  - İnteraktif Smith Diyagramı
  - RF tasarımı
  - Dinamik görüntüleme

### 💾 Mikroişlemci & Yazılım

- [ ] **Baud Rate Hesaplayıcı**
  - Seri iletişim hızları
  - Hata oranları
  - Frekans sapması

- [ ] **CAN/I2C/SPI Bus Hesaplayıcı**
  - Protokol parametreleri
  - Timing hesaplamaları
  - Pull-up direnç

- [ ] **Timing Calculator**
  - Mikro kontrol cü zaman dilimleri
  - Clock cycle hesapları
  - Delay kalkulasyonu

- [ ] **Memory Calculator**
  - RAM, Flash, EEPROM yönetimi
  - Adres uzayı haritası
  - Bellek fragmentasyonu

- [ ] **Code Size Estimator**
  - Derlenmiş kod boyutu tahmini
  - İnstruction set analizi
  - Flash kullanımı

### ⚡ Güç Elektronikleri

- [ ] **Boost/Buck Converter**
  - DC-DC dönüştürücü tasarımı
  - Endüktör değeri hesapları
  - Verimlililik analizi

- [ ] **MOSFET/BJT Termal Analiz**
  - Güç tüketimi
  - Isı çıkışı
  - Isınma zamanı

- [ ] **Transformer Hesap**
  - Oran ve güç hesabı
  - Kayıp hesaplamaları
  - L/C değerleri

- [ ] **Power Distribution Aracı**
  - PCB power plane tasarımı
  - Gerilim düşümü analizi
  - Kablo boyutlandırması

- [ ] **Motor Control Aracı**
  - Motor parametreleri
  - PWM hesaplamaları
  - Hız ve torque

### 🧪 Test & Ölçüm

- [ ] **Tolerance Stack-up Aracı**
  - Tolerans analizi (RSS, Lineer)
  - Kümülatif hata
  - Σ hesaplamaları

- [ ] **Measurement Error Propagation**
  - Ölçüm hatası analizi
  - Standart sapma
  - Belirsizlik hesapları

- [ ] **Noise Figure Calculator**
  - RF sistemi gürültü hesabı
  - Amplifikatör kaskat analizi
  - dB hesaplamaları

- [ ] **SNR Calculator**
  - Sinyal-gürültü oranı
  - C/N (taşıyıcı/gürültü)
  - EbNo (bit hatasına karşı)

- [ ] **Dynamic Range Aracı**
  - Test cihazı dinamik aralığı
  - Ölçüm limitleri
  - Hassasiyet analizi

### 📡 Veri & İletişim

- [ ] **CRC Calculator**
  - CRC16/32 kontrol hesaplamaları
  - Polinomial destek
  - Doğrulama

- [ ] **Hamming Code Aracı**
  - Hata düzeltme kodu
  - Kod oluşturma/doğrulama
  - Bit pozisyon analizi

- [ ] **Manchester/NRZ Encoder**
  - Kodlama simulasyonu
  - İşaret gösterimi
  - Zaman diyagramı

- [ ] **IP Subnet Calculator**
  - Ağ hesaplamaları
  - CIDR notasyonu
  - Broadcast adresleri

- [ ] **JSON/YAML Formatter & Validator**
  - Veri formatı düzenleme
  - Syntaks doğrulama
  - CompressUtils/minify

### 🏥 Tıbbi Elektronik

- [ ] **ECG Filter Tasarımcı**
  - EKG sinyal filtreleme
  - 50/60 Hz buzz filter
  - Bant geçiş tasarımı

- [ ] **EMG Amplifikatör Aracı**
  - Kas sinyali amplifikasyonu
  - Kazanç hesabı
  - Bant genişliği

- [ ] **Bio-Impedance Aracı**
  - Biyoelektrik ölçümler
  - İmpedans analizi
  - Frekans yanıtı

- [ ] **SpO2/Pulse Oksimeter Aracı**
  - Oksijen doygunluğu hesapları
  - Nabız hızı analizi
  - Sinyal işleme

### 🎨 Görüntü İşleme

- [ ] **Color Space Converter**
  - RGB/HSV/Lab dönüşümü
  - Renk analizi
  - Görsel gösterim

- [ ] **Image Analyzer**
  - Resim pixel analizi
  - Histogram
  - Görüntü bilgileri

- [ ] **QR/Barcode Generator**
  - Test QR kodu oluşturma
  - Ürün barkodu
  - Kod taraması

### 🔧 Üniversal Araçlar

- [ ] **Comprehensive Unit Converter**
  - Tür/Ünite dönüştürme (dBm, dB, Watts vb.)
  - Sıcaklık, uzunluk, ağırlık
  - Kişisel birim tanımlama

- [ ] **Equation Solver**
  - Formüla çözücü (NumPy ile)
  - Lineer/nonlineer denklemler
  - Grafik gösterimi

- [ ] **Graph Plotter**
  - Matematiksel fonksiyon grafikleri
  - Interactive plotting
  - CSV export

- [ ] **FMEA Tool**
  - Risk & Failure Mode analizi
  - RPN (Risk Priority Number) hesabı
  - Tablo yönetimi

- [ ] **Time Zone Converter**
  - Zaman dilimi dönüştürme
  - DST (Yaz saati) hesapları
  - Harita projeleri için

### 💻 Donanım Erişimi & Benzetme

- [ ] **GPIO Simulator**
  - Virtual GPIO test platformu
  - Pin konfigürasyonu
  - Logic state kontrolü

- [ ] **Logic Analyzer Emulator**
  - Seri sinyalleri analiz etme
  - Protocol decode (I2C, SPI)
  - Timing measurements

- [ ] **Oscilloscope Data Plotter**
  - CSV kayıtlı datadan grafik
  - Rise time, overshoot analizi
  - FFT spektrumu

---

## 📈 Implementasyon Öncelikleri

### 🔴 Hemen (v0.0.3-v0.1.0)
1. **Baud Rate Hesaplayıcı** ⏱️ 1.5 saat
2. **CRC Calculator** ⏱️ 1.5 saat
3. **Comprehensive Unit Converter** ⏱️ 3 saat
4. **Time Zone Converter** ⏱️ 1.5 saat

**Toplam:** 7.5 saat (hafta sonu yapılabilir)

### 🟠 Kısa Vadeli (v0.1.0-v0.2.0)
- IP Subnet Calculator
- JSON/YAML Formatter
- SNR Calculator
- Color Space Converter
- Memory Calculator

### 🟡 Orta Vadeli (v0.2.0-v0.3.0)
- CAN/I2C/SPI Bus Hesaplayıcı
- Impedans Hesaplayıcı
- MOSFET Termal Analiz
- FMEA Tool
- Graph Plotter

### 🟢 Uzun Vadeli (v0.3.0+)
- Smith Chart Generator
- ECG Filter Tasarımcı
- Transmission Line Aracı
- Bio-Impedance Aracı
- Logic Analyzer Emulator

---

## 🎯 İstatistikler

- **Toplam Planlanmış Araç:** 39
- **Tahmini Toplam Süre:** ~120-150 saat
- **Mevcut Araç Sayısı:** 31
- **Hedef Araç Sayısı (v1.0):** 70+

---

## 📝 Yaşam Döngüsü

```
Planlama (Bu liste) 
  ↓
Kod Yazma (✏️ İşlemde)
  ↓
Test & Debug
  ↓
Commit & PR
  ↓
Release (GitHub tags)
  ↓
Belgeler Güncelleme
```

---

**Son Güncelleme:** 1 Mart 2026
**Sorumlu:** Takım
