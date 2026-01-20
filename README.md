# devreyakan Araç Kutusu (OSE) v 0.0.1

**Elektronik mühendisleri, makerlar ve gömülü sistem geliştiricileri için hepsi bir arada açık kaynaklı masaüstü yardımcı yazılımı.**

![Version](https://img.shields.io/badge/version-0.0.1-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11%2B-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Hakkında

**devreyakan Araç Kutusu v2**, günlük elektronik tasarım ve geliştirme süreçlerinde ihtiyaç duyulan hesaplamaları, simülasyonları ve donanım araçlarını tek bir çatı altında toplayan modüler bir uygulamadır.

**PyQt6** ile geliştirilen bu sürüm, **Modüler Eklenti Mimarisi (Tool Manager)** sayesinde, ana çekirdeğe dokunmadan yeni araçların kolayca eklenmesine ve güncellenmesine olanak tanır.

##  Özellikler ve Araçlar

Proje şu an aşağıdaki modülleri ve araçları içermektedir:

### Donanım ve Gömülü Sistem Araçları
* **Hex Uploader:** `avrdude` altyapısını kullanarak AVR tabanlı kartlara (Arduino vb.) derlenmiş hex dosyalarını yükler.
* **Serial Tool:** `pySerial` altyapısını kullanarak seri port iletişimi ve debug arayüzü.
* **ESP Tool:** `esptool` altyapısını kullanarak Espressif çipleri için yardımcı araçlar.
* **Checksum & Bit Tool:** Veri bütünlüğü doğrulama ve bit manipülasyon işlemleri.

###  Simülasyon ve Analiz
* **Circuit Sim:** NumPy tabanlı, Netlist parse edebilen Nodal Analiz (Düğüm Gerilimi) yöntemini kullanan hafif devre simülatörü.
* **Filter Tool:** Aktif ve pasif filtre tasarımları.
* **PID Tool:** Kontrol sistemleri için PID katsayı hesaplayıcı.

### Hesaplayıcılar
* **Komponentler:** Direnç (Renk kodları/SMD), Kapasitör, İndüktör (Coil), NTC, LED.
* **Güç:** Voltaj Regülatörü, Pil Ömrü (Battery Tool).
* **Analog:** OpAmp devreleri, ADC çözünürlük hesapları.
* **RF & Haberleşme:** RF Anten hesapları, QTH (Locator) dönüştürücü.
* **Diğer:** Kablo kesit hesapları, PCB iz genişliği hesaplayıcı, Base Converter (Taban çevirici).



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