import google.generativeai as genai
import os

# Ganti dengan API key kamu sendiri
# Kamu bisa mendapatkan API key di https://aistudio.google.com/
GOOGLE_API_KEY = ""

try:
    genai.configure(api_key=GOOGLE_API_KEY)
except AttributeError:
    print("Pastikan kamu sudah menginstal pustaka yang benar: pip install google-generativeai")
    exit()

def dapatkan_fakta_angka(nomor_input):
    """
    Menghasilkan fakta unik tentang angka yang diberikan menggunakan Gemini AI.
    """
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    if nomor_input == '667':
        prompt = "Berikan saya satu lelucon singkat dan lucu bahwa angka 667 adalah angka keramat atmin shin."
    else:
        prompt = f"Berikan saya sebuah fakta unik dan menarik tentang angka {nomor_input}. Buatlah penjelasan yang singkat dan mudah dimengerti."

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Terjadi kesalahan saat menghubungi AI: {e}"

def main():
    """
    Fungsi utama untuk menjalankan program.
    """
    print("✨ Selamat datang di program fakta unik tentang angka! ✨")
    print("Masukkan angka yang kamu mau tau untuk mencari fakta uniknya.")

    while True:
        input_pengguna = input("\nMasukkan angka (atau ketik 'keluar' untuk berhenti): ")

        if input_pengguna.lower() == 'keluar':
            print("Terima kasih telah menggunakan program ini. Sampai jumpa! 👋")
            break

        if input_pengguna.isdigit():
            print(f"\n{input_pengguna.zfill(3)} adalah angka...")
            fakta = dapatkan_fakta_angka(input_pengguna)
            print(fakta)
        else:
            print("❌ Input tidak valid. Harap masukkan hanya angka.")

if __name__ == "__main__":
    # Peringatan jika API key belum diatur
    if GOOGLE_API_KEY == "MASUKKAN_API_KEY_KAMU_DISINI":
        print("\n⚠️ PERINGATAN: API Key Gemini belum diatur.")
        print("Silakan ganti 'MASUKKAN_API_KEY_KAMU_DISINI' di dalam kode dengan API key kamu yang asli.")
        print("Program tidak akan berfungsi dengan benar tanpanya.\n")
    else:
        main()