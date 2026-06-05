# Dataset Kullanımı

Bu klasör model eğitimi için kullanılan veri dosyalarını içerir.

Varsayılan eğitim komutu önce şu dosyayı arar:

```bash
data/energy_consumption.csv
```

Bu dosya yoksa proje içinde gelen küçük örnek dataset kullanılır:

```bash
data/sample_energy_consumption.csv
```

Örnek dataset yalnızca kurulumun ve eğitim pipeline'ının çalıştığını göstermek içindir. Üretim kalitesinde bir model eğitmek için daha geniş, gerçek ve temsil gücü yüksek bir akıllı ev enerji tüketimi dataseti kullanılmalıdır.

## Beklenen Kolonlar

- `temperature`: Sıcaklık değeri
- `humidity`: Nem oranı
- `hour`: Gün içindeki saat, 0-23
- `day_of_week`: Haftanın günü, Pazartesi 0 ve Pazar 6
- `month`: Ay, 1-12
- `active_appliances`: Aynı anda aktif olan cihaz sayısı
- `lights_usage`: Açık aydınlatma noktası sayısı
- `heating_status`: Isıtma sistemi durumu, 0 veya 1
- `cooling_status`: Soğutma sistemi durumu, 0 veya 1
- `household_size`: Evde yaşayan kişi sayısı
- `weather_condition`: `gunesli`, `bulutlu`, `yagmurlu`, `karli` veya `ruzgarli`
- `energy_consumption`: Hedef değişken, kWh cinsinden enerji tüketimi

## Gerçek Dataset Önerisi

Appliances Energy Prediction gibi kamuya açık enerji tüketimi datasetleri bu proje için uygun bir başlangıç olabilir. Gerçek dataset kullanırken kolon adlarını yukarıdaki sözleşmeye uyarlayın veya `app/ml/preprocessing.py` içindeki kolon tanımlarını bilinçli biçimde güncelleyin.

