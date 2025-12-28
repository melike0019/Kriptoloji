"""
Hill Cipher Algoritması (2x2 Matris)
"""

import numpy as np


def _mod_inverse(a, m):
    """Modüler ters hesaplar."""
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None


def _text_to_numbers(text):
    """Metni sayılara çevirir (A=0, B=1, ..., Z=25)."""
    return [ord(c.upper()) - 65 for c in text if c.isalpha()]


def _numbers_to_text(numbers):
    """Sayıları metne çevirir."""
    return ''.join([chr(n + 65) for n in numbers])


def _validate_key(key_matrix):
    """Anahtar matrisinin geçerliliğini kontrol eder."""
    det = int(np.linalg.det(key_matrix)) % 26
    if det == 0:
        return False
    return _mod_inverse(det, 26) is not None


def hill_encrypt(text, key_matrix):
    """
    Hill cipher ile metni şifreler (2x2 matris).
    
    Args:
        text: Şifrelenecek metin
        key_matrix: 2x2 anahtar matrisi (liste veya numpy array)
    
    Returns:
        Şifrelenmiş metin
    """
    text = text.replace(' ', '').upper()
    
    # Tek sayıda karakter varsa padding ekle
    if len(text) % 2 != 0:
        text += 'X'
    
    # Anahtar matrisini numpy array'e çevir
    key = np.array(key_matrix, dtype=int)
    
    if not _validate_key(key):
        raise ValueError("Geçersiz anahtar matrisi! Determinant 26 ile aralarında asal olmalı.")
    
    # Metni sayılara çevir
    numbers = _text_to_numbers(text)
    
    # Çiftler halinde şifrele
    result_numbers = []
    for i in range(0, len(numbers), 2):
        pair = np.array([[numbers[i]], [numbers[i + 1]]])
        encrypted = np.dot(key, pair) % 26
        result_numbers.extend(encrypted.flatten())
    
    return _numbers_to_text(result_numbers)


def hill_decrypt(text, key_matrix):
    """
    Hill cipher ile metni çözer (2x2 matris).
    
    Args:
        text: Çözülecek metin
        key_matrix: 2x2 anahtar matrisi
    
    Returns:
        Çözülmüş metin
    """
    text = text.replace(' ', '').upper()
    
    # Anahtar matrisini numpy array'e çevir
    key = np.array(key_matrix, dtype=int)
    
    if not _validate_key(key):
        raise ValueError("Geçersiz anahtar matrisi!")
    
    # Determinant ve modüler ters
    det = int(np.linalg.det(key)) % 26
    det_inv = _mod_inverse(det, 26)
    
    # Adjoint matris
    adj = np.array([[key[1, 1], -key[0, 1]], [-key[1, 0], key[0, 0]]])
    adj = adj % 26
    
    # Ters matris
    inv_key = (det_inv * adj) % 26
    
    # Metni sayılara çevir
    numbers = _text_to_numbers(text)
    
    # Çiftler halinde çöz
    result_numbers = []
    for i in range(0, len(numbers), 2):
        pair = np.array([[numbers[i]], [numbers[i + 1]]])
        decrypted = np.dot(inv_key, pair) % 26
        result_numbers.extend(decrypted.flatten())
    
    return _numbers_to_text(result_numbers)

