import tweepy
import os
# Impor fungsi analisis sentimen yang sudah Anda buat
from sentiment_model import analyze_sentiment

# --- KONFIGURASI KUNCI API ---
# Cara aman: simpan kunci di environment variables.
# Untuk sekarang, Anda bisa langsung menempelkannya di sini.
# JANGAN PERNAH UNGGAH FILE INI KE GITHUB JIKA KUNCI ADA DI SINI.
BEARER_TOKEN = "CONFIDENTIAL_BEARER_TOKEN"

# Inisialisasi koneksi ke API Twitter v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# --- FUNGSI PENGUMPULAN DATA ---
def collect_and_analyze_tweets(keyword, max_results=10):
    """
    Mengumpulkan cuitan berdasarkan kata kunci dan menganalisis sentimennya.
    """
    try:
        # Cari cuitan terbaru yang mengandung kata kunci, dalam Bahasa Indonesia
        response = client.search_recent_tweets(
            query=f"{keyword} lang:id -is:retweet",
            max_results=max_results
        )

        # Jika tidak ada data, kembalikan list kosong
        if not response.data:
            print("Tidak ada cuitan yang ditemukan.")
            return []

        analyzed_tweets = []
        for tweet in response.data:
            text = tweet.text
            sentiment = analyze_sentiment(text)

            analyzed_tweets.append({
                "text": text,
                "sentiment_label": sentiment['label'],
                "sentiment_score": sentiment['score']
            })

        return analyzed_tweets

    except Exception as e:
        print(f"Terjadi error: {e}")
        return []

# --- BAGIAN EKSEKUSI UTAMA ---
if __name__ == "__main__":
    # Tentukan kata kunci yang ingin dicari
    KATA_KUNCI = "" # Ganti dengan topik yang Anda minati

    print(f"Mengumpulkan dan menganalisis cuitan terbaru dengan kata kunci: '{KATA_KUNCI}'...")

    hasil_analisis = collect_and_analyze_tweets(KATA_KUNCI, max_results=20)

    if hasil_analisis:
        print("\n--- Hasil Analisis Sentimen ---")
        for i, tweet_data in enumerate(hasil_analisis):
            print(f"\n{i+1}. Cuitan: {tweet_data['text']}")
            print(f"   Sentimen: {tweet_data['sentiment_label']} (Skor: {tweet_data['sentiment_score']:.2f})")