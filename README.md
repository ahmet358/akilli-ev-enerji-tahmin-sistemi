# Akıllı Ev Enerji Tüketimi Tahmin Sistemi

Akıllı Ev Enerji Tüketimi Tahmin Sistemi; kullanıcı girdilerine göre akıllı ev enerji tüketimini tahmin eden, tahminleri ve kullanıcı işlemlerini SQLite veritabanında saklayan, birden fazla makine öğrenmesi modelini eğitip karşılaştıran ve en iyi modeli web arayüzü üzerinden üretim tahmini için kullanan uçtan uca bir FastAPI uygulamasıdır.

Proje; backend, veritabanı, makine öğrenmesi pipeline'ı, Jinja2 tabanlı responsive arayüz, model performans ekranı, Docker desteği ve Render deployment yapılandırmasını birlikte sunar.

## Temel Özellikler

- Kullanıcı oluşturma ve gizlilik dostu basit profil yönetimi
- Enerji tüketimi tahmini için doğrulamalı Türkçe form arayüzü
- Tahmin kayıtlarının ve kullanıcı işlemlerinin veritabanında saklanması
- Linear Regression, Ridge Regression, Random Forest Regressor, Gradient Boosting Regressor ve Support Vector Regressor modellerinin eğitilmesi
- MAE, MSE, RMSE ve R2 Score metrikleriyle model karşılaştırması
- En iyi modelin RMSE öncelikli seçim kuralıyla üretim modeli olarak kaydedilmesi
- Dashboard üzerinde kullanıcı, tahmin, ortalama tüketim, aktif model ve son işlem görünümü
- Plotly grafikleriyle tahmin ve model performansı görselleştirmeleri
- Dockerfile, `.env.example` ve `render.yaml` ile deployment hazırlığı

## Kullanılan Teknolojiler

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- scikit-learn
- pandas ve numpy
- joblib
- Jinja2
- HTML, CSS, JavaScript
- Bootstrap ve Bootstrap Icons
- Plotly
- python-dotenv
- Docker

## Proje Mimarisi

```text
smart-home-energy-prediction/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── routes/
│   ├── ml/
│   ├── templates/
│   └── static/
├── data/
├── saved_models/
├── reports/
├── notebooks/
├── requirements.txt
├── Dockerfile
├── render.yaml
├── .env.example
└── README.md
```

## Veritabanı Yapısı

Uygulama varsayılan olarak SQLite kullanır. `DATABASE_URL` ortam değişkeniyle farklı bir bağlantı adresi verilebilir.

### users

- `id`
- `full_name`
- `email`
- `created_at`

### prediction_records

- `id`
- `user_id`
- `temperature`
- `humidity`
- `hour`
- `day_of_week`
- `month`
- `active_appliances`
- `lights_usage`
- `heating_status`
- `cooling_status`
- `household_size`
- `weather_condition`
- `predicted_energy_consumption`
- `model_used`
- `created_at`

### user_actions

- `id`
- `user_id`
- `action_type`
- `action_description`
- `created_at`

Sistem parola saklamaz. Kullanıcı bilgileri yalnızca tahmin geçmişini ve işlem kayıtlarını ilişkilendirmek için tutulur.

## Makine Öğrenmesi Akışı

Eğitim pipeline'ı `app/ml/train_model.py` içinde bulunur.

1. Dataset yüklenir.
2. Beklenen kolonlar doğrulanır.
3. Eksik değerler yönetilir.
4. Sayısal kolonlar ölçeklenir.
5. Kategorik kolonlar One-Hot Encoding ile kodlanır.
6. Veri eğitim ve test setlerine ayrılır.
7. Birden fazla regresyon modeli eğitilir.
8. MAE, MSE, RMSE ve R2 Score metrikleri hesaplanır.
9. En düşük RMSE ve eşitlik durumunda en yüksek R2 Score değerine göre en iyi model seçilir.
10. Model, preprocessing pipeline ve rapor dosyaları kaydedilir.

## Üretilen Model ve Rapor Dosyaları

Eğitimden sonra şu dosyalar oluşturulur:

- `saved_models/best_model.joblib`
- `saved_models/preprocessor.joblib`
- `reports/model_results.json`
- `reports/model_results.csv`
- `reports/feature_importance.csv`

`feature_importance.csv` yalnızca seçilen model özellik önem skorlarını destekliyorsa üretilir.

## Dataset Kullanımı

Varsayılan gerçek dataset yolu:

```bash
data/energy_consumption.csv
```

Bu dosya yoksa eğitim komutu proje içindeki küçük örnek dataset ile çalışır:

```bash
data/sample_energy_consumption.csv
```

Örnek dataset yalnızca sistemin kurulup çalıştığını doğrulamak içindir. Gerçek tahmin kalitesi için daha geniş ve temsili bir akıllı ev enerji tüketimi dataseti kullanılmalıdır. Beklenen kolonlar `data/README.md` dosyasında açıklanmıştır.

## Yerel Kurulum

Proje klasörüne girin:

```bash
cd smart-home-energy-prediction
```

Sanal ortam oluşturun:

```bash
python -m venv .venv
```

Windows PowerShell için sanal ortamı etkinleştirin:

```bash
.\.venv\Scripts\Activate.ps1
```

macOS veya Linux için:

```bash
source .venv/bin/activate
```

Bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

İsteğe bağlı olarak ortam dosyasını oluşturun:

```bash
copy .env.example .env
```

macOS veya Linux için:

```bash
cp .env.example .env
```

## Modeli Eğitme

```bash
python app/ml/train_model.py
```

Komut tamamlandığında en iyi model `saved_models/` klasörüne, performans raporları ise `reports/` klasörüne kaydedilir.

## Web Sitesini Başlatma

```bash
uvicorn app.main:app --reload
```

Tarayıcıdan şu adrese gidin:

```text
http://127.0.0.1:8000
```

## Sistemi Kullanma

1. Ana sayfadan kullanıcı oluşturma ekranına gidin.
2. Ad soyad ve e-posta ile basit bir kullanıcı profili oluşturun.
3. Tahmin sayfasında ev koşullarını girin.
4. Tahmini hesaplayın ve sonuç sayfasındaki kWh değerini inceleyin.
5. Dashboard sayfasından son tahminleri, işlem kayıtlarını ve grafiklerini görüntüleyin.
6. Model Performansı sayfasından eğitilen modellerin metriklerini karşılaştırın.

## Ortam Değişkenleri

`.env.example` dosyasında önerilen değişkenler bulunur:

- `APP_NAME`: Uygulama adı
- `DEBUG`: Geliştirme modu
- `DATABASE_URL`: Veritabanı bağlantısı
- `MODEL_PATH`: Üretim modeli dosya yolu
- `PREPROCESSOR_PATH`: Preprocessing pipeline dosya yolu
- `DATASET_PATH`: Eğitim dataseti dosya yolu

## Docker ile Çalıştırma

Docker imajını oluşturun:

```bash
docker build -t akilli-ev-enerji .
```

Container başlatın:

```bash
docker run -p 8000:8000 akilli-ev-enerji
```

Model dosyaları container içinde yoksa önce eğitim komutunu çalıştırmanız gerekir. Gerçek deployment için eğitilmiş model dosyalarını imaja dahil edebilir veya deployment öncesinde eğitim adımını ayrı bir süreç olarak çalıştırabilirsiniz.

## Render Üzerinde Deployment

Projede Render Blueprint için `render.yaml` dosyası hazırdır.

1. Projeyi GitHub, GitLab veya Bitbucket üzerinde bir repoya gönderin.
2. Render Dashboard üzerinde yeni Blueprint oluşturun.
3. Repoyu seçin ve Render'ın `render.yaml` dosyasını okumasını sağlayın.
4. Ortam değişkenlerini kontrol edin.
5. Deployment işlemini başlatın.
6. Deployment sonrası `/health` endpoint'inin çalıştığını doğrulayın.

Render Blueprint bağlantısı repo adresine göre şu formatta olur:

```text
https://dashboard.render.com/blueprint/new?repo=https://github.com/kullanici/repo-adi
```

SQLite dosyası ücretsiz web servislerinde kalıcı disk olmadan geçici olabilir. Kalıcı production kullanımı için Render Disk, yönetilen PostgreSQL veya başka bir kalıcı veritabanı tercih edilmelidir.

## Ekran Görüntüleri

Bu bölüm deployment veya yerel çalıştırma sonrası ekran görüntüleriyle doldurulabilir.

- Ana Sayfa
- Tahmin Formu
- Tahmin Sonucu
- Dashboard
- Model Performansı

## Gelecek İyileştirmeler

- Gerçek akıllı sayaç verisiyle daha geniş eğitim
- Kullanıcı bazlı güvenli kimlik doğrulama
- PostgreSQL desteği ve migration yönetimi
- Model versiyonlama ve otomatik yeniden eğitim akışı
- Zaman serisi özellikleri ve mevsimsellik analizi
- API tabanlı tahmin endpoint'i ve rate limiting
- Dashboard için daha ayrıntılı enerji verimliliği önerileri

