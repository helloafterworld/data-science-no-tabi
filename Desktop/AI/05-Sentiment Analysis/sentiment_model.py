# 1. Impor komponen yang diperlukan dari library transformers
from transformers import pipeline

# 2. Inisialisasi pipeline untuk analisis sentimen
#    Kita akan menggunakan model yang sudah dilatih khusus untuk sentimen Bahasa Indonesia.
#    Model ini akan diunduh secara otomatis saat pertama kali dijalankan.
print("Memuat model analisis sentimen...")
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="mdhugol/indonesia-bert-sentiment-classification"
)
print("Model berhasil dimuat!")

# 3. Buat fungsi untuk menganalisis kalimat
def analyze_sentiment(text):
    """
    Fungsi ini mengambil satu kalimat teks dan mengembalikan
    label sentimen (positive, negative, neutral) dan skornya.
    """
    if not isinstance(text, str) or not text.strip():
        return {"label": "Invalid", "score": 0.0}

    result = sentiment_analyzer(text)
    return result[0] # Hasilnya berupa list, kita ambil elemen pertamanya

# --- Bagian Pengujian ---
if __name__ == "__main__":
    print("\n--- Memulai Pengujian Model ---")

    kalimat1 = "Pelayanan di restoran ini sangat luar biasa, makanannya enak!"
    kalimat2 = "Saya kecewa sekali, paket saya datang terlambat dan barangnya rusak."
    kalimat3 = "Filmnya biasa saja, tidak bagus tapi juga tidak jelek."
    kalimat4 = "Hari ini cuaca cerah."

    hasil1 = analyze_sentiment(kalimat1)
    hasil2 = analyze_sentiment(kalimat2)
    hasil3 = analyze_sentiment(kalimat3)
    hasil4 = analyze_sentiment(kalimat4)

    print(f"\nKalimat: '{kalimat1}'")
    print(f"Hasil Analisis: Label = {hasil1['label']}, Skor = {hasil1['score']:.4f}")

    print(f"\nKalimat: '{kalimat2}'")
    print(f"Hasil Analisis: Label = {hasil2['label']}, Skor = {hasil2['score']:.4f}")

    print(f"\nKalimat: '{kalimat3}'")
    print(f"Hasil Analisis: Label = {hasil3['label']}, Skor = {hasil3['score']:.4f}")

    print(f"\nKalimat: '{kalimat4}'")
    print(f"Hasil Analisis: Label = {hasil4['label']}, Skor = {hasil4['score']:.4f}")