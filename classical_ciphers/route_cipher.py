"""
Route Cipher Algoritması
"""

def route_cipher_encrypt(text, rows, cols, route='spiral'):
    """
    Route cipher ile metni şifreler.
    
    Args:
        text: Şifrelenecek metin
        rows: Satır sayısı
        cols: Sütun sayısı
        route: Okuma yolu ('spiral', 'snake', 'column')
    
    Returns:
        Şifrelenmiş metin
    """
    text = text.replace(' ', '').upper()
    
    # Matrisi doldur
    matrix = [[''] * cols for _ in range(rows)]
    text_index = 0
    
    for row in range(rows):
        for col in range(cols):
            if text_index < len(text):
                matrix[row][col] = text[text_index]
                text_index += 1
            else:
                matrix[row][col] = 'X'  # Padding
    
    # Yola göre oku
    if route == 'spiral':
        return _read_spiral(matrix, rows, cols)
    elif route == 'snake':
        return _read_snake(matrix, rows, cols)
    else:  # column
        return _read_column(matrix, rows, cols)


def route_cipher_decrypt(text, rows, cols, route='spiral'):
    """
    Route cipher ile metni çözer.
    
    Args:
        text: Çözülecek metin
        rows: Satır sayısı
        cols: Sütun sayısı
        route: Okuma yolu
    
    Returns:
        Çözülmüş metin
    """
    matrix = [[''] * cols for _ in range(rows)]
    
    # Yola göre yaz
    if route == 'spiral':
        _write_spiral(matrix, rows, cols, text)
    elif route == 'snake':
        _write_snake(matrix, rows, cols, text)
    else:  # column
        _write_column(matrix, rows, cols, text)
    
    # Matrisi satır satır oku
    result = ""
    for row in range(rows):
        for col in range(cols):
            result += matrix[row][col]
    
    return result.rstrip('X')


def _read_spiral(matrix, rows, cols):
    """Spiral yoluyla okur."""
    result = ""
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    
    while top <= bottom and left <= right:
        # Sağa
        for col in range(left, right + 1):
            result += matrix[top][col]
        top += 1
        
        # Aşağı
        for row in range(top, bottom + 1):
            result += matrix[row][right]
        right -= 1
        
        if top <= bottom:
            # Sola
            for col in range(right, left - 1, -1):
                result += matrix[bottom][col]
            bottom -= 1
        
        if left <= right:
            # Yukarı
            for row in range(bottom, top - 1, -1):
                result += matrix[row][left]
            left += 1
    
    return result


def _write_spiral(matrix, rows, cols, text):
    """Spiral yoluyla yazar."""
    text_index = 0
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    
    while top <= bottom and left <= right and text_index < len(text):
        # Sağa
        for col in range(left, right + 1):
            if text_index < len(text):
                matrix[top][col] = text[text_index]
                text_index += 1
        top += 1
        
        # Aşağı
        for row in range(top, bottom + 1):
            if text_index < len(text):
                matrix[row][right] = text[text_index]
                text_index += 1
        right -= 1
        
        if top <= bottom:
            # Sola
            for col in range(right, left - 1, -1):
                if text_index < len(text):
                    matrix[bottom][col] = text[text_index]
                    text_index += 1
            bottom -= 1
        
        if left <= right:
            # Yukarı
            for row in range(bottom, top - 1, -1):
                if text_index < len(text):
                    matrix[row][left] = text[text_index]
                    text_index += 1
            left += 1


def _read_snake(matrix, rows, cols):
    """Yılan yoluyla okur (satır satır, alternatif yönler)."""
    result = ""
    for row in range(rows):
        if row % 2 == 0:
            for col in range(cols):
                result += matrix[row][col]
        else:
            for col in range(cols - 1, -1, -1):
                result += matrix[row][col]
    return result


def _write_snake(matrix, rows, cols, text):
    """Yılan yoluyla yazar."""
    text_index = 0
    for row in range(rows):
        if row % 2 == 0:
            for col in range(cols):
                if text_index < len(text):
                    matrix[row][col] = text[text_index]
                    text_index += 1
        else:
            for col in range(cols - 1, -1, -1):
                if text_index < len(text):
                    matrix[row][col] = text[text_index]
                    text_index += 1


def _read_column(matrix, rows, cols):
    """Sütun sütun okur."""
    result = ""
    for col in range(cols):
        for row in range(rows):
            result += matrix[row][col]
    return result


def _write_column(matrix, rows, cols, text):
    """Sütun sütun yazar."""
    text_index = 0
    for col in range(cols):
        for row in range(rows):
            if text_index < len(text):
                matrix[row][col] = text[text_index]
                text_index += 1

