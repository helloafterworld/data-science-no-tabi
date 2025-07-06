# Aplikasi Prediksi Dini Gagal Jantung

Sebuah aplikasi web interaktif yang dibangun menggunakan Streamlit untuk memprediksi risiko penyakit jantung berdasarkan data klinis pasien.

**[Link ke Aplikasi Streamlit Anda yang sudah di-deploy]** 

##  latar Belakang & Tujuan
Proyek ini bertujuan untuk membangun model machine learning yang andal dan dapat diinterpretasikan untuk membantu skrining awal penyakit jantung. Fokus utama tidak hanya pada akurasi, tetapi juga pada kemampuan untuk menjelaskan faktor-faktor yang mendorong prediksi.

## Alur Kerja Proyek
1.  **Pembersihan Data:** Menangani nilai 0 yang tidak logis pada kolom Kolesterol dan Tekanan Darah.
2.  **Analisis Data Eksploratif (EDA):** Mengidentifikasi pola dan hubungan antar variabel melalui visualisasi.
3.  **Pemodelan:** Membandingkan beberapa model dan melakukan optimisasi pada model terbaik (Random Forest) menggunakan GridSearchCV.
4.  **Interpretasi:** Menganalisis *feature importance* dan menggunakan SHAP (jika Anda jadi menggunakannya) untuk menjelaskan prediksi.
5.  **Deployment:** Membangun aplikasi web interaktif dengan Streamlit.

## Teknologi yang Digunakan
- Python
- Pandas & NumPy
- Scikit-learn
- Matplotlib & Seaborn
- Streamlit

## Cara Menjalankan
1. Clone repositori ini.
2. Buat environment virtual dan install dependensi dari `requirements.txt`.
3. Jalankan `streamlit run app.py` di terminal.