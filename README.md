# Kişisel Finans Yönetimi

Gelir ve gider kayıtlarını takip etmek, dönemsel durumunu görmek ve kayıtları dışa aktarmak için hazırlanmış Streamlit tabanlı kişisel finans uygulaması.

Uygulama Python ile geliştirilmiştir. İşlemler yerel SQLite veritabanında saklanır; arayüz tarayıcıda Streamlit tarafından sunulur.

## Özellikler

- Gelir ve gider işlemi ekleme, düzenleme ve silme
- Tutar ve açıklama için temel giriş kontrolleri
- İşlemleri tür, kategori ve tarih aralığına göre filtreleme
- Filtrelenmiş işlem listesini görüntüleme
- CSV ve Excel (.xlsx) dosyası olarak dışa aktarma
- Dashboard üzerinde toplam gelir, toplam gider, bakiye ve işlem sayısını görme
- Gelir-gider karşılaştırma grafiği
- Kategori bazında gider grafiği
- Aylara göre gelir, gider ve bakiye analizi

## Kullanılan teknolojiler

- **Python** — uygulamanın programlama dili
- **Streamlit** — web arayüzü ve etkileşimli bileşenler
- **SQLite** — işlemleri yerel dosyada saklayan veritabanı
- **pandas** — işlem verilerini tablo, filtre ve analiz için işleme
- **openpyxl** — Excel dosyası oluşturma

## Proje yapısı

```text
Kisisel_finans/
├── app.py                    # Streamlit uygulamasının başlangıç noktası
├── finance.db                # Uygulama çalışınca oluşturulan yerel veritabanı
├── requirements.txt          # Python paketleri
├── finance_app/
│   ├── database.py           # SQLite bağlantısı ve kayıt işlemleri
│   ├── helpers.py            # Veri dönüştürme, filtreleme ve doğrulama
│   └── ui/
│       ├── sidebar.py        # Kenar çubuğu filtreleri
│       ├── transactions.py   # İşlem formları ve işlem listesi
│       ├── dashboard.py      # Özet kartları ve karşılaştırma grafiği
│       └── analytics.py      # Kategori ve aylık analizler
└── README.md
```

## Gereksinimler

- Python 3
- `pip`

Bağımlılık paketleri `requirements.txt` dosyasında listelenmiştir.

## Kurulum

### Windows (PowerShell)

Proje klasörüne geçin ve sanal ortam oluşturun:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Gerekli paketleri yükleyin:

```powershell
pip install -r requirements.txt
```

### macOS veya Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Uygulamayı çalıştırma

Sanal ortam etkinken, proje klasöründe uygulamayı başlatın:

```bash
streamlit run app.py
```

Streamlit uygulamayı başlatır ve tarayıcıda açılabilecek yerel bir adres gösterir.

## Ödev sunumu için örnek akış

Sunumda gerçek finans bilgilerinizi kullanmayın. Beklenen toplamların kolayca görülebilmesi için boş veritabanıyla açılan ayrı bir proje kopyasında şu üç örnek işlemi ekleyin. Tarihleri aynı ay içinde seçin:

| Tür | Kategori | Tutar | Açıklama |
| --- | --- | ---: | --- |
| Gelir | Maaş | 50.000 TL | Örnek maaş |
| Gider | Yemek | 1.200 TL | Örnek market alışverişi |
| Gider | Ulaşım | 600 TL | Örnek ulaşım gideri |

Ardından şu akışı gösterin:

1. **Dashboard:** Toplam gelir 50.000 TL, toplam gider 1.800 TL, bakiye 48.200 TL ve işlem sayısı 3 olmalı.
2. **İşlemler:** Kayıtların SQLite üzerinden listelendiğini gösterin. Bir kaydı düzenleyip sonra silerek güncelleme ve silme özelliklerini sunun.
3. **Filtreler:** Tür, kategori ve tarih seçimini değiştirip işlem listesinin ve özetlerin filtrelere göre güncellendiğini gösterin.
4. **Analiz:** Kategori gider grafiğini ve aylık gelir-gider-bakiye tablosunu gösterin.
5. **Dışa aktarma:** CSV ve Excel indirme düğmelerinin filtrelenmiş kayıtları verdiğini gösterin.

Örnek işlemler gerçek `finance.db` dosyanıza ekleneceği için sunum öncesinde veritabanınızı yedekleyin veya boş veritabanıyla çalışan ayrı bir proje kopyası kullanın.

## Verilerin saklanması

İşlem kayıtları proje klasöründeki `finance.db` SQLite dosyasında saklanır. Dosya ilk çalıştırmada otomatik oluşturulur. Veritabanı bu bilgisayarda kalır; kayıtları başka bir bilgisayara taşımak için `finance.db` dosyasını güvenli şekilde yedekleyebilirsiniz.

Veritabanı ve yerel gizli ayar dosyaları `.gitignore` içinde tutulur; kişisel işlem kayıtlarını GitHub'a yüklemeyin.
