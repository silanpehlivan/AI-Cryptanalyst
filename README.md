# AI Cryptanalyst

Bu proje, Yapay Zeka destekli bir kripto çözücü uygulamasıdır. Streamlit tabanlı kullanıcı arayüzü ile şifreli metinleri analize ederek en olası şifreleme algoritmasını tespit eder ve çözümünü sunar.

## Özellikler

- Caesar (Sezar) şifrelemesi çözümü
- Vigenere şifrelemesi çözümü
- XOR tabanlı şifre çözümü
- Base64 kod çözümü
- Entropi ve İndeks of Coincidence (IC) hesaplama
- Model eğitimi ve doğrulama araçları

## Dosya yapısı

- `app.py`: Streamlit uygulaması
- `main_solver.py`: Ana kriptanaliz sınıfı ve çözümleyici
- `solvers.py`: Şifre çözümleme algoritmaları
- `train_model.py`: Model eğitimi scripti
- `evaluate_model.py`: Eğitilmiş modeli değerlendirme
- `verify_model.py`: Model doğrulama scripti
- `verify_vigenere.py`: Vigenere doğrulama aracı
- `data_generator.py`: Veri seti oluşturma ve işleme
- `utils.py`: Yardımcı fonksiyonlar
- `crypto_dataset.csv`: Kullanılan eğitim/veri seti

## Çalıştırma

1. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

2. Uygulamayı başlatın:

```bash
streamlit run app.py
```

## Notlar

Bu proje, kriptanaliz algoritmalarını ve makine öğrenmesi tabanlı yaklaşımı birleştirerek karmaşık şifrelenmiş metinleri otomatik olarak çözmeyi hedefler.
