# Impor semua library yang dibutuhkan
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ==============================================================================
# 1. PERSIAPAN DATA
# ==============================================================================
# Membuat data contoh dalam bentuk DataFrame pandas.
# Dalam skenario nyata, Anda akan memuat data dari file (misal: pd.read_csv('data.csv'))
data = {
    'usia': [25, 34, 28, 45, 52, 22, 39, 31, 29, 48],
    'gender': ['Wanita', 'Pria', 'Pria', 'Wanita', 'Pria', 'Wanita', 'Pria', 'Wanita', 'Pria', 'Wanita'],
    'lama_browsing_menit': [15, 5, 8, 25, 20, 12, 18, 7, 6, 22],
    'jumlah_klik': [10, 3, 5, 12, 11, 8, 9, 4, 3, 13],
    'beli_produk': [1, 0, 0, 1, 1, 1, 1, 0, 0, 1]  # Target: 1 = Beli, 0 = Tidak Beli
}
df = pd.DataFrame(data)

print("--- 1. Data Awal ---")
print(df)
print("\n" + "="*60 + "\n")

# ==============================================================================
# 2. PRA-PEMROSESAN DATA
# ==============================================================================
# Model machine learning memerlukan input numerik.
# Kita ubah kolom 'gender' yang berisi teks menjadi angka.
df_processed = pd.get_dummies(df, columns=['gender'], drop_first=True)

print("--- 2. Data Setelah Di-preprocess (Gender diubah jadi angka) ---")
print(df_processed)
print("\n" + "="*60 + "\n")


# ==============================================================================
# 3. PEMISAHAN FITUR (INPUT) DAN TARGET (OUTPUT)
# ==============================================================================
# X adalah semua data yang kita gunakan untuk memprediksi (fitur).
X = df_processed.drop('beli_produk', axis=1)
# y adalah apa yang ingin kita prediksi (target).
y = df_processed['beli_produk']


# ==============================================================================
# 4. PEMBAGIAN DATA LATIH DAN DATA UJI
# ==============================================================================
# Model akan "belajar" dari data latih (80% dari data).
# Performanya akan diuji pada data uji (20% dari data) yang belum pernah dilihatnya.
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,    # 20% untuk data uji
    random_state=42   # Memastikan hasil pembagian data selalu sama setiap kali dijalankan
)


# ==============================================================================
# 5. PEMBUATAN DAN PELATIHAN MODEL XGBOOST
# ==============================================================================
# Inisialisasi model XGBoost untuk klasifikasi (XGBClassifier).
# use_label_encoder=False dan eval_metric='logloss' untuk menghindari pesan warning.
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')

print("--- 5. Melatih Model XGBoost... ---")
# Melatih model menggunakan data latih.
model.fit(X_train, y_train)
print("Model selesai dilatih!")
print("\n" + "="*60 + "\n")


# ==============================================================================
# 6. EVALUASI MODEL
# ==============================================================================
# Gunakan model yang sudah dilatih untuk membuat prediksi pada data uji.
y_pred = model.predict(X_test)

# Bandingkan prediksi model dengan jawaban sebenarnya untuk menghitung akurasi.
accuracy = accuracy_score(y_test, y_pred)
print("--- 6. Hasil Evaluasi Model ---")
print(f"Data Uji (Jawaban Sebenarnya): {y_test.values}")
print(f"Hasil Prediksi Model           : {y_pred}")
print(f"✅ Akurasi Model pada Data Uji  : {accuracy * 100:.2f}%")
print("\n" + "="*60 + "\n")


# ==============================================================================
# 7. CONTOH PREDIKSI PADA DATA BARU
# ==============================================================================
# Sekarang, mari kita gunakan model untuk memprediksi kasus baru.
# Misal ada pelanggan baru: Usia 36, Pria, browsing selama 19 menit, melakukan 10 klik.

pelanggan_baru = pd.DataFrame({
    'usia': [36],
    'lama_browsing_menit': [19],
    'jumlah_klik': [10],
    'gender_Pria': [1] # 1 karena Pria, 0 jika Wanita
})

# Pastikan urutan kolom sesuai dengan data saat pelatihan
pelanggan_baru = pelanggan_baru[X_train.columns]

# Lakukan prediksi
prediksi_baru = model.predict(pelanggan_baru)
proba_prediksi_baru = model.predict_proba(pelanggan_baru)

print("--- 7. Prediksi untuk Pelanggan Baru ---")
print(f"Data Pelanggan Baru:\n{pelanggan_baru.to_string(index=False)}")
print("-" * 20)
hasil_teks = 'Akan Membeli' if prediksi_baru[0] == 1 else 'Tidak Akan Membeli'
print(f"Hasil Prediksi: {hasil_teks} (Label: {prediksi_baru[0]})")
print(f"Probabilitas [P(Tidak Beli), P(Beli)]: {proba_prediksi_baru[0]}")