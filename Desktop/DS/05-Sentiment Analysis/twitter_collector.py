import tweepy
import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import time # Impor library untuk 'tidur'

# Impor fungsi analisis sentimen
from sentiment_model import analyze_sentiment

# --- KONFIGURASI KUNCI API ---
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAPHb3QEAAAAA%2B9qvxeb9Db07FViCV1dBOr8ywQI%3DYdNervEw7vefBEcbTyf4bkZRzS5IuLQhadbunIirwkow7gzgAA"
CSV_FILE = "collected_tweets.csv"

# Inisialisasi koneksi
try:
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
except Exception as e:
    print(f"❌ Gagal inisialisasi Tweepy. Periksa Bearer Token Anda. Error: {e}")
    client = None

# --- FUNGSI PENYIMPANAN DATA (Tidak ada perubahan) ---
def save_to_csv(data_to_save):
    # ... (kode ini tetap sama persis) ...
    df = pd.DataFrame(data_to_save)
    try:
        if os.path.exists(CSV_FILE):
            df.to_csv(CSV_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            df.to_csv(CSV_FILE, mode='w', header=True, index=False, encoding='utf-8-sig')
        print(f"✅ {len(df)} cuitan baru berhasil disimpan ke {CSV_FILE}")
    except Exception as e:
        print(f"❌ Gagal menyimpan ke CSV: {e}")


# --- FUNGSI PENGUMPULAN DATA (DENGAN PENANGANAN ERROR 429) ---
def collect_and_analyze_tweets(keyword, max_results=10):
    if not client:
        return []
        
    try:
        print(f"📡 Menghubungi API Twitter untuk mencari cuitan dengan kata kunci '{keyword}'...")
        
        response = client.search_recent_tweets(
            query=f"{keyword} lang:id -is:retweet",
            max_results=max_results,
            tweet_fields=["created_at"] 
        )

        if not response.data:
            print("Tidak ada cuitan baru yang ditemukan.")
            return []

        print(f"📊 Ditemukan {len(response.data)} cuitan. Memulai analisis sentimen...")
        
        analyzed_tweets = []
        for tweet in tqdm(response.data, desc="Menganalisis Sentimen"):
            text = tweet.text
            sentiment = analyze_sentiment(text)
            
            analyzed_tweets.append({
                "timestamp": tweet.created_at,
                "keyword": keyword,
                "tweet_text": text,
                "sentiment_label": sentiment['label'],
                "sentiment_score": sentiment['score']
            })
        
        return analyzed_tweets
    
    # --- BLOK PENANGANAN ERROR BARU ---
    except tweepy.errors.TooManyRequests:
        print("❌ Terkena Rate Limit (Too Many Requests).")
        print("⏸️ Program akan tidur selama 15 menit sebelum melanjutkan...")
        time.sleep(15 * 60) # Tidur selama 15 menit (15 * 60 detik)
        print("▶️ Mencoba kembali...")
        return collect_and_analyze_tweets(keyword, max_results) # Coba lagi fungsinya
    # -----------------------------------

    except Exception as e:
        print(f"❌ Terjadi error saat mengambil data: {e}")
        return []

# --- BAGIAN EKSEKUSI UTAMA ---
if __name__ == "__main__":
    if client:
        KATA_KUNCI = "Idolm@ster"
        hasil_analisis = collect_and_analyze_tweets(KATA_KUNCI, max_results=50)
        if hasil_analisis:
            print("💾 Menyimpan hasil analisis ke file CSV...")
            save_to_csv(hasil_analisis)
            print("🎉 Proses Selesai.")