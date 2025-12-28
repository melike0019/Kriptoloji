"""
Kriptoloji Projesi - İstemci Uygulaması
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
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from modern_ciphers import aes_encrypt, des_encrypt


class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.public_key = None
    
    def connect(self):
        """Sunucuya bağlanır."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
            print(f"✓ Sunucuya bağlandı: {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Bağlantı hatası: {str(e)}")
            return False
    
    def receive_public_key(self):
        """Sunucudan açık anahtarı alır."""
        try:
            # Socket timeout ayarla
            self.socket.settimeout(10.0)
            
            # Kısa bir bekleme (sunucunun veriyi göndermesi için)
            time.sleep(0.3)
            
            # Veriyi al - daha basit yaklaşım
            data = b''
            chunk = None
            
            # İlk chunk'ı al
            try:
                chunk = self.socket.recv(8192)  # Daha büyük buffer
                if chunk:
                    data += chunk
            except socket.timeout:
                print("Timeout: Sunucudan veri gelmedi")
                return False
            
            # Eğer veri küçükse, daha fazla veri olabilir
            if len(data) < 1000:  # RSA public key genellikle daha büyüktür
                try:
                    # Non-blocking moda geç
                    self.socket.settimeout(0.1)
                    while True:
                        try:
                            chunk = self.socket.recv(8192)
                            if not chunk:
                                break
                            data += chunk
                        except socket.timeout:
                            break  # Daha fazla veri yok
                except:
                    pass
            
            if not data:
                print("Hata: Sunucudan veri alınamadı")
                return False
            
            # JSON'u parse et
            try:
                decoded = data.decode('utf-8')
                key_message = json.loads(decoded)
            except json.JSONDecodeError as e:
                print(f"Hata: JSON parse edilemedi: {str(e)}")
                print(f"Alınan veri uzunluğu: {len(data)} byte")
                print(f"Alınan veri (ilk 500 karakter): {data[:500]}")
                return False
            except UnicodeDecodeError as e:
                print(f"Hata: Unicode decode hatası: {str(e)}")
                return False
            
            if key_message.get('type') == 'public_key':
                public_key_pem = key_message['public_key'].encode('utf-8')
                self.public_key = serialization.load_pem_public_key(
                    public_key_pem,
                    backend=default_backend()
                )
                print("✓ Açık anahtar alındı")
                return True
            else:
                print(f"Hata: Beklenmeyen mesaj tipi: {key_message.get('type')}")
                print(f"Mesaj içeriği: {str(key_message)[:200]}")
                return False
        except Exception as e:
            print(f"Hata: Açık anahtar alınırken hata oluştu: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def encrypt_symmetric_key(self, symmetric_key):
        """Simetrik anahtarı RSA ile şifreler."""
        encrypted_key = self.public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_key).decode('utf-8')
    
    def send_encrypted_message(self, message, algorithm='AES'):
        """
        Şifrelenmiş mesajı sunucuya gönderir.
        
        Args:
            message: Gönderilecek mesaj
            algorithm: 'AES', 'DES' veya 'RSA'
        """
        if algorithm == 'RSA':
            # RSA ile direkt mesaj şifreleme
            print(f"Mesaj RSA ile şifreleniyor...")
            
            # Mesajı parçalara böl (RSA 2048 bit = 245 byte max)
            max_chunk_size = 245
            message_bytes = message.encode('utf-8')
            encrypted_chunks = []
            
            for i in range(0, len(message_bytes), max_chunk_size):
                chunk = message_bytes[i:i+max_chunk_size]
                encrypted_chunk = self.public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                encrypted_chunks.append(base64.b64encode(encrypted_chunk).decode('utf-8'))
            
            print("✓ Mesaj RSA ile şifrelendi")
            
            # RSA şifreli mesajı gönder
            message_data = {
                'type': 'rsa_encrypted_message',
                'algorithm': 'RSA',
                'chunks': encrypted_chunks
            }
            message_json = json.dumps(message_data)
            message_bytes = message_json.encode('utf-8')
            
            # Veriyi parça parça gönder (büyük mesajlar için)
            total_sent = 0
            while total_sent < len(message_bytes):
                try:
                    sent = self.socket.send(message_bytes[total_sent:])
                    if sent == 0:
                        raise RuntimeError("Socket baglantisi kesildi")
                    total_sent += sent
                except Exception as e:
                    print(f"Hata: Mesaj gonderilirken hata: {str(e)}")
                    raise
            
            print("✓ Şifrelenmiş mesaj gönderildi")
            
        else:
            # Simetrik anahtar oluştur
            if algorithm == 'AES':
                symmetric_key = os.urandom(16)
            elif algorithm == 'DES':
                symmetric_key = os.urandom(8)
            else:
                raise ValueError("Algoritma 'AES', 'DES' veya 'RSA' olmalıdır")
            
            print(f"\nSimetrik anahtar oluşturuldu: {symmetric_key.hex()[:32]}...")
            
            # Mesajı şifrele
            print(f"Mesaj şifreleniyor ({algorithm})...")
            if algorithm == 'AES':
                iv, ciphertext = aes_encrypt(message, symmetric_key)
            else:
                iv, ciphertext = des_encrypt(message, symmetric_key)
            
            print("✓ Mesaj şifrelendi")
            
            # Simetrik anahtarı RSA ile şifrele
            print("Simetrik anahtar RSA ile şifreleniyor...")
            encrypted_key_b64 = self.encrypt_symmetric_key(symmetric_key)
            print("✓ Simetrik anahtar şifrelendi")
            
            # Şifrelenmiş anahtarı gönder
            key_data = {
                'type': 'encrypted_key',
                'algorithm': algorithm,
                'encrypted_key': encrypted_key_b64
            }
            key_json = json.dumps(key_data)
            self.socket.sendall(key_json.encode('utf-8'))
            print("✓ Şifrelenmiş anahtar gönderildi")
            
            # Kısa bir bekleme (sunucunun veriyi alması için)
            import time
            time.sleep(0.1)
            
            # Şifrelenmiş mesajı gönder
            message_data = {
                'type': 'encrypted_message',
                'iv': base64.b64encode(iv).decode('utf-8'),
                'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
            }
            message_json = json.dumps(message_data)
            self.socket.sendall(message_json.encode('utf-8'))
            print("✓ Şifrelenmiş mesaj gönderildi")
        
        # Sunucudan onay al
        response = self.socket.recv(4096).decode('utf-8')
        response_data = json.loads(response)
        
        if response_data['type'] == 'ack':
            print(f"\n✓ Sunucu onayı: {response_data['message']}")
        
        return True
    
    def disconnect(self):
        """Sunucu bağlantısını kapatır."""
        if self.socket:
            self.socket.close()
            print("Bağlantı kapatıldı")


def main():
    """Ana istemci fonksiyonu."""
    print(f"\n{'='*60}")
    print("KRİPTOLOJİ PROJESİ - İSTEMCİ UYGULAMASI")
    print(f"{'='*60}\n")
    
    client = Client()
    
    if not client.connect():
        return
    
    # Açık anahtarı al
    if not client.receive_public_key():
        print("Açık anahtar alınamadı!")
        client.disconnect()
        return
    
    # Kullanıcıdan mesaj al
    print("\n" + "="*60)
    message = input("Gönderilecek mesajı girin: ")
    algorithm = input("Algoritma seçin (AES/DES/RSA) [AES]: ").upper() or "AES"
    
    if algorithm not in ['AES', 'DES', 'RSA']:
        print("Geçersiz algoritma! AES kullanılıyor.")
        algorithm = 'AES'
    
    print(f"\n{'='*60}")
    print(f"Mesaj: {message}")
    print(f"Algoritma: {algorithm}")
    print(f"{'='*60}\n")
    
    # Mesajı gönder
    try:
        client.send_encrypted_message(message, algorithm)
    except Exception as e:
        print(f"Hata: {str(e)}")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()

