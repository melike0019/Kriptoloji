"""
Substitution Cipher (Yerine Koyma Şifreleme)
"""

import random
import string


def generate_key():
    """Rastgele bir substitution key oluşturur."""
    alphabet = list(string.ascii_uppercase)
    shuffled = alphabet.copy()
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))


def substitution_encrypt(text, key):
    """
    Substitution cipher ile metni şifreler.
    
    Args:
        text: Şifrelenecek metin
        key: Karakter eşleştirme sözlüğü
    
    Returns:
        Şifrelenmiş metin
    """
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += key.get(char, char)
        else:
            result += char
    return result


def substitution_decrypt(text, key):
    """
    Substitution cipher ile metni çözer.
    
    Args:
        text: Çözülecek metin
        key: Karakter eşleştirme sözlüğü
    
    Returns:
        Çözülmüş metin
    """
    reverse_key = {v: k for k, v in key.items()}
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += reverse_key.get(char, char)
        else:
            result += char
    return result

