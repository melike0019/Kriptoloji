"""
Columnar Transposition Cipher Algoritması
"""

def columnar_transposition_encrypt(text, key):
    """
    Columnar Transposition cipher ile metni şifreler.
    
    Args:
        text: Şifrelenecek metin (boşluklar kaldırılır)
        key: Anahtar kelime
    
    Returns:
        Şifrelenmiş metin
    """
    text = text.replace(' ', '').upper()
    key = key.upper()
    
    # Anahtarın sıralı indekslerini bul
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    
    # Matris oluştur
    num_cols = len(key)
    num_rows = (len(text) + num_cols - 1) // num_cols
    
    # Metni matrise yerleştir
    matrix = [[''] * num_cols for _ in range(num_rows)]
    text_index = 0
    
    for row in range(num_rows):
        for col in range(num_cols):
            if text_index < len(text):
                matrix[row][col] = text[text_index]
                text_index += 1
            else:
                matrix[row][col] = 'X'  # Padding
    
    # Sütunları anahtar sırasına göre oku
    result = ""
    for col in key_order:
        for row in range(num_rows):
            result += matrix[row][col]
    
    return result


def columnar_transposition_decrypt(text, key):
    """
    Columnar Transposition cipher ile metni çözer.
    
    Args:
        text: Çözülecek metin
        key: Anahtar kelime
    
    Returns:
        Çözülmüş metin
    """
    key = key.upper()
    
    # Anahtarın sıralı indekslerini bul
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    
    num_cols = len(key)
    num_rows = (len(text) + num_cols - 1) // num_cols
    
    # Matris oluştur
    matrix = [[''] * num_cols for _ in range(num_rows)]
    
    # Şifreli metni matrise yerleştir
    text_index = 0
    for col in key_order:
        for row in range(num_rows):
            if text_index < len(text):
                matrix[row][col] = text[text_index]
                text_index += 1
    
    # Matrisi satır satır oku
    result = ""
    for row in range(num_rows):
        for col in range(num_cols):
            result += matrix[row][col]
    
    # Padding'i kaldır
    return result.rstrip('X')

