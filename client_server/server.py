"""
Kriptoloji Projesi - Sunucu Uygulaması
RSA ile anahtar dağıtımı ve AES/DES ile şifreli veri iletimi
"""

import sys
import os

# Proje root'unu Python path'ine ekle
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import socket
import json
import base64
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from modern_ciphers import aes_decrypt, des_decrypt


class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None
        
        # RSA anahtar çifti oluştur
        print("RSA anahtar cifti olusturuluyor...")
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        print("✓ RSA anahtar çifti oluşturuldu")
    
    def get_public_key_pem(self):
        """Açık anahtarı PEM formatında döndürür."""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def decrypt_symmetric_key(self, encrypted_key_b64):
        """RSA ile şifrelenmiş simetrik anahtarı çözer."""
        encrypted_key = base64.b64decode(encrypted_key_b64)
        symmetric_key = self.private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return symmetric_key
    
    def start(self):
        """Sunucuyu başlatır."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        
        print(f"\n{'='*60}")
        print(f"Sunucu başlatıldı: {self.host}:{self.port}")
        print(f"{'='*60}\n")
        print("İstemci bağlantısı bekleniyor...")
        
        while True:
            try:
                client_socket, client_address = self.socket.accept()
                print(f"\n✓ İstemci bağlandı: {client_address}")
                
                # Açık anahtarı gönder
                try:
                    public_key_pem = self.get_public_key_pem()
                    key_message = {
                        'type': 'public_key',
                        'public_key': public_key_pem.decode('utf-8')
                    }
                    key_json = json.dumps(key_message)
                    key_bytes = key_json.encode('utf-8')
                    
                    # Veriyi gönder
                    total_sent = 0
                    while total_sent < len(key_bytes):
                        sent = client_socket.send(key_bytes[total_sent:])
                        if sent == 0:
                            raise RuntimeError("Socket baglantisi kesildi")
                        total_sent += sent
                    
                    # Kısa bir bekleme (istemcinin veriyi alması için)
                    time.sleep(0.1)
                    print("✓ Açık anahtar gönderildi")
                except Exception as e:
                    print(f"HATA: Acik anahtar gonderilirken hata: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    client_socket.close()
                    continue
                
                # İstemciden veri al (parça parça)
                # İlk mesajı al (encrypted_key veya rsa_encrypted_message)
                first_data = b''
                client_socket.settimeout(30.0)  # 30 saniye timeout
                
                try:
                    # İlk chunk'ı al
                    chunk = client_socket.recv(8192)
                    if chunk:
                        first_data += chunk
                    
                    # JSON'un tamamlanıp tamamlanmadığını kontrol et
                    client_socket.settimeout(1.0)  # Kısa timeout
                    max_attempts = 20
                    attempts = 0
                    
                    while attempts < max_attempts:
                        try:
                            # JSON'u kontrol et
                            decoded = first_data.decode('utf-8')
                            # İlk JSON'u bul (kapanış parantezini bul)
                            brace_count = 0
                            json_end = -1
                            for i, char in enumerate(decoded):
                                if char == '{':
                                    brace_count += 1
                                elif char == '}':
                                    brace_count -= 1
                                    if brace_count == 0:
                                        json_end = i + 1
                                        break
                            
                            if json_end > 0:
                                # İlk JSON tamamlanmış
                                first_message_str = decoded[:json_end]
                                first_message = json.loads(first_message_str)
                                # Kalan veriyi sakla (varsa)
                                remaining_data = decoded[json_end:].strip()
                                break
                            else:
                                # JSON henüz tamamlanmamış, daha fazla veri bekle
                                chunk = client_socket.recv(8192)
                                if not chunk:
                                    break
                                first_data += chunk
                                attempts = 0
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            # Daha fazla veri bekle
                            try:
                                chunk = client_socket.recv(8192)
                                if not chunk:
                                    attempts += 1
                                    if attempts >= 3:
                                        break
                                    continue
                                first_data += chunk
                                attempts = 0
                            except socket.timeout:
                                attempts += 1
                                if attempts >= 3:
                                    break
                                continue
                        except socket.timeout:
                            # Timeout, mevcut veriyi kontrol et
                            if first_data:
                                try:
                                    decoded = first_data.decode('utf-8')
                                    # İlk JSON'u bul
                                    brace_count = 0
                                    json_end = -1
                                    for i, char in enumerate(decoded):
                                        if char == '{':
                                            brace_count += 1
                                        elif char == '}':
                                            brace_count -= 1
                                            if brace_count == 0:
                                                json_end = i + 1
                                                break
                                    
                                    if json_end > 0:
                                        first_message_str = decoded[:json_end]
                                        first_message = json.loads(first_message_str)
                                        remaining_data = decoded[json_end:].strip()
                                        break
                                except:
                                    pass
                            attempts += 1
                            if attempts >= 3:
                                break
                
                except Exception as e:
                    print(f"Veri alma hatası: {str(e)}")
                    if first_data:
                        print(f"Alinan veri uzunlugu: {len(first_data)} byte")
                    client_socket.close()
                    continue
                
                if not first_data:
                    print("Hata: İstemciden veri alınamadı")
                    client_socket.close()
                    continue
                
                # JSON'u parse et - iki JSON mesajı birleşmiş olabilir
                remaining_data = ""  # Varsayılan değer
                try:
                    decoded = first_data.decode('utf-8')
                    # İlk JSON'u ayır (kapanış parantezini bul)
                    brace_count = 0
                    json_end = -1
                    for i, char in enumerate(decoded):
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                json_end = i + 1
                                break
                    
                    if json_end > 0:
                        # İki JSON mesajı birleşmiş
                        first_message_str = decoded[:json_end]
                        first_message = json.loads(first_message_str)
                        remaining_data = decoded[json_end:].strip()
                    else:
                        # Tek JSON mesajı
                        first_message = json.loads(decoded)
                        remaining_data = ""
                except json.JSONDecodeError as e:
                    # JSON parse hatası - belki iki JSON birleşmiş
                    try:
                        decoded = first_data.decode('utf-8')
                        # İlk JSON'u bul
                        brace_count = 0
                        json_end = -1
                        for i, char in enumerate(decoded):
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    json_end = i + 1
                                    break
                        
                        if json_end > 0:
                            first_message_str = decoded[:json_end]
                            first_message = json.loads(first_message_str)
                            remaining_data = decoded[json_end:].strip()
                        else:
                            raise
                    except:
                        print(f"Hata: JSON parse edilemedi: {str(e)}")
                        print(f"Alinan veri uzunlugu: {len(first_data)} byte")
                        print(f"Alinan veri (ilk 500 karakter): {first_data[:500]}")
                        client_socket.close()
                        continue
                
                if first_message['type'] == 'rsa_encrypted_message':
                    # RSA ile direkt şifrelenmiş mesaj
                    print(f"\nAlgoritma: {first_message['algorithm']}")
                    print("RSA ile şifrelenmiş mesaj alındı, çözülüyor...")
                    
                    encrypted_chunks = first_message['chunks']
                    plaintext_chunks = []
                    
                    for chunk_b64 in encrypted_chunks:
                        encrypted_chunk = base64.b64decode(chunk_b64)
                        decrypted_chunk = self.private_key.decrypt(
                            encrypted_chunk,
                            padding.OAEP(
                                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                algorithm=hashes.SHA256(),
                                label=None
                            )
                        )
                        plaintext_chunks.append(decrypted_chunk)
                    
                    plaintext = b''.join(plaintext_chunks).decode('utf-8')
                    print("✓ Mesaj RSA ile çözüldü")
                    
                else:
                    # Simetrik şifreleme (AES/DES)
                    key_data = first_message
                    print(f"\nAlgoritma: {key_data['algorithm']}")
                    print("Sifrelenmis simetrik anahtar alindi, cozuluyor...")
                    
                    # Simetrik anahtarı çöz
                    try:
                        symmetric_key = self.decrypt_symmetric_key(key_data['encrypted_key'])
                        print(f"[OK] Simetrik anahtar cozuldu: {symmetric_key.hex()[:32]}...")
                    except Exception as e:
                        print(f"Hata: Simetrik anahtar cozulurken hata: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        client_socket.close()
                        continue
                    
                    # Şifrelenmiş mesajı al
                    # Eğer kalan veri varsa onu kullan, yoksa yeni veri al
                    print(f"Kalan veri kontrolu: {len(remaining_data) if remaining_data else 0} karakter")
                    if remaining_data:
                        # Kalan veriden ikinci JSON'u parse et
                        print(f"Kalan veriden mesaj parse ediliyor... ({len(remaining_data)} karakter)")
                        try:
                            message_data = json.loads(remaining_data)
                            print("[OK] Mesaj kalan veriden parse edildi")
                        except json.JSONDecodeError as e:
                            print(f"Kalan veri parse edilemedi: {str(e)}, daha fazla veri aliniyor...")
                            # Kalan veri yeterli değil, daha fazla veri al
                            encrypted_message_data = remaining_data.encode('utf-8')
                            client_socket.settimeout(5.0)
                            while True:
                                try:
                                    chunk = client_socket.recv(4096)
                                    if not chunk:
                                        break
                                    encrypted_message_data += chunk
                                    try:
                                        decoded = encrypted_message_data.decode('utf-8')
                                        message_data = json.loads(decoded)
                                        break
                                    except (json.JSONDecodeError, UnicodeDecodeError):
                                        continue
                                except socket.timeout:
                                    break
                            message_data = json.loads(encrypted_message_data.decode('utf-8'))
                    else:
                        # Yeni veri al
                        print("Yeni mesaj verisi aliniyor...")
                        encrypted_message_data = b''
                        client_socket.settimeout(5.0)
                        while True:
                            try:
                                chunk = client_socket.recv(4096)
                                if not chunk:
                                    break
                                encrypted_message_data += chunk
                                try:
                                    decoded = encrypted_message_data.decode('utf-8')
                                    message_data = json.loads(decoded)
                                    break
                                except (json.JSONDecodeError, UnicodeDecodeError):
                                    continue
                            except socket.timeout:
                                if encrypted_message_data:
                                    try:
                                        message_data = json.loads(encrypted_message_data.decode('utf-8'))
                                        break
                                    except:
                                        pass
                                break
                        
                        if not encrypted_message_data:
                            print("Hata: Şifrelenmiş mesaj alınamadı")
                            client_socket.close()
                            continue
                        
                        message_data = json.loads(encrypted_message_data.decode('utf-8'))
                    
                    iv = base64.b64decode(message_data['iv'])
                    ciphertext = base64.b64decode(message_data['ciphertext'])
                    
                    print("\nSifrelenmis mesaj alindi, cozuluyor...")
                    
                    # Mesajı çöz
                    try:
                        if key_data['algorithm'] == 'AES':
                            plaintext = aes_decrypt(iv, ciphertext, symmetric_key)
                        elif key_data['algorithm'] == 'DES':
                            plaintext = des_decrypt(iv, ciphertext, symmetric_key)
                        else:
                            plaintext = "Bilinmeyen algoritma"
                    except Exception as e:
                        print(f"Hata: Mesaj cozulurken hata olustu: {str(e)}")
                        import traceback
                        traceback.print_exc()
                        client_socket.close()
                        continue
                
                # Çözülmüş mesajı göster
                try:
                    print(f"\n{'='*60}")
                    print("COZULMUS MESAJ:")
                    print(f"{'='*60}")
                    print(plaintext)
                    print(f"{'='*60}\n")
                except Exception as e:
                    print(f"Hata: Mesaj gosterilirken hata: {str(e)}")
                
                # Onay gönder
                response = {
                    'type': 'ack',
                    'message': 'Mesaj başarıyla alındı ve çözüldü'
                }
                response_json = json.dumps(response)
                client_socket.sendall(response_json.encode('utf-8'))
                
                client_socket.close()
                print("İstemci bağlantısı kapatıldı\n")
                
            except KeyboardInterrupt:
                print("\n\nSunucu kapatılıyor...")
                break
            except Exception as e:
                print(f"Hata: {str(e)}")
                if client_socket:
                    client_socket.close()
    
    def stop(self):
        """Sunucuyu durdurur."""
        if self.socket:
            self.socket.close()
            print("Sunucu kapatıldı")


if __name__ == "__main__":
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

