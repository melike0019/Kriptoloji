"""
Rail Fence Cipher Algoritması
"""

def rail_fence_encrypt(text, rails):
    """
    Rail Fence cipher ile metni şifreler.
    
    Args:
        text: Şifrelenecek metin
        rails: Ray sayısı
    
    Returns:
        Şifrelenmiş metin
    """
    if rails == 1:
        return text
    
    # Ray'leri oluştur
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    
    for char in text:
        fence[rail].append(char)
        rail += direction
        
        if rail == rails - 1 or rail == 0:
            direction = -direction
    
    # Ray'leri birleştir
    result = ''.join([''.join(row) for row in fence])
    return result


def rail_fence_decrypt(text, rails):
    """
    Rail Fence cipher ile metni çözer.
    
    Args:
        text: Çözülecek metin
        rails: Ray sayısı
    
    Returns:
        Çözülmüş metin
    """
    if rails == 1:
        return text
    
    # Ray uzunluklarını hesapla
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    
    for _ in text:
        fence[rail].append(None)
        rail += direction
        
        if rail == rails - 1 or rail == 0:
            direction = -direction
    
    # Metni ray'lere dağıt
    index = 0
    for i in range(rails):
        for j in range(len(fence[i])):
            fence[i][j] = text[index]
            index += 1
    
    # Orijinal metni oluştur
    result = []
    rail = 0
    direction = 1
    
    for _ in text:
        result.append(fence[rail].pop(0))
        rail += direction
        
        if rail == rails - 1 or rail == 0:
            direction = -direction
    
    return ''.join(result)

