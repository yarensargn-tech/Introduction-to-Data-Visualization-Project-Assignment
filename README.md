# GRID-STRESS · Akıllı Şebeke Stres Analiz Sistemi

> **Smart Grid Stress Analysis System** — Veri Görselleştirme Dersi Projesi
>
> Elektrik şebekesi operasyon merkezleri için gerçek zamanlı izleme, stres analizi
> ve **Ollama LLM** destekli karar destek sistemi.

---

## 🎯 Ne Yapar?

Bu sistem, elektrik şebekesi operatörlerinin günlük olarak karşılaştığı bir
problemi çözer: **şebekenin hangi noktasının ne kadar stres altında olduğunu
anlamak ve doğru anda doğru kararı vermek.**

Sistem, 10 trafo merkezi ve 12 iletim hattından oluşan Türkiye benzeri bir
şebekeyi gerçek zamanlı simüle eder. Her saniye:

- Her bileşenin **yük, gerilim, sıcaklık ve frekansını** takip eder
- Çok faktörlü bir **stres skoru** (0-100) hesaplar
- Anomalileri otomatik tespit eder
- **Ollama LLM** ile operatöre Türkçe, profesyonel öneriler sunar
- Operatör doğal dilde sistem hakkında soru sorabilir

---

## 🧩 Çözülen Gerçek Problem

**Problem:** Şebeke operatörleri yüzlerce sensörden gelen veriyi izlemek zorunda.
Aşırı yük, gerilim sapması, sıcaklık artışı gibi durumların hangi bileşenlerde
ne anlama geldiğini ayırt etmek hem teknik bilgi hem hızlı reaksiyon gerektirir.
Yanlış bir karar, geniş alanlı elektrik kesintisine (blackout) neden olabilir.

**Çözüm:** GRID-STRESS, bütün şebeke verisini tek bir kontrol odası arayüzünde
toplar, çok boyutlu stres analizi yapar ve LLM tabanlı bir AI danışman ile
**operatörün anlayacağı dilde** öneriler sunar.

---

## 🏗️ Mimari

```
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER (Dashboard UI)                   │
│   Harita · Grafikler · Stres Göstergesi · Sohbet · Tablo   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON (her 2 sn)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                       FLASK API                             │
│   /api/grid/snapshot · /api/llm/* · /api/anomalies · ...    │
└────────┬───────────────┬───────────────┬──────────┬─────────┘
         │               │               │          │
         ▼               ▼               ▼          ▼
   ┌─────────┐    ┌──────────┐    ┌──────────┐  ┌────────┐
   │  Grid   │    │  Stress  │    │   LLM    │  │  Data  │
   │  Sim.   │───▶│ Analyzer │    │ Advisor  │  │ Logger │
   └─────────┘    └──────────┘    └─────┬────┘  └────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │   OLLAMA (yerel) │
                               │  llama3.2 / vs.  │
                               └──────────────────┘
```

---

## 🚀 Kurulum

### 1. Gereksinimler

- **Python 3.9+**
- **Ollama** kurulu ve bir model yüklenmiş olmalı
  - İndir: https://ollama.com/download
  - Önerilen model: `ollama pull llama3.2` (3B - hızlı) veya `ollama pull gemma2:2b`

### 2. Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### 3. Ollama servisini başlat

Yeni bir terminalde:

```bash
ollama serve
```

Servisin çalışıp çalışmadığını kontrol etmek için:

```bash
curl http://localhost:11434/api/tags
```

### 4. Uygulamayı çalıştır

```bash
python app.py
```

Tarayıcıdan `http://localhost:5000` adresine gidin.

---

## 🎛️ Kullanım

### Dashboard Bileşenleri

| Bölüm | İşlev |
|-------|-------|
| **Stres Skoru (sol üst)** | 0-100 arası genel sistem stres göstergesi |
| **Anlık Metrikler** | Toplam yük, üretim, frekans, gerilim, kayıplar |
| **Senaryo Testi** | Kış pik / yaz pik / hat arızası simülasyonları |
| **Şebeke Topolojisi (orta)** | Türkiye haritası üzerinde gerçek zamanlı şebeke |
| **Stres & Yük Trend** | Zaman içinde stres ve yük grafiği |
| **AI Danışman (sağ üst)** | LLM otomatik önerileri (30 sn'de bir yenilenir) |
| **Olay Kayıtları** | Tespit edilen anomaliler |
| **Operatör Asistanı** | LLM ile sohbet — "İstanbul'daki yük kritik mi?" gibi sorular |
| **Trafo Tablosu (alt)** | Tüm 10 trafo merkezinin durum kartları |

### Özellikler

#### 1. Gerçek zamanlı izleme
Her 2 saniyede sistem güncellenir. Trafolar yüke göre **yeşil/sarı/kırmızı** renge boyanır.

#### 2. Senaryo testleri
Sağ üst panelden farklı senaryolar tetiklenebilir:
- **Kış pik yükü** — %35 yük artışı
- **Yaz klima yükü** — %45 artış (Antalya'da daha sert)
- **Hat arızası** — Kocaeli-Ankara hattı devre dışı
- **Üretim kaybı** — Frekans düşüşü ve kompansasyon

#### 3. Manüel stres uygulama
Herhangi bir trafo merkezine tıklayın → modal açılır → istediğiniz yükü, istediğiniz süre kadar uygulayın.

#### 4. LLM destekli analiz
- **Otomatik öneri**: Sistem her 30 saniyede yeni öneri üretir
- **Bileşen analizi**: Bir trafoya tıklayın, AI o bileşene özel risk değerlendirmesi yapar
- **Sohbet**: Türkçe doğal dilde soru sorabilirsiniz: 
  - "Hangi trafo en riskli durumda?"
  - "Yük dağılımını nasıl optimize edebilirim?"
  - "Frekans neden 50 Hz'in altında?"

---

## 📊 Stres Skoru Nasıl Hesaplanır?

Her bileşen için 4 ana faktör değerlendirilir:

```
Stres = max(0.6 × en_yüksek_faktör + 0.4 × ortalama_faktör)

Faktörler:
├── Yük Stresi    (yük%, eşikler: 80, 95)
├── Gerilim Stresi  (yüke bağlı düşüş)
├── Sıcaklık Stresi (eşikler: 65°C, 80°C)
└── Frekans Stresi  (sapma: ±0.2, ±0.5 Hz)
```

Sistem genel stresi:

```
Genel Stres = ortalama(bileşen_stresleri) × 0.4 
            + max(bileşen_stresleri) × 0.4 
            + frekans_stresi × 0.2
```

**Seviyeler:**
- 🟢 **Düşük (0-30)**: Normal çalışma
- 🟡 **Orta (30-50)**: Dikkat
- 🟠 **Yüksek (50-75)**: Müdahale gerekli
- 🔴 **Kritik (75-100)**: Acil eylem

---

## 🤖 Ollama Entegrasyonu Detayı

LLM, sisteme şu bilgilerle beslenir:

1. **Sistem yönergesi (system prompt)**: TEİAŞ seviyesi operasyon danışmanı rolü
2. **Anlık şebeke özeti**: Yük, frekans, kritik bileşenler vs.
3. **Operatör sorusu / context**

LLM şu şekilde yanıt verir:
- Mevcut durum özeti (1 cümle)
- Riskler (1-2 cümle)
- Somut öneriler (1-2 madde)

Modeli değiştirmek için:

```bash
export OLLAMA_MODEL=mistral   # veya gemma2, qwen2.5, vs.
python app.py
```

---

## 📁 Proje Yapısı

```
smart_grid_stress_analyzer/
├── app.py                    # Ana Flask uygulaması
├── requirements.txt          # Python bağımlılıkları
├── README.md                 # Bu dosya
├── modules/
│   ├── grid_simulator.py     # Şebeke simülasyonu
│   ├── stress_analyzer.py    # Stres skoru hesaplama
│   ├── llm_advisor.py        # Ollama entegrasyonu
│   └── data_logger.py        # Tarihsel veri & istatistik
├── templates/
│   └── index.html            # Dashboard arayüzü
└── static/
    ├── css/
    │   └── style.css         # Kontrol odası teması
    └── js/
        └── main.js           # Frontend logic
```

---

## 🎨 Tasarım Felsefesi

Arayüz, gerçek bir **şebeke kontrol odası** estetiği üzerine inşa edildi:

- **Karanlık tema**: 7/24 izleme yapan operatörlerin gözünü yormayan koyu renkler
- **Monospace tipografi (JetBrains Mono)**: Teknik veriler için netlik
- **Display fontu (Syne)**: Başlıklar ve büyük sayılar için karakter
- **Renk kodlaması**: Tüm sistem genelinde tutarlı (yeşil=normal, sarı=uyarı, kırmızı=kritik)
- **Yüksek bilgi yoğunluğu**: Tek ekranda kontrol odasında ihtiyaç duyulan tüm veriler

---

## 🔧 Genişletme Fikirleri

1. **Gerçek SCADA bağlantısı**: Modbus/IEC-61850 üzerinden gerçek sensör verileri
2. **ML tahmini**: Yük tahmini için LSTM modeli ekle
3. **Çok kullanıcılı operatör paneli**: WebSocket ile gerçek zamanlı çoklu kullanıcı
4. **PDF rapor üretimi**: Vardiya sonu otomatik özet raporu
5. **Mobil bildirim**: Kritik anomali için SMS/push bildirim
6. **Veritabanı**: PostgreSQL + TimescaleDB ile uzun vadeli analiz

---

## ⚠️ Bilinen Sınırlamalar

- Veriler **simülasyondur** — gerçek SCADA entegrasyonu yok
- LLM yanıtları model kalitesine bağlı (3B model hızlı ama kısıtlı, 7B+ önerilir)
- Frontend `localStorage` kullanmaz — sayfa yenilendiğinde sohbet sıfırlanır

---

## 📜 Lisans

Akademik amaçlı geliştirilmiştir. Ders projesi.

---

## 👤 İletişim

Veri Görselleştirme dersi projesi · 2026

## Mermaid Kodu

flowchart TB

UI[Dashboard UI]
API[Flask API]

SIM[Grid Simulator]
ANALYZER[Stress Analyzer]
ANOM[Anomaly Detector]
LOG[Data Logger]

LLM[LLM Advisor]
MODEL[Ollama Model]

UI --> API

API --> SIM
SIM --> ANALYZER
ANALYZER --> ANOM
ANOM --> API

ANALYZER --> API

SIM --> LOG
ANALYZER --> LOG

API --> LLM
LLM --> MODEL
MODEL --> LLM
LLM --> API

API --> UI
