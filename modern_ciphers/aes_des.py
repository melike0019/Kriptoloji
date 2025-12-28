"""
Modern Kriptografi Algoritmaları (AES ve DES)
Kütüphane kullanarak implementasyon
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import base64


def aes_encrypt(plaintext, key=None):
    """
    AES-128 ile metni şifreler (CBC modu).
    
    Args:
        plaintext: Şifrelenecek metin
        key: 16 byte anahtar (None ise rastgele oluşturulur)
    
    Returns:
        (iv, encrypted_data) tuple'ı
    """
    if key is None:
        key = os.urandom(16)
    elif len(key) != 16:
        # Anahtarı 16 byte'a tamamla veya kısalt
        key = key[:16].ljust(16, b'0')
    
    # IV oluştur
    iv = os.urandom(16)
    
    # Padding ekle
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode('utf-8'))
    padded_data += padder.finalize()
    
    # Şifrele
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv, ciphertext


def aes_decrypt(iv, ciphertext, key):
    """
    AES-128 ile metni çözer (CBC modu).
    
    Args:
        iv: Initialization Vector
        ciphertext: Şifrelenmiş veri
        key: 16 byte anahtar
    
    Returns:
        Çözülmüş metin
    """
    if len(key) != 16:
        key = key[:16].ljust(16, b'0')
    
    # Çöz
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Padding kaldır
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext)
    plaintext += unpadder.finalize()
    
    return plaintext.decode('utf-8')


def des_encrypt(plaintext, key=None):
    """
    DES ile metni şifreler (CBC modu).
    
    Not: cryptography kütüphanesi normal DES'i desteklemediği için
    TripleDES kullanılmaktadır. 8 byte anahtar ile TripleDES, 
    aynı anahtarın 3 kez kullanıldığı EDE modunda çalışır.
    
    Args:
        plaintext: Şifrelenecek metin
        key: 8 byte anahtar (None ise rastgele oluşturulur)
    
    Returns:
        (iv, encrypted_data) tuple'ı
    """
    if key is None:
        key = os.urandom(8)
    elif len(key) != 8:
        key = key[:8].ljust(8, b'0')
    
    # IV oluştur
    iv = os.urandom(8)
    
    # Padding ekle
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(plaintext.encode('utf-8'))
    padded_data += padder.finalize()
    
    # Şifrele (TripleDES kullanılıyor - 8 byte anahtar ile EDE modu)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv, ciphertext


def des_decrypt(iv, ciphertext, key):
    """
    DES ile metni çözer (CBC modu).
    
    Not: TripleDES kullanılmaktadır (normal DES desteği yok).
    
    Args:
        iv: Initialization Vector
        ciphertext: Şifrelenmiş veri
        key: 8 byte anahtar
    
    Returns:
        Çözülmüş metin
    """
    if len(key) != 8:
        key = key[:8].ljust(8, b'0')
    
    # Çöz (TripleDES)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Padding kaldır
    unpadder = padding.PKCS7(64).unpadder()
    plaintext = unpadder.update(padded_plaintext)
    plaintext += unpadder.finalize()
    
    return plaintext.decode('utf-8')

