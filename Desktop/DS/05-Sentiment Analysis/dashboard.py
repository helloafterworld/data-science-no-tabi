import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Dashboard Analisis Sentimen",
    page_icon="📊",
    layout="wide"
)

# --- Fungsi untuk memuat data (dengan cache agar efisien) ---
@st.cache_data(ttl=60) # Cache data selama 60 detik
def load_data():
    try:
        df = pd.read_csv("collected_tweets.csv")
        # Pastikan kolom timestamp diubah menjadi tipe datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        return pd.DataFrame() # Kembalikan DataFrame kosong jika file tidak ditemukan

# --- Judul & Deskripsi Dashboard ---
st.title("📊 Dashboard Analisis Sentimen Twitter")
st.write("Dashboard ini memvisualisasikan sentimen dari cuitan yang dikumpulkan secara real-time.")

# Muat data
df = load_data()

if df.empty:
    st.warning("File 'collected_tweets.csv' tidak ditemukan atau kosong. Silakan jalankan 'twitter_collector.py' terlebih dahulu.")
else:
    # --- Tampilan Metrik Utama (KPI) ---
    st.divider()
    total_tweets = len(df)
    keyword = df['keyword'].iloc[-1] if 'keyword' in df.columns else 'Tidak Diketahui'

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cuitan Terkumpul", f"{total_tweets}")
    col2.metric("Kata Kunci yang Dipantau", f"'{keyword.upper()}'")
    col3.metric("Data Terakhir Diperbarui", f"{df['timestamp'].max().strftime('%H:%M:%S')}")
    st.divider()

    # --- Visualisasi Utama ---
    col_viz1, col_viz2 = st.columns(2)

    with col_viz1:
        # 1. Grafik Distribusi Sentimen (Pie Chart)
        st.subheader("Distribusi Sentimen Keseluruhan")
        sentiment_counts = df['sentiment_label'].value_counts()

        fig1, ax1 = plt.subplots()
        ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
        ax1.axis('equal')  # Memastikan pie chart berbentuk lingkaran
        st.pyplot(fig1)

    with col_viz2:
        # 2. Grafik Tren Sentimen dari Waktu ke Waktu (Line Chart)
        st.subheader("Tren Sentimen per Jam")
        # Resample data per jam dan hitung jumlah setiap sentimen
        df_resampled = df.set_index('timestamp').resample('h')['sentiment_label'].value_counts().unstack().fillna(0)
        st.line_chart(df_resampled)

    st.divider()

    # --- Analisis Teks dengan Word Cloud ---
    st.subheader("Kata Paling Sering Muncul (Word Cloud)")

    # Filter berdasarkan sentimen
    sentiment_filter = st.selectbox("Pilih Sentimen untuk Word Cloud:", ["Semua"] + list(df['sentiment_label'].unique()))

    if sentiment_filter != "Semua":
        filtered_df = df[df['sentiment_label'] == sentiment_filter]
    else:
        filtered_df = df

    if not filtered_df.empty:
        # Gabungkan semua teks dari kolom tweet_text
        text_corpus = ' '.join(filtered_df['tweet_text'])

        wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(text_corpus)

        fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
        ax_wc.imshow(wordcloud, interpolation='bilinear')
        ax_wc.axis('off')
        st.pyplot(fig_wc)
    else:
        st.warning("Tidak ada data untuk sentimen yang dipilih.")

    # --- Menampilkan Data Mentah ---
    with st.expander("Lihat Data Mentah yang Terkumpul"):
        st.dataframe(df)