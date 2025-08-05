import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# --- 1. MEMUAT DAN EKSPLORASI DATA ---
# Muat dataset dari file CSV yang sudah diunduh
df = pd.read_csv('heart.csv')

# Menampilkan 5 baris pertama untuk melihat struktur data
print("--- Tampilan Awal Data ---")
print(df.head())
print("\n")


# --- 2. PRA-PEMROSESAN DATA (PREPROCESSING) ---
# Mengubah fitur kategorikal (berbasis teks) menjadi numerik menggunakan one-hot encoding
# Ini penting karena model machine learning hanya bisa memproses angka.
df_processed = pd.get_dummies(df, columns=['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope'], drop_first=True)

# Menampilkan data setelah diubah
print("--- Data Setelah Diubah ke Format Numerik ---")
print(df_processed.head())
print("\n")


# --- 3. MEMBAGI DATA UNTUK TRAINING DAN TESTING ---
# Pisahkan fitur (X) dan variabel target (y)
X = df_processed.drop('HeartDisease', axis=1)  # Semua kolom kecuali HeartDisease
y = df_processed['HeartDisease']               # Hanya kolom HeartDisease

# Bagi data menjadi 80% untuk training dan 20% untuk testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Ukuran data training: {X_train.shape[0]} baris")
print(f"Ukuran data testing: {X_test.shape[0]} baris\n")


# --- 4. MELATIH MODEL MACHINE LEARNING ---
# Inisialisasi model Logistic Regression
# Ini adalah model klasifikasi yang baik untuk memulai
model = LogisticRegression(max_iter=1000) # max_iter ditambah untuk memastikan konvergensi

# Latih model menggunakan data training
model.fit(X_train, y_train)
print("--- Model berhasil dilatih! ---\n")


# --- 5. EVALUASI DAN PREDIKSI ---
# Evaluasi model menggunakan data testing
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Akurasi model pada data testing: {accuracy:.2f}")

# Contoh membuat prediksi untuk 1 data pasien baru
# Pastikan urutan dan jumlah kolomnya sama dengan X_train
# Nilai di bawah ini hanya contohtaFrame(pasien_baru)

# Lakukan prediksi
prediksi_pasien = model.predict(X_test.iloc[0:1])
prediksi_proba = model.predict_proba(X_test.iloc[0:1])

print("\n--- Prediksi untuk Pasien Baru ---")
print(f"Data Pasien: {X_test.iloc[0:1].to_dict(orient='records')[0]}")
print(f"Hasil Prediksi: {prediksi_pasien[0]}")
if prediksi_pasien[0] == 1:
    print("Hasil Prediksi: Berisiko Terkena Penyakit Jantung.")
else:
    print("Hasil Prediksi: Tidak Berisiko Terkena Penyakit Jantung.")

print(f"Probabilitas (0: Tidak Berisiko, 1: Berisiko): {prediksi_proba[0]}")