"""
Pigpen Cipher Algoritması
"""

PIGPEN_MAP = {
    'A': '┌─┐\n│ │\n└─┘', 'B': '┌─┐\n│·│\n└─┘', 'C': '┌─┐\n│·│\n└─┘',
    'D': '┌─┐\n│ │\n└─┘', 'E': '┌─┐\n│·│\n└─┘', 'F': '┌─┐\n│·│\n└─┘',
    'G': '┌─┐\n│ │\n└─┘', 'H': '┌─┐\n│·│\n└─┘', 'I': '┌─┐\n│·│\n└─┘',
    'J': '┌─┐\n│ │\n└─┘', 'K': '┌─┐\n│·│\n└─┘', 'L': '┌─┐\n│·│\n└─┘',
    'M': '┌─┐\n│ │\n└─┘', 'N': '┌─┐\n│·│\n└─┘', 'O': '┌─┐\n│·│\n└─┘',
    'P': '┌─┐\n│ │\n└─┘', 'Q': '┌─┐\n│·│\n└─┘', 'R': '┌─┐\n│·│\n└─┘',
    'S': '┌─┐\n│ │\n└─┘', 'T': '┌─┐\n│·│\n└─┘', 'U': '┌─┐\n│·│\n└─┘',
    'V': '┌─┐\n│ │\n└─┘', 'W': '┌─┐\n│·│\n└─┘', 'X': '┌─┐\n│·│\n└─┘',
    'Y': '┌─┐\n│ │\n└─┘', 'Z': '┌─┐\n│·│\n└─┘'
}

# Basitleştirilmiş Pigpen mapping (gerçek semboller yerine kod)
PIGPEN_SIMPLE = {
    'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6',
    'G': '7', 'H': '8', 'I': '9', 'J': '10', 'K': '11', 'L': '12',
    'M': '13', 'N': '14', 'O': '15', 'P': '16', 'Q': '17', 'R': '18',
    'S': '19', 'T': '20', 'U': '21', 'V': '22', 'W': '23', 'X': '24',
    'Y': '25', 'Z': '26'
}

REVERSE_PIGPEN = {v: k for k, v in PIGPEN_SIMPLE.items()}


def pigpen_encrypt(text):
    """
    Pigpen cipher ile metni şifreler.
    
    Args:
        text: Şifrelenecek metin
    
    Returns:
        Şifrelenmiş metin (kod numaraları)
    """
    text = text.upper().replace(' ', '')
    result = ""
    
    for char in text:
        if char.isalpha():
            result += PIGPEN_SIMPLE.get(char, char) + " "
        else:
            result += char
    
    return result.strip()


def pigpen_decrypt(text):
    """
    Pigpen cipher ile metni çözer.
    
    Args:
        text: Çözülecek metin (kod numaraları)
    
    Returns:
        Çözülmüş metin
    """
    parts = text.split()
    result = ""
    
    for part in parts:
        if part.isdigit() and part in REVERSE_PIGPEN:
            result += REVERSE_PIGPEN[part]
        else:
            result += part
    
    return result

