# Kriptoloji Final Projesi

Bu proje, klasik ve modern kriptografik algoritmalar kullanılarak şifreli veri iletimi gerçekleştiren kapsamlı bir sistemdir.

## 📋 Proje İçeriği

### 1. Klasik Kriptografi Algoritmaları
Streamlit tabanlı kullanıcı arayüzü üzerinden uygulanan klasik şifreleme yöntemleri:

- **Sezar Şifreleme** - Basit kaydırma şifreleme
- **Substitution Cipher** - Yerine koyma şifreleme
- **Vigenère Cipher** - Çoklu alfabe şifreleme
- **Rail Fence Cipher** - Zigzag şifreleme
- **Columnar Transposition** - Sütun transpozisyon
- **Route Cipher** - Yol bazlı şifreleme (spiral, snake, column)
- **Playfair Cipher** - Bigram şifreleme
- **Polybius Cipher** - Kare tabanlı şifreleme
- **Pigpen Cipher** - Sembol tabanlı şifreleme
- **Hill Cipher** - Matris tabanlı şifreleme (2×2)

### 2. Modern Kriptografi Algoritmaları
- **AES-128** (Advanced Encryption Standard) - CBC modu
- **DES** (Data Encryption Standard) - CBC modu

### 3. Manuel Implementasyonlar (Kütüphanesiz)
Eğitim amaçlı sadeleştirilmiş implementasyonlar:

**Manuel DES:**
- Feistel Network yapısı
- S-Box substitution (8 adet)
- Permütasyon işlemleri
- Round key generation

### 4. İstemci-Sunucu Haberleşmesi
- RSA ile güvenli anahtar dağıtımı
- AES/DES ile şifreli veri iletimi
- Terminal tabanlı uygulama

## 🚀 Kurulum

### Gereksinimler
- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Adımlar

1. **Projeyi klonlayın veya indirin**

2. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

## 📖 Kullanım

### Streamlit Arayüzü

Klasik ve modern kriptografi algoritmalarını test etmek için Streamlit arayüzünü kullanın:

```bash
streamlit run streamlit_app.py
```

Tarayıcınızda otomatik olarak açılacaktır (genellikle `http://localhost:8501`).

**Özellikler:**
- Klasik kriptografi algoritmalarını seçip test edebilirsiniz
- Modern kriptografi (AES/DES) algoritmalarını deneyebilirsiniz
- Manuel DES implementasyonunu görebilirsiniz
- Şifreleme ve çözme işlemlerini gerçekleştirebilirsiniz

### İstemci-Sunucu Uygulaması

#### Sunucuyu Başlatma

Bir terminal penceresinde:

```bash
python client_server/server.py
```

Sunucu `localhost:12345` adresinde dinlemeye başlayacaktır.

#### İstemciyi Çalıştırma

Başka bir terminal penceresinde:

```bash
python client_server/client.py
```

İstemci sunucuya bağlanacak, RSA ile anahtar alışverişi yapacak ve AES/DES ile şifrelenmiş mesaj gönderecektir.

**İşlem Akışı:**
1. Sunucu RSA anahtar çifti oluşturur
2. Sunucu açık anahtarı istemciye gönderir
3. İstemci simetrik anahtarı (AES/DES) oluşturur
4. İstemci simetrik anahtarı RSA ile şifreleyip sunucuya gönderir
5. İstemci mesajı simetrik anahtarla şifreleyip gönderir
6. Sunucu simetrik anahtarı çözer
7. Sunucu mesajı çözer ve gösterir

## 📁 Proje Yapısı

```
Kriptoloji/
├── classical_ciphers/          # Klasik şifreleme algoritmaları
│   ├── caesar.py
│   ├── substitution.py
│   ├── vigenere.py
│   ├── rail_fence.py
│   ├── columnar_transposition.py
│   ├── route_cipher.py
│   ├── playfair.py
│   ├── polybius.py
│   ├── pigpen.py
│   ├── hill.py
│   └── __init__.py
├── modern_ciphers/             # Modern şifreleme algoritmaları
│   ├── aes_des.py
│   └── __init__.py
├── manual_des/                 # Manuel DES implementasyonu
│   ├── manual_des.py
│   ├── test_manual_des.py
│   └── __init__.py
├── client_server/              # İstemci-sunucu uygulaması
│   ├── server.py
│   ├── client.py
│   └── __init__.py
├── streamlit_app.py            # Ana Streamlit uygulaması
├── requirements.txt            # Python bağımlılıkları
└── README.md                   # Bu dosya
```

### Wireshark ile Paket Analizi

İstemci-sunucu uygulaması çalışırken Wireshark kullanarak ağ trafiğini analiz edebilirsiniz:

1. Wireshark'ı açın
2. `localhost` veya `127.0.0.1` trafiğini dinleyin
3. İstemci-sunucu haberleşmesini gözlemleyin
4. TCP paketlerinin payload kısımlarında şifrelenmiş veriyi görebilirsiniz
5. Açık metin görünmeyecek, sadece şifrelenmiş bayt dizileri görünecektir

## 📝 Özellikler

- ✅ 10 farklı klasik kriptografi algoritması
- ✅ AES-128 ve DES modern şifreleme algoritmaları (kütüphaneli)
- ✅ Manuel DES implementasyonları (kütüphanesiz, eğitim amaçlı)
- ✅ RSA ile güvenli anahtar dağıtımı
- ✅ İstemci-sunucu şifreli haberleşme (AES/DES + RSA)
- ✅ Kullanıcı dostu Streamlit arayüzü
- ✅ Terminal tabanlı istemci-sunucu uygulaması
- ✅ Wireshark ile paket analizi desteği


