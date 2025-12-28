"""
Vigenère Cipher Algoritması
"""

def vigenere_encrypt(text, key):
    """
    Vigenère cipher ile metni şifreler.
    
    Args:
        text: Şifrelenecek metin
        key: Anahtar kelime
    
    Returns:
        Şifrelenmiş metin
    """
    result = ""
    key = key.upper()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - 65
            
            shifted = (ord(char) - ascii_offset + shift) % 26
            result += chr(shifted + ascii_offset)
            key_index += 1
        else:
            result += char
    
    return result


def vigenere_decrypt(text, key):
    """
    Vigenère cipher ile metni çözer.
    
    Args:
        text: Çözülecek metin
        key: Anahtar kelime
    
    Returns:
        Çözülmüş metin
    """
    result = ""
    key = key.upper()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - 65
            
            shifted = (ord(char) - ascii_offset - shift) % 26
            result += chr(shifted + ascii_offset)
            key_index += 1
        else:
            result += char
    
    return result

