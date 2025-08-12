import instaloader
import pandas as pd
import torch
from transformers import pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import getpass
import time

# ==============================================================================
# LANGKAH 1: INISIALISASI DAN LOGIN KE INSTALOADER
# ==============================================================================

print("Menginisialisasi Instaloader...")
L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=True, # Kita hanya butuh komentar
    save_metadata=False,
    compress_json=False
)

try:
    # Minta username dan password dengan aman
    USER = input("Masukkan username Instagram Anda: ")
    PASSWORD = getpass.getpass("Masukkan password Instagram Anda: ")
    L.login(USER, PASSWORD)
    print(f"Login sebagai {USER} berhasil!")
except Exception as e:
    print(f"Gagal login: {e}")
    print("Mencoba melanjutkan tanpa login (kemungkinan akan sangat terbatas).")

# ==============================================================================
# LANGKAH 2: AMBIL KOMENTAR DARI POST INSTAGRAM
# ==============================================================================

# Ganti dengan "shortcode" dari URL post Instagram yang Anda inginkan
# Contoh URL: https://www.instagram.com/p/C-pNw2Jy41h/ -> shortcode adalah 'C-pNw2Jy41h'
POST_SHORTCODE = 'DM-Hyr9yNxk' # <-- GANTI INI
print(f"Mengambil komentar dari post: {POST_SHORTCODE}...")

try:
    post = instaloader.Post.from_shortcode(L.context, POST_SHORTCODE)
    
    comments = []
    count = 0
    # Batasi jumlah komentar untuk menghindari blokir
    MAX_COMMENTS = 100 

    for comment in post.get_comments():
        if count >= MAX_COMMENTS:
            break
        comments.append(comment.text)
        count += 1
        # Beri jeda sedikit setiap 20 komentar
        if count % 20 == 0:
            print(f"  ...berhasil mengambil {count} komentar...")
            time.sleep(2)

    print(f"Total komentar yang berhasil diambil: {len(comments)}")
    # Ubah list komentar menjadi DataFrame pandas
    df = pd.DataFrame(comments, columns=['comment'])
    print("DataFrame berhasil dibuat.")

except Exception as e:
    print(f"Gagal mengambil komentar: {e}")
    df = pd.DataFrame() # Buat dataframe kosong jika gagal

# ==============================================================================
# LANGKAH 3: MUAT MODEL ANALISIS SENTIMEN
# ==============================================================================

if not df.empty:
    print("Memuat model analisis sentimen untuk Bahasa Indonesia...")
    # Menggunakan model dari indobenchmark yang di-fine-tune untuk sentimen
    pretrained_name = "w11wo/indonesian-sentiment-analysis-roberta"
    
    sentiment_analysis = pipeline(
        "sentiment-analysis",
        model=pretrained_name,
        tokenizer=pretrained_name
    )
    print("Model berhasil dimuat.")

    # ==============================================================================
    # LANGKAH 4: LAKUKAN ANALISIS & SIMPAN HASIL
    # ==============================================================================
    
    print("Menganalisis sentimen untuk setiap komentar...")
    results = []
    for index, row in df.iterrows():
        try:
            # Analisis sentimen hanya pada 512 karakter pertama untuk efisiensi
            text_to_analyze = row['comment'][:512]
            result = sentiment_analysis(text_to_analyze)
            results.append(result[0])
        except Exception:
            # Jika ada error pada satu komentar, lewati saja
            results.append({'label': 'error', 'score': 0.0})

    # Buat DataFrame dari hasil analisis
    df_results = pd.DataFrame(results)
    
    # Gabungkan DataFrame asli dengan hasil analisis
    df = pd.concat([df, df_results], axis=1)
    
    print("Analisis sentimen selesai.")
    print("\nContoh hasil analisis:")
    print(df.head())
    
    # Simpan hasil ke file CSV
    output_filename = f"sentiment_analysis_{POST_SHORTCODE}.csv"
    df.to_csv(output_filename, index=False)
    print(f"\nHasil lengkap telah disimpan ke file: {output_filename}")


    # ==============================================================================
    # LANGKAH 5: VISUALISASI HASIL
    # ==============================================================================
    
    print("Membuat visualisasi hasil...")
    # Hitung jumlah setiap sentimen
    sentiment_counts = df['label'].value_counts()

    plt.figure(figsize=(8, 6))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette="viridis")
    plt.title(f'Distribusi Sentimen untuk Post "{POST_SHORTCODE}"')
    plt.xlabel('Sentimen')
    plt.ylabel('Jumlah Komentar')
    plt.show()

else:
    print("\nTidak ada data untuk dianalisis.")