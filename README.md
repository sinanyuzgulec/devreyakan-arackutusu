# devreyakan Araç Kutusu (OSE) v 0.0.2

**Elektronik mühendisleri, makerlar ve gömülü sistem geliştiricileri için hepsi bir arada açık kaynaklı masaüstü yardımcı yazılımı.**

![Version](https://img.shields.io/badge/version-0.0.1-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Hakkında

**devreyakan Araç Kutusu (OSE)**, günlük elektronik tasarım ve geliştirme süreçlerinde ihtiyaç duyulan hesaplamaları, simülasyonları ve donanım araçlarını tek bir çatı altında toplayan modüler bir uygulamadır.

**PyQt6** ile geliştirilen bu sürüm, **Modüler Eklenti Mimarisi (Tool Manager)** sayesinde, ana çekirdeğe dokunmadan yeni araçların kolayca eklenmesine ve güncellenmesine olanak tanır.

##  Özellikler ve Araçlar

Proje **31+ modüler araç** içermektedir. Aşağıtta kategori bazında araçlar listelenmiştir:

### 📊 Tüm Araçlar

| # | Araç Adı | Kategori | Açıklama |
|---|----------|----------|----------|
| 1 | **ADC Adım Hesaplayıcı** | Analog | ADC çözünürlük ve dijital değer hesaplamaları |
| 2 | **Op-Amp Kazanç Hesaplayıcı** | Analog | Operasyonel amplifikatör kazanç ve devreleri |
| 3 | **Taban Dönüştürücü** | Matematik | Sayısal sistemler arası dönüşüm (2, 8, 10, 16) |
| 4 | **Pil Ömrü Aracı** | Güç | Pil kapasitesi ve çalışma süresi hesaplamaları |
| 5 | **LM317 Regülatör Hesaplayıcı** | Güç | Voltaj regülatörü tasarımı ve hesapları |
| 6 | **Seri Port İzleyici** | Gömülü Sistem | Seri port iletişimi ve debug arayüzü |
| 7 | **ESP Tool** | Gömülü Sistem | Espressif çipleri için yardımcı araçlar |
| 8 | **Hex Uploader** | Gömülü Sistem | AVR karalar için hex dosyası yükleme (avrdude) |
| 9 | **Struct Bitfield Analizcisi** | Veri | Bitfield ve maskeleme işlemleri |
| 10 | **Struct Analizcisi** | Veri | Veri yapısı analizi ve boyut hesaplamaları |
| 11 | **Bobin Hesaplayıcı** | Komponent | İndüktör (Coil) hesaplamaları |
| 12 | **LED Direnç Hesaplayıcı** | Komponent | LED seri direnç ve güç hesapları |
| 13 | **NTC Termistör Hesaplayıcı** | Komponent | NTC sıcaklık sensörü hesaplamaları |
| 14 | **Direnç Renk Bulucu** | Komponent | Direnç renk kodları ve SMD değerleri |
| 15 | **SMD Kod Bulucu** | Komponent | SMD bileşen kodları ve değerleri |
| 16 | **LCD Karakter Çizici** | Komponent | LCD display karakter sürücü |
| 17 | **Ohm Yasası Hesaplayıcı** | Elektrik | Voltaj, akım, direnç ve güç hesaplamaları |
| 18 | **Kablo Kesit Hesaplayıcı** | Elektrik | Kablo çapı ve kesit alanı hesapları |
| 19 | **Devre Simülatörü** | Simülasyon | NumPy tabanlı Nodal Analiz devre simülasyonu |
| 20 | **RC Filtre Tasarımcısı** | Simülasyon | Aktif/pasif RC filtre tasarımı |
| 21 | **PID Kontrolcü Hesaplayıcı** | Kontrol | PID katsayı ve sistem yanıt hesaplamaları |
| 22 | **PCB Yol Genişliği Hesaplayıcı** | Tasarım | PCB iz akım taşıma kapasitesi |
| 23 | **RF Anten Hesaplayıcı** | RF | RF anten boyutu ve frekans hesapları |
| 24 | **QTH Locator Dönüştürücü** | RF | Koordinat ve QTH locator dönüşümü |
| 25 | **Soğutucu Seçim Aracı** | Isı Yönetimi | Termal direnç ve heat sink seçimi |
| 26 | **Mekanik Rezonans Tarayıcı** | Mekanik | Doğal frekans ve sönümleme analizi |
| 27 | **Euler Kolon Analizi** | Mekanik | Kritik yük ve yapısal stabilite |
| 28 | **Dişli Oranı Hesaplayıcı** | Mekanik | Dişli oranı, torque ve güç hesabı |
| 29 | **555 Zamanlayıcı Hesaplayıcı** | Elektronik | 555 timer frekans ve görev döngüsü |
| 30 | **Sistem Araçları** | Sistem | Sistem bilgileri ve konfigürasyon |
| 31 | **Veri Bütünlüğü Aracı** | Veri | Checksum ve veri doğrulama |



## Kurulum

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

### Ön Gereksinimler
* Python 3.10 veya üzeri
* `avrdude` (Hex yükleyici modülü için sistem yolunda (PATH) bulunmalıdır)

### Adım Adım Kurulum

1.  **Depoyu klonlayın:**
    ```bash
    git clone [https://github.com/sinanyuzgulec/devreyakan-arackutusu.git](https://github.com/sinanyuzgulec/devreyakan-arackutusu.git)
    cd arackutusu
    ```

2.  **Sanal ortam oluşturun (Önerilen):**
    ```bash
    python -m venv venv
    # Windows için:
    venv\Scripts\activate
    # Linux/Mac için:
    source venv/bin/activate
    ```

3.  **Bağımlılıkları yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Not: `requirements.txt` dosyanız yoksa temel bağımlılıklar: `PyQt6`, `numpy`, `pyserial`)*

4.  **Uygulamayı başlatın:**
    ```bash
    python main.py
    ```
    *(Veya giriş noktanız `/gui/main_window.py` ise ilgili dosya)*

## Yol Haritası

Projenin bir sonraki ana hedefi (v2.1), mevcut masaüstü (PyQt6) mimarisini koruyarak tüm araçları Web arayüzü ve REST API üzerinden de erişilebilir hale getirmektir.

### Mimari & Çekirdek (Web Adaptasyonu)
- [ ] **Core Abstraction Layer:** Araçların `ui.py` (GUI) bağımlılıklarını `logic.py` (Mantık) katmanından tamamen izole etmek.
- [ ] **Input Schema Registry:** Her aracın giriş parametrelerini (Tip, Range, Default, Label) tanımlayan standart bir şema yapısı (JSON-Schema benzeri) oluşturmak.
- [ ] **Web Server API:** `/core/web_server.py` modülü altında araçları listeleyen ve çalıştıran REST endpoint'lerini (`POST /api/run/<tool_id>`) yazmak.
- [ ] **Headless Tool Manager:** `PyQt6` kütüphanesi yüklü olmasa bile sunucu ortamında araçları tarayıp yükleyebilen yeni bir modül yükleyici geliştirmek.
- [ ] **Tool UI Improvement:** Araç UI'larının grafiksel olarak zenginleştirilmesi.

### Araçların Dönüşümü
- [ ] **Logic Refactoring:** Tüm araçların hesaplama çekirdeklerini `WebExposable` arayüzüne uyarlamak.
- [ ] **Data Serialization:** Karmaşık çıktıların (NumPy dizileri, Matplotlib grafikleri vb.) JSON formatında serileştirilmesi için adaptörler yazmak.

### Web Frontend (Hedeflenen)
- [ ] **Dynamic Form Generator:** API'den gelen şemaya göre HTML inputlarını (Select, Slider, Text) otomatik üreten JS motoru.
- [ ] **Unified Result Viewer:** Hesaplama sonuçlarını, logları ve grafikleri tek bir standart formatta gösteren web bileşeni.

### Eklenecek Yeni Araçlar
- [ ] **Bode Plotter:** Frekans cevabı analizi için grafik aracı.
- [ ] **Logic Analyzer Client:** Mantık analizörü donanımları için arayüz.
- [ ] **Unit Converter:** Mühendislik birimleri arası kapsamlı dönüştürücü.

## Geliştirici Kılavuzu (Modüler Yapı)

Bu proje dinamik bir **Tool Manager** yapısı kullanır. Yeni bir araç eklemek için:

1.  `/tools/` dizini altında aracınız için yeni bir klasör oluşturun (örn: `my_new_tool`).
2.  Klasör içine `__init__.py`, `ui.py` (Arayüz) ve `logic.py` (Mantık) dosyalarını ekleyin.
3.  Tool Manager, başlangıçta bu klasörü otomatik olarak tarar ve menüye ekler.

### Dosya Yapısı Örneği
```text
/
├── core/             # Çekirdek modüller (Updater, Localization, ToolManager)
├── gui/              # Ana pencere ve genel widget'lar
├── localization/     # Dil dosyaları (tr.json, en.json)
└── tools/            # Dinamik araçlar klasörü
    ├── circuit_sim/  # Örnek: Devre simülatörü modülü
    ├── uploader_tool/ # Örnek: Hex yükleyici
    └── ...
