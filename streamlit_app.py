"""
Kriptoloji Projesi - Streamlit Kullanıcı Arayüzü
Klasik ve Modern Kriptografi Algoritmaları
"""

import sys
import os

# Proje root'unu Python path'ine ekle
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import base64
import numpy as np

# Klasik şifreleme algoritmaları
from classical_ciphers import (
    caesar_encrypt, caesar_decrypt,
    substitution_encrypt, substitution_decrypt, generate_key,
    vigenere_encrypt, vigenere_decrypt,
    rail_fence_encrypt, rail_fence_decrypt,
    columnar_transposition_encrypt, columnar_transposition_decrypt,
    route_cipher_encrypt, route_cipher_decrypt,
    playfair_encrypt, playfair_decrypt,
    polybius_encrypt, polybius_decrypt,
    pigpen_encrypt, pigpen_decrypt,
    hill_encrypt, hill_decrypt
)

# Modern şifreleme algoritmaları
from modern_ciphers import aes_encrypt, aes_decrypt, des_encrypt, des_decrypt

# Manuel DES
from manual_des import manual_des_encrypt, manual_des_decrypt

# Sayfa yapılandırması
st.set_page_config(
    page_title="Kriptoloji Projesi",
    page_icon="🔐",
    layout="wide"
)

# Ana başlık
st.title("🔐 Kriptoloji Projesi - Final")
st.markdown("---")

# Sidebar - Algoritma seçimi
st.sidebar.title("Algoritma Seçimi")
algorithm_type = st.sidebar.radio(
    "Şifreleme Türü",
    ["Klasik Kriptografi", "Modern Kriptografi","Manuel DES"]
)

# Klasik Kriptografi
if algorithm_type == "Klasik Kriptografi":
    st.header("📜 Klasik Kriptografi Algoritmaları")
    
    classical_algorithm = st.selectbox(
        "Algoritma Seçin",
        [
            "Sezar Şifreleme",
            "Substitution Cipher",
            "Vigenère Cipher",
            "Rail Fence Cipher",
            "Columnar Transposition",
            "Route Cipher",
            "Playfair Cipher",
            "Polybius Cipher",
            "Pigpen Cipher",
            "Hill Cipher"
        ]
    )
    
    operation = st.radio("İşlem", ["Şifrele", "Çöz"], horizontal=True)
    
    text_input = st.text_area("Metin", height=100)
    
    # Algoritmaya göre parametreler
    if classical_algorithm == "Sezar Şifreleme":
        shift = st.slider("Kaydırma Miktarı", 0, 25, 3)
        
        if st.button("Uygula"):
            if text_input:
                if operation == "Şifrele":
                    result = caesar_encrypt(text_input, shift)
                    st.success("Şifrelenmiş Metin:")
                    st.code(result, language=None)
                else:
                    result = caesar_decrypt(text_input, shift)
                    st.success("Çözülmüş Metin:")
                    st.code(result, language=None)
    
    elif classical_algorithm == "Substitution Cipher":
        if 'sub_key' not in st.session_state:
            st.session_state.sub_key = generate_key()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yeni Anahtar Oluştur"):
                st.session_state.sub_key = generate_key()
        
        with col2:
            st.write("**Anahtar:**", str(st.session_state.sub_key)[:50] + "...")
        
        if st.button("Uygula"):
            if text_input:
                if operation == "Şifrele":
                    result = substitution_encrypt(text_input, st.session_state.sub_key)
                    st.success("Şifrelenmiş Metin:")
                    st.code(result, language=None)
                else:
                    result = substitution_decrypt(text_input, st.session_state.sub_key)
                    st.success("Çözülmüş Metin:")
                    st.code(result, language=None)
    
    elif classical_algorithm == "Vigenère Cipher":
        key = st.text_input("Anahtar Kelime", "KEY")
        
        if st.button("Uygula"):
            if text_input and key:
                if operation == "Şifrele":
                    result = vigenere_encrypt(text_input, key)
                    st.success("Şifrelenmiş Metin:")
                    st.code(result, language=None)
                else:
                    result = vigenere_decrypt(text_input, key)
                    st.success("Çözülmüş Metin:")
                    st.code(result, language=None)
    
    elif classical_algorithm == "Rail Fence Cipher":
        rails = st.slider("Ray Sayısı", 2, 10, 3)
        
        if st.button("Uygula"):
            if text_input:
                if operation == "Şifrele":
                    result = rail_fence_encrypt(text_input, rails)
                    st.success("Şifrelenmiş Metin:")
                    st.code(result, language=None)
                else:
                    result = rail_fence_decrypt(text_input, rails)
                    st.success("Çözülmüş Metin:")
                    st.code(result, language=None)
    
    elif classical_algorithm == "Columnar Transposition":
        key = st.text_input("Anahtar Kelime", "KEY")
        
        if st.button("Uygula"):
            if text_input and key:
                if operation == "Şifrele":
                    result = columnar_transposition_encrypt(text_input, key)
                    st.success("Şifrelenmiş Metin:")
                    st.code(result, language=None)
                else:
                    result = columnar_transposition_decrypt(text_input, key)
                    st.success("Çözülmüş Metin:")
                    st.code(result, language=None)
    
    elif classical_algorithm == "Route Cipher":
        col1, col2, col3 = st.columns(3)
        with col1:
            rows = st.number_input("Satır Sayısı", 2, 10, 4)
        with col2:
            cols = st.number_input("Sütun Sayısı", 2, 10, 4)
        with col3:
            route = st.selectbox("Okuma Yolu", ["spiral", "snake", "column"])
        
        if st.button("Uygula"):
            if text_input:
                if operation == "Şifrele":
                    result = route_cipher_encrypt(text_input, rows, cols, route)
                    st.success("Şifrelenmiş Metin:")
                    st.code(result, language=None)
                else:
                    result = route_cipher_decrypt(text_input, rows, cols, route)
                    st.success("Çözülmüş Metin:")
                    st.code(result, language=None)
    
    elif classical_algorithm == "Playfair Cipher":
        key = st.text_input("Anahtar Kelime", "PLAYFAIR")
        
        if st.button("Uygula"):
            if text_input and key:
                if operation == "Şifrele":
                    result = playfair_encrypt(text_input, key)
                    st.success("Şifrelenmiş Metin:")
                    st.code(result, language=None)
                else:
                    result = playfair_decrypt(text_input, key)
                    st.success("Çözülmüş Metin:")
                    st.code(result, language=None)
    
    elif classical_algorithm == "Polybius Cipher":
        key = st.text_input("Anahtar Kelime (Opsiyonel)", "")
        
        if st.button("Uygula"):
            if text_input:
                if operation == "Şifrele":
                    result = polybius_encrypt(text_input, key)
                    st.success("Şifrelenmiş Metin:")
                    st.code(result, language=None)
                else:
                    result = polybius_decrypt(text_input, key)
                    st.success("Çözülmüş Metin:")
                    st.code(result, language=None)
    
    elif classical_algorithm == "Pigpen Cipher":
        if st.button("Uygula"):
            if text_input:
                if operation == "Şifrele":
                    result = pigpen_encrypt(text_input)
                    st.success("Şifrelenmiş Metin:")
                    st.code(result, language=None)
                else:
                    result = pigpen_decrypt(text_input)
                    st.success("Çözülmüş Metin:")
                    st.code(result, language=None)
    
    elif classical_algorithm == "Hill Cipher":
        st.write("2x2 Anahtar Matrisi:")
        col1, col2 = st.columns(2)
        with col1:
            a = st.number_input("a", value=3, min_value=0, max_value=25)
            b = st.number_input("b", value=3, min_value=0, max_value=25)
        with col2:
            c = st.number_input("c", value=2, min_value=0, max_value=25)
            d = st.number_input("d", value=5, min_value=0, max_value=25)
        
        key_matrix = [[a, b], [c, d]]
        
        if st.button("Uygula"):
            if text_input:
                try:
                    if operation == "Şifrele":
                        result = hill_encrypt(text_input, key_matrix)
                        st.success("Şifrelenmiş Metin:")
                        st.code(result, language=None)
                    else:
                        result = hill_decrypt(text_input, key_matrix)
                        st.success("Çözülmüş Metin:")
                        st.code(result, language=None)
                except Exception as e:
                    st.error(f"Hata: {str(e)}")

# Modern Kriptografi
elif algorithm_type == "Modern Kriptografi":
    st.header("🔒 Modern Kriptografi Algoritmaları")
    
    modern_algorithm = st.selectbox(
        "Algoritma Seçin",
        ["AES-128", "DES"]
    )
    
    operation = st.radio("İşlem", ["Şifrele", "Çöz"], horizontal=True)
    
    text_input = st.text_area("Metin", height=100)
    
    key_input = st.text_input("Anahtar (16 karakter AES için, 8 karakter DES için)", "MySecretKey1234")
    
    if modern_algorithm == "AES-128":
        if operation == "Şifrele":
            if st.button("Şifrele"):
                if text_input:
                    try:
                        key = key_input[:16].encode('utf-8').ljust(16, b'0')
                        iv, ciphertext = aes_encrypt(text_input, key)
                        
                        st.success("Şifreleme Başarılı!")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**IV (Base64):**")
                            st.code(base64.b64encode(iv).decode(), language=None)
                        with col2:
                            st.write("**Şifrelenmiş Veri (Base64):**")
                            st.code(base64.b64encode(ciphertext).decode(), language=None)
                        
                        # Session state'e kaydet
                        st.session_state.aes_iv = base64.b64encode(iv).decode()
                        st.session_state.aes_ciphertext = base64.b64encode(ciphertext).decode()
                        st.session_state.aes_key = key_input[:16]
                    except Exception as e:
                        st.error(f"Hata: {str(e)}")
        else:
            iv_b64 = st.text_input("IV (Base64)", st.session_state.get('aes_iv', ''))
            ciphertext_b64 = st.text_input("Şifrelenmiş Veri (Base64)", st.session_state.get('aes_ciphertext', ''))
            
            if st.button("Çöz"):
                if iv_b64 and ciphertext_b64 and key_input:
                    try:
                        key = key_input[:16].encode('utf-8').ljust(16, b'0')
                        iv = base64.b64decode(iv_b64)
                        ciphertext = base64.b64decode(ciphertext_b64)
                        
                        plaintext = aes_decrypt(iv, ciphertext, key)
                        st.success("Çözme Başarılı!")
                        st.write("**Çözülmüş Metin:**")
                        st.code(plaintext, language=None)
                    except Exception as e:
                        st.error(f"Hata: {str(e)}")
    
    elif modern_algorithm == "DES":
        if operation == "Şifrele":
            if st.button("Şifrele"):
                if text_input:
                    try:
                        key = key_input[:8].encode('utf-8').ljust(8, b'0')
                        iv, ciphertext = des_encrypt(text_input, key)
                        
                        st.success("Şifreleme Başarılı!")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**IV (Base64):**")
                            st.code(base64.b64encode(iv).decode(), language=None)
                        with col2:
                            st.write("**Şifrelenmiş Veri (Base64):**")
                            st.code(base64.b64encode(ciphertext).decode(), language=None)
                        
                        st.session_state.des_iv = base64.b64encode(iv).decode()
                        st.session_state.des_ciphertext = base64.b64encode(ciphertext).decode()
                        st.session_state.des_key = key_input[:8]
                    except Exception as e:
                        st.error(f"Hata: {str(e)}")
        else:
            iv_b64 = st.text_input("IV (Base64)", st.session_state.get('des_iv', ''))
            ciphertext_b64 = st.text_input("Şifrelenmiş Veri (Base64)", st.session_state.get('des_ciphertext', ''))
            
            if st.button("Çöz"):
                if iv_b64 and ciphertext_b64 and key_input:
                    try:
                        key = key_input[:8].encode('utf-8').ljust(8, b'0')
                        iv = base64.b64decode(iv_b64)
                        ciphertext = base64.b64decode(ciphertext_b64)
                        
                        plaintext = des_decrypt(iv, ciphertext, key)
                        st.success("Çözme Başarılı!")
                        st.write("**Çözülmüş Metin:**")
                        st.code(plaintext, language=None)
                    except Exception as e:
                        st.error(f"Hata: {str(e)}")



# Manuel DES
elif algorithm_type == "Manuel DES":
    st.header("🛠️ Manuel DES (Sadeleştirilmiş)")
    st.info("Bu implementasyon eğitim amaçlıdır. Gerçek DES standardını birebir uygulamaz. Feistel Network, S-Box ve Permütasyonlar gibi temel yapı taşlarını içerir.")
    
    operation = st.radio("İşlem", ["Şifrele", "Çöz"], horizontal=True)
    
    text_input = st.text_area("Metin", height=100)
    key_input = st.text_input("Anahtar (8 karakter)", "MyKey123")
    
    if operation == "Şifrele":
        if st.button("Şifrele"):
            if text_input and key_input:
                try:
                    key = key_input[:8].ljust(8, '0')
                    ciphertext_hex = manual_des_encrypt(text_input, key)
                    st.success("Şifreleme Başarılı!")
                    st.write("**Şifrelenmiş Metin (Hex):**")
                    st.code(ciphertext_hex, language=None)
                    st.session_state.manual_des_ciphertext = ciphertext_hex
                    st.session_state.manual_des_key = key
                except Exception as e:
                    st.error(f"Hata: {str(e)}")
    else:
        ciphertext_hex = st.text_input("Şifrelenmiş Metin (Hex)", st.session_state.get('manual_des_ciphertext', ''))
        
        if st.button("Çöz"):
            if ciphertext_hex and key_input:
                try:
                    key = key_input[:8].ljust(8, '0')
                    plaintext = manual_des_decrypt(ciphertext_hex, key)
                    st.success("Çözme Başarılı!")
                    st.write("**Çözülmüş Metin:**")
                    st.code(plaintext, language=None)
                except Exception as e:
                    st.error(f"Hata: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Kriptoloji Final Projesi** - Klasik ve Modern Kriptografi Algoritmaları")

