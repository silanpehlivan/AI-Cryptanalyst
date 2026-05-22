# AI Cryptanalyst 🚀

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Streamlit](https://img.shields.io/badge/Streamlit-%23FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/) [![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

AI Cryptanalyst, Yapay Zeka destekli bir kripto çözücü uygulamasıdır. Streamlit tabanlı görsel kullanıcı arayüzü üzerinden şifreli metinleri analiz eder, en uygun şifreleme algoritmasını tahmin eder ve çözümünü sağlar.

## ✨ Öne çıkanlar

- Otomatik şifre tespiti ve çözümleme
- Caesar, Vigenere, XOR ve Base64 destekli
- Metin analizi için Entropi ve IC hesaplama
- Model eğitimi, değerlendirme ve doğrulama araçları
- Kullanıcı dostu Streamlit arayüzü

## ⚙️ Özellikler

- `Caesar` (Sezar) şifre çözümü
- `Vigenere` şifre çözümü
- `XOR` tabanlı şifre çözümü
- `Base64` kod çözümü
- Entropi hesaplama
- İndeks of Coincidence (IC) analizi
- Model eğitim ve doğrulama süreçleri

## 🧩 Nasıl çalışır?

1. Kullanıcı şifreli metni girer.
2. Model ve algoritmalar metni analiz eder.
3. En olası şifreleme türü tespit edilir.
4. Şifreli metin çözülür ve kullanıcıya sunulur.

## 📁 Dosya yapısı

- `app.py`: Streamlit uygulaması
- `main_solver.py`: Ana kriptanaliz sınıfı ve çözümleyici
- `solvers.py`: Şifre çözümleme algoritmaları
- `train_model.py`: Model eğitim scripti
- `evaluate_model.py`: Eğitilmiş modeli değerlendirme
- `verify_model.py`: Model doğrulama scripti
- `verify_vigenere.py`: Vigenere doğrulama aracı
- `data_generator.py`: Veri seti oluşturma ve işleme
- `utils.py`: Yardımcı fonksiyonlar
- `crypto_dataset.csv`: Kullanılan eğitim/veri seti

## 🚀 Kurulum

1. Proje dizinine gidin:

```bash
cd AI-Cryptanalyst
```

2. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:

```bash
streamlit run app.py
```

## Notlar

Bu proje, kriptanaliz algoritmalarını ve makine öğrenmesi tabanlı yaklaşımı birleştirerek karmaşık şifrelenmiş metinleri otomatik olarak çözmeyi hedefler.
