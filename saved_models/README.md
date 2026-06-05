# Kaydedilen Model Dosyaları

Model eğitimi tamamlandığında bu klasöre aşağıdaki dosyalar üretilir:

- `best_model.joblib`: Üretimde kullanılacak en iyi regresyon modeli
- `preprocessor.joblib`: Eksik değer yönetimi, ölçekleme ve kategorik kodlama adımlarını içeren preprocessing pipeline

Bu dosyalar versiyon kontrolüne alınmak zorunda değildir. Deployment ortamında model dosyalarının oluşması için eğitim komutu çalıştırılmalı veya daha önce eğitilmiş güvenilir model dosyaları bu klasöre yerleştirilmelidir.

