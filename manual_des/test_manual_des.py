"""
Manuel DES Test Scripti
Terminal üzerinden test için
"""

import sys
import os

# Proje root'unu Python path'ine ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from manual_des import manual_des_encrypt, manual_des_decrypt


def test_manual_des():
    """Manuel DES'i test eder."""
    print("="*60)
    print("MANUEL DES TEST")
    print("="*60)
    
    # Test verileri
    plaintext = input("\nŞifrelenecek metni girin: ")
    key = input("Anahtarı girin (8 karakter): ").ljust(8, '0')[:8]
    
    print(f"\nOrijinal Metin: {plaintext}")
    print(f"Anahtar: {key}")
    
    # Şifrele
    print("\nŞifreleme yapılıyor...")
    ciphertext_hex = manual_des_encrypt(plaintext, key)
    print(f"Şifrelenmiş Metin (Hex): {ciphertext_hex}")
    
    # Çöz
    print("\nÇözme yapılıyor...")
    decrypted = manual_des_decrypt(ciphertext_hex, key)
    print(f"Çözülmüş Metin: {decrypted}")
    
    # Doğrulama
    print("\n" + "="*60)
    if plaintext == decrypted:
        print("✓ TEST BAŞARILI - Şifreleme ve çözme tersinir!")
    else:
        print("✗ TEST BAŞARISIZ - Metinler eşleşmiyor!")
        print(f"Orijinal: '{plaintext}'")
        print(f"Çözülmüş: '{decrypted}'")
    print("="*60)


if __name__ == "__main__":
    test_manual_des()

