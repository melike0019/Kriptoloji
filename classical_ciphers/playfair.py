"""
Playfair Cipher Algoritması
"""

def _prepare_key(key):
    """Anahtardan 5x5 matris oluşturur."""
    key = key.upper().replace('J', 'I')
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    
    # Tekrarları kaldır ve matrisi oluştur
    seen = set()
    matrix = []
    
    for char in key:
        if char.isalpha() and char not in seen:
            matrix.append(char)
            seen.add(char)
    
    for char in alphabet:
        if char not in seen:
            matrix.append(char)
    
    return [matrix[i:i+5] for i in range(0, 25, 5)]


def _find_position(matrix, char):
    """Karakterin matristeki pozisyonunu bulur."""
    char = char.upper().replace('J', 'I')
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return (i, j)
    return None


def _prepare_text(text):
    """Metni Playfair için hazırlar (çiftler halinde)."""
    text = text.upper().replace('J', 'I').replace(' ', '')
    pairs = []
    i = 0
    
    while i < len(text):
        if i + 1 < len(text):
            if text[i] == text[i + 1]:
                pairs.append(text[i] + 'X')
                i += 1
            else:
                pairs.append(text[i] + text[i + 1])
                i += 2
        else:
            pairs.append(text[i] + 'X')
            i += 1
    
    return pairs


def playfair_encrypt(text, key):
    """
    Playfair cipher ile metni şifreler.
    
    Args:
        text: Şifrelenecek metin
        key: Anahtar kelime
    
    Returns:
        Şifrelenmiş metin
    """
    matrix = _prepare_key(key)
    pairs = _prepare_text(text)
    result = ""
    
    for pair in pairs:
        char1, char2 = pair[0], pair[1]
        row1, col1 = _find_position(matrix, char1)
        row2, col2 = _find_position(matrix, char2)
        
        if row1 == row2:
            # Aynı satır
            result += matrix[row1][(col1 + 1) % 5]
            result += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            # Aynı sütun
            result += matrix[(row1 + 1) % 5][col1]
            result += matrix[(row2 + 1) % 5][col2]
        else:
            # Dikdörtgen
            result += matrix[row1][col2]
            result += matrix[row2][col1]
    
    return result


def playfair_decrypt(text, key):
    """
    Playfair cipher ile metni çözer.
    
    Args:
        text: Çözülecek metin
        key: Anahtar kelime
    
    Returns:
        Çözülmüş metin
    """
    matrix = _prepare_key(key)
    pairs = _prepare_text(text)
    result = ""
    
    for pair in pairs:
        char1, char2 = pair[0], pair[1]
        row1, col1 = _find_position(matrix, char1)
        row2, col2 = _find_position(matrix, char2)
        
        if row1 == row2:
            # Aynı satır
            result += matrix[row1][(col1 - 1) % 5]
            result += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            # Aynı sütun
            result += matrix[(row1 - 1) % 5][col1]
            result += matrix[(row2 - 1) % 5][col2]
        else:
            # Dikdörtgen
            result += matrix[row1][col2]
            result += matrix[row2][col1]
    
    return result

