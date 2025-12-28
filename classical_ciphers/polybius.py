"""
Polybius Square Cipher Algoritması
"""

def _create_polybius_square(key=""):
    """Polybius karesi oluşturur."""
    if key:
        key = key.upper().replace('J', 'I')
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        seen = set()
        square = []
        
        for char in key:
            if char.isalpha() and char not in seen:
                square.append(char)
                seen.add(char)
        
        for char in alphabet:
            if char not in seen:
                square.append(char)
    else:
        square = list("ABCDEFGHIKLMNOPQRSTUVWXYZ")
    
    return [square[i:i+5] for i in range(0, 25, 5)]


def polybius_encrypt(text, key=""):
    """
    Polybius cipher ile metni şifreler.
    
    Args:
        text: Şifrelenecek metin
        key: Anahtar kelime (opsiyonel)
    
    Returns:
        Şifrelenmiş metin (rakam çiftleri)
    """
    square = _create_polybius_square(key)
    text = text.upper().replace('J', 'I').replace(' ', '')
    result = ""
    
    for char in text:
        if char.isalpha():
            for i in range(5):
                for j in range(5):
                    if square[i][j] == char:
                        result += str(i + 1) + str(j + 1)
        else:
            result += char
    
    return result


def polybius_decrypt(text, key=""):
    """
    Polybius cipher ile metni çözer.
    
    Args:
        text: Çözülecek metin (rakam çiftleri)
        key: Anahtar kelime (opsiyonel)
    
    Returns:
        Çözülmüş metin
    """
    square = _create_polybius_square(key)
    result = ""
    i = 0
    
    while i < len(text):
        if text[i].isdigit():
            if i + 1 < len(text) and text[i + 1].isdigit():
                row = int(text[i]) - 1
                col = int(text[i + 1]) - 1
                if 0 <= row < 5 and 0 <= col < 5:
                    result += square[row][col]
                i += 2
            else:
                i += 1
        else:
            result += text[i]
            i += 1
    
    return result

