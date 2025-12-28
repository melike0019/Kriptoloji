"""
Sezar Şifreleme Algoritması
"""

def caesar_encrypt(text, shift):
    """
    Sezar şifreleme ile metni şifreler.
    
    Args:
        text: Şifrelenecek metin
        shift: Kaydırma miktarı (0-25)
    
    Returns:
        Şifrelenmiş metin
    """
    result = ""
    shift = shift % 26
    
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
        else:
            result += char
    
    return result


def caesar_decrypt(text, shift):
    """
    Sezar şifreleme ile metni çözer.
    
    Args:
        text: Çözülecek metin
        shift: Kaydırma miktarı (0-25)
    
    Returns:
        Çözülmüş metin
    """
    return caesar_encrypt(text, -shift)

