# Model Raporları

Eğitim işlemi sonrasında model performans sonuçları bu klasöre yazılır:

- `model_results.json`: Web arayüzünün okuduğu model performans raporu
- `model_results.csv`: Tablo tabanlı analiz için performans çıktısı
- `feature_importance.csv`: Seçilen model destekliyorsa özellik önem skorları

Raporlarda MAE, MSE, RMSE ve R2 Score metrikleri bulunur. Üretim modeli öncelikle en düşük RMSE değerine göre seçilir.

