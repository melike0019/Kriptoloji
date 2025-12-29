import struct

# --- 1. STANDART DES TABLOLARI (Sabitler) ---

# Initial Permutation (IP)
IP_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
]

# Final Permutation (IP^-1)
FP_TABLE = [
    40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
]

# Expansion Table (E)
E_TABLE = [
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1
]

# Permutation Function (P)
P_TABLE = [
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25
]

# Key Permutation 1 (PC-1) - 64 bit anahtarı 56 bite düşürür
PC1_TABLE = [
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2,
    59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39,
    31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37,
    29, 21, 13, 5, 28, 20, 12, 4
]

# Key Permutation 2 (PC-2) - 56 bitten 48 bitlik round key üretir
PC2_TABLE = [
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
    26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
    51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
]

# Key Shift Schedule (Hangi turda kaç bit kayacak)
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# S-Box'lar (Standart DES S-Box Değerleri )
S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# --- 2. YARDIMCI BİT FONKSİYONLARI ---

def str_to_bit_array(text_bytes):
    """Byte dizisini bit dizisine (0 ve 1'lerden oluşan liste) çevirir."""
    bits = []
    for byte in text_bytes:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bit_array_to_bytes(bits):
    """Bit dizisini byte dizisine çevirir."""
    byte_arr = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        byte_arr.append(byte)
    return bytes(byte_arr)

def permute(bits, table):
    """Bitleri verilen tabloya göre karıştırır."""
    return [bits[pos - 1] for pos in table]

def xor(bits1, bits2):
    """İki bit dizisini XOR'lar."""
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def left_shift(bits, n):
    """Bitleri sola dairesel kaydırır."""
    return bits[n:] + bits[:n]

# --- 3. ANAHTAR ÜRETİMİ (Standard Key Schedule) ---

def generate_round_keys(key_text):
    # Anahtarı 8 byte'a tamamla veya kırp
    key_bytes = key_text.encode('utf-8')
    key_bytes = key_bytes[:8].ljust(8, b'\x00')
    
    key_bits = str_to_bit_array(key_bytes)
    
    # PC-1 Permütasyonu (64 bit -> 56 bit)
    key_bits = permute(key_bits, PC1_TABLE)
    
    # İkiye böl (C ve D)
    C = key_bits[:28]
    D = key_bits[28:]
    
    round_keys = []
    for shift in SHIFT_SCHEDULE:
        # Kaydırma
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        
        # Birleştir ve PC-2 Permütasyonu (56 bit -> 48 bit)
        cd_combined = C + D
        round_key = permute(cd_combined, PC2_TABLE)
        round_keys.append(round_key)
        
    return round_keys

# --- 4. FEISTEL VE ROUND İŞLEMLERİ ---

def substitute(expanded_bits):
    """48 bitlik girdiyi S-Box'lardan geçirip 32 bit çıktı üretir."""
    output = []
    # 48 bit, 6 bitlik 8 parçaya bölünür
    for i in range(8):
        chunk = expanded_bits[i*6 : (i+1)*6]
        
        # İlk ve son bit satırı, ortadaki 4 bit sütunu belirler
        row = (chunk[0] << 1) | chunk[5]
        col = (chunk[1] << 3) | (chunk[2] << 2) | (chunk[3] << 1) | chunk[4]
        
        val = S_BOXES[i][row][col]
        
        # Değeri 4 bitlik binary'ye çevirip ekle
        for j in range(3, -1, -1):
            output.append((val >> j) & 1)
    return output

def des_block_encrypt(block_bits, round_keys):
    # 1. Initial Permutation (IP)
    block_bits = permute(block_bits, IP_TABLE)
    
    # 2. Bölme (L0, R0)
    L = block_bits[:32]
    R = block_bits[32:]
    
    # 3. 16 Round
    for r_key in round_keys:
        L_prev = L
        
        # Feistel Fonksiyonu (F)
        # a. Expansion (32 bit -> 48 bit)
        expanded_R = permute(R, E_TABLE)
        
        # b. XOR with Round Key
        xored = xor(expanded_R, r_key)
        
        # c. S-Box Substitution (48 bit -> 32 bit)
        substituted = substitute(xored)
        
        # d. P Permutation (32 bit -> 32 bit)
        f_result = permute(substituted, P_TABLE)
        
        # e. XOR with Left
        new_R = xor(L_prev, f_result)
        
        # f. Swap (Sonraki tur için L = R, R = New_R)
        L = R
        R = new_R
    
    # Not: Standart DES'te son turdan sonra L ve R yer değişmez (veya ters çevrilir).
    # Genellikle R16 L16 olarak birleşir.
    final_block = R + L
    
    # 4. Final Permutation (IP^-1)
    final_block = permute(final_block, FP_TABLE)
    
    return final_block

# --- 5. ANA FONKSİYONLAR (Padding & Main) ---

def pkcs7_pad(data):
    """Standart PKCS7 Padding."""
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data):
    """PKCS7 Padding kaldırma."""
    pad_len = data[-1]
    return data[:-pad_len]

def manual_des_encrypt(plaintext, key):
    # 1. Padding (PKCS7)
    plaintext_bytes = plaintext.encode('utf-8')
    padded_text = pkcs7_pad(plaintext_bytes)
    
    # 2. Anahtarları Hazırla (16 adet)
    round_keys = generate_round_keys(key)
    
    encrypted_bits = []
    
    # 3. Blok Blok Şifrele
    for i in range(0, len(padded_text), 8):
        block = padded_text[i:i+8]
        block_bits = str_to_bit_array(block)
        
        enc_block = des_block_encrypt(block_bits, round_keys)
        encrypted_bits.extend(enc_block)
        
    # 4. Sonucu Hex'e çevir
    encrypted_bytes = bit_array_to_bytes(encrypted_bits)
    return encrypted_bytes.hex().upper()

def manual_des_decrypt(ciphertext_hex, key):
    # Hex decode
    ciphertext = bytes.fromhex(ciphertext_hex)
    
    # Anahtarları Hazırla ve TERS ÇEVİR (16 adet)
    round_keys = generate_round_keys(key)
    round_keys = round_keys[::-1] # Decrypt için ters sıra
    
    decrypted_bits = []
    
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        block_bits = str_to_bit_array(block)
        
        # Decrypt işlemi Encrypt ile aynıdır, sadece anahtar sırası terstir
        dec_block = des_block_encrypt(block_bits, round_keys)
        decrypted_bits.extend(dec_block)
        
    decrypted_bytes = bit_array_to_bytes(decrypted_bits)
    
    # Padding kaldır
    try:
        return pkcs7_unpad(decrypted_bytes).decode('utf-8')
    except:
        return "[Hata] Padding bozuk veya yanlış anahtar."

# --- TEST KISMI ---
if __name__ == "__main__":
    metin = "Kriptoloji Final Sunumu"
    anahtar = "MyKey123"
    
    print(f"Metin: {metin}")
    print(f"Key  : {anahtar}")
    print("-" * 30)
    
    # Şifreleme
    encrypted = manual_des_encrypt(metin, anahtar)
    print(f"Standard DES Çıktısı (Hex): {encrypted}")
    
    # Çözme
    decrypted = manual_des_decrypt(encrypted, anahtar)
    print(f"Çözülmüş Metin: {decrypted}")
