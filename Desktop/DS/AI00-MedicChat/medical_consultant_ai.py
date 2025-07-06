import os
import google.generativeai as genai
import time

# --- KONFIGURASI ---
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"  # Ganti dengan kunci API Google Anda

# --- Inisialisasi Klien Google AI ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"Error initializing Google AI client: {e}")
    exit()

# --- PROMPT SISTEM (DASAR) ---
SYSTEM_PROMPT = """
Anda adalah "Asisten Kesehatan AI", sebuah program yang dirancang untuk memberikan informasi kesehatan umum. Peran Anda adalah sebagai konsultan informatif, BUKAN sebagai dokter.

ATURAN PALING PENTING:
1.  JANGAN PERNAH memberikan diagnosis medis, resep obat, atau anjuran pengobatan yang pasti.
2.  SELALU gunakan frasa seperti "kemungkinan", "bisa jadi merupakan gejala dari", "umumnya disebabkan oleh", atau "opsi pengobatan yang mungkin ada".
3.  SELALU akhiri setiap respons yang berhubungan dengan kondisi medis dengan penafian yang jelas: "Informasi ini bukan pengganti nasihat medis profesional. Silakan berkonsultasi dengan dokter untuk diagnosis dan penanganan yang tepat."
4.  Jaga nada bicara agar tetap empatik, tenang, dan informatif.
"""

# <-- PERUBAHAN UTAMA 1: INSTRUKSI SPESIFIK UNTUK SETIAP MODE -->
MODE_INSTRUCTIONS = {
    "diagnosis": """
    INSTRUKSI MODE SAAT INI: Anda berada dalam 'Mode Analisis Gejala'. 
    Fokuslah untuk membantu pengguna memahami kemungkinan-kemungkinan penyebab dari gejala yang mereka sebutkan. Ajukan pertanyaan klarifikasi yang relevan jika diperlukan untuk mendapatkan gambaran yang lebih jelas (misalnya: "Sudah berapa lama Anda merasakan ini?", "Apakah ada gejala lain yang menyertai?"). Analisis informasi secara logis.
    """,
    "pencegahan": """
    INSTRUKSI MODE SAAT INI: Anda berada dalam 'Mode Pencegahan'. 
    Fokuslah untuk memberikan tips, saran, dan informasi praktis tentang gaya hidup sehat, diet, olahraga, dan langkah-langkah proaktif lain untuk mencegah penyakit sesuai dengan topik yang ditanyakan pengguna. Berikan jawaban yang actionable dan mudah diikuti.
    """,
    "penyembuhan": """
    INSTRUKSI MODE SAAT INI: Anda berada dalam 'Mode Informasi Perawatan'. 
    Jelaskan opsi-opsi perawatan atau manajemen umum yang ada untuk suatu kondisi. Anda bisa menjelaskan cara kerja perawatan, manfaatnya, dan efek sampingnya secara umum. Jangan pernah merekomendasikan atau meresepkan satu perawatan spesifik di atas yang lain.
    """
}

# Menyimpan riwayat percakapan
conversation_history = {
    "diagnosis": [],
    "pencegahan": [],
    "penyembuhan": [],
    "eksplorasi": []
}

def get_ai_response(user_input, mode):
    global conversation_history
    
    conversation_history[mode].append({"role": "user", "content": user_input})
    
    # <-- PERUBAHAN UTAMA 2: GABUNGKAN PROMPT DASAR DENGAN INSTRUKSI MODE -->
    mode_instruction = MODE_INSTRUCTIONS.get(mode, "") # Gunakan string kosong jika mode 'eksplorasi'
    final_system_prompt = f"{SYSTEM_PROMPT}\n{mode_instruction}"

    # Susun pesan untuk API
    messages_to_send = [
        {'role': 'user', 'parts': [final_system_prompt]},
        {'role': 'model', 'parts': ["Tentu, saya mengerti peran saya sesuai instruksi. Silakan mulai."]}
    ]
    
    for message in conversation_history[mode]:
        role = "model" if message["role"] == "assistant" else "user"
        messages_to_send.append({"role": role, "parts": [message["content"]]})

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(messages_to_send)
        ai_response = response.text
        
        conversation_history[mode].append({"role": "assistant", "content": ai_response})
        
        return ai_response
    except Exception as e:
        return f"Maaf, terjadi kesalahan saat menghubungi Google AI: {e}"

# --- Sisa kode tidak ada perubahan ---
def print_disclaimer():
    print("\n" + "="*60)
    print("!!! PENAFIAN PENTING !!!")
    print("Saya adalah Asisten Kesehatan AI dan bukan seorang dokter.")
    # ... sisa teks disclaimer ...
    print("Selalu konsultasikan masalah kesehatan Anda dengan dokter atau profesional medis yang berkualifikasi.")
    print("="*60 + "\n")

def display_menu():
    print("Selamat datang di Konsultan Medis AI.")
    print("Silakan pilih mode percakapan:")
    print("1. Diagnosis (Membantu menganalisis gejala)")
    print("2. Pencegahan (Memberikan tips pencegahan penyakit)")
    print("3. Penyembuhan (Informasi perawatan umum)")
    print("4. Eksplorasi (Diskusi bebas tentang kesehatan)")
    print("5. Keluar")
    return input("Masukkan pilihan Anda (1-5): ")

def chat_loop(mode, mode_name):
    print_disclaimer()
    print(f"--- Anda sekarang dalam Mode: {mode_name} ---")
    print("Ketik 'menu' untuk kembali ke menu utama, atau 'keluar' untuk berhenti.")
    
    conversation_history[mode].clear()

    while True:
        user_input = input("Anda: ")
        if user_input.lower() == 'menu':
            break
        if user_input.lower() == 'keluar':
            exit()
        
        print("\nAsisten AI sedang berpikir...")
        response = get_ai_response(user_input, mode)
        
        for char in response:
            print(char, end='', flush=True)
            time.sleep(0.01)
        print("\n")

def main():
    while True:
        choice = display_menu()
        if choice == '1':
            chat_loop("diagnosis", "Analisis Gejala (Diagnosis)")
        elif choice == '2':
            chat_loop("pencegahan", "Pencegahan Penyakit")
        elif choice == '3':
            chat_loop("penyembuhan", "Informasi Perawatan (Penyembuhan)")
        elif choice == '4':
            chat_loop("eksplorasi", "Eksplorasi")
        elif choice == '5':
            print("Terima kasih telah menggunakan layanan ini. Jaga kesehatan selalu!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()