import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap
import matplotlib.pyplot as plt

# --- Konfigurasi Halaman & Opsi ---
st.set_page_config(
    page_title="Analisis Risiko Jantung",
    page_icon="❤️",
    layout="wide"
)
# st.set_option('deprecation.showPyplotGlobalUse', False) # Menonaktifkan warning pyplot

# --- Memuat Aset (Model, Scaler, Explainer) ---
@st.cache_resource
def load_assets():
    with open('heart_failure_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('heart_failure_scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    with open('shap_explainer.pkl', 'rb') as explainer_file:
        explainer = pickle.load(explainer_file)
    # Muat data asli untuk perbandingan
    original_df = pd.read_csv('../data/heart.csv')
    return model, scaler, explainer, original_df

model, scaler, explainer, original_df = load_assets()

# --- Antarmuka Pengguna (UI) ---
st.title("❤️ Analisis Insight Risiko Gagal Jantung")
st.write("""
Aplikasi ini tidak hanya memprediksi, tetapi juga memberikan penjelasan mengapa suatu prediksi dibuat. Masukkan parameter medis di sidebar untuk memulai.
**Disclaimer:** Ini adalah alat bantu edukasi, bukan pengganti diagnosis medis profesional.
""")

# Input pengguna di Sidebar
st.sidebar.header("Parameter Input Pasien")
def user_input_features():
    Age = st.sidebar.slider("Umur (Tahun)", 28, 77, 54)
    Sex = st.sidebar.selectbox("Jenis Kelamin", ["M", "F"])
    ChestPainType = st.sidebar.selectbox("Tipe Nyeri Dada", ["ATA", "NAP", "ASY", "TA"])
    RestingBP = st.sidebar.slider("Tekanan Darah Istirahat", 0, 200, 132)
    Cholesterol = st.sidebar.slider("Kolesterol", 0, 603, 244)
    FastingBS = st.sidebar.selectbox("Gula Darah Puasa > 120 mg/dl", [0, 1])
    RestingECG = st.sidebar.selectbox("Hasil EKG Istirahat", ["Normal", "ST", "LVH"])
    MaxHR = st.sidebar.slider("Detak Jantung Maksimal", 60, 202, 137)
    ExerciseAngina = st.sidebar.selectbox("Angina Akibat Olahraga", ["N", "Y"])
    Oldpeak = st.sidebar.slider("Oldpeak (Depresi ST)", -3.0, 7.0, 0.9, 0.1)
    ST_Slope = st.sidebar.selectbox("Slope Segmen ST", ["Up", "Flat", "Down"])
    
    data = {'Age': Age, 'Sex': Sex, 'ChestPainType': ChestPainType, 'RestingBP': RestingBP,
            'Cholesterol': Cholesterol, 'FastingBS': FastingBS, 'RestingECG': RestingECG,
            'MaxHR': MaxHR, 'ExerciseAngina': ExerciseAngina, 'Oldpeak': Oldpeak, 'ST_Slope': ST_Slope}
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# --- Preprocessing & Prediksi (Sama seperti sebelumnya) ---
# Salin bagian encoding dan penyesuaian kolom dari app.py Anda sebelumnya ke sini
raw_input_df = input_df.copy() # Simpan input mentah untuk ditampilkan
model_feature_names = scaler.get_feature_names_out()

input_encoded = pd.get_dummies(input_df, drop_first=True)
final_df = pd.DataFrame(columns=model_feature_names)
final_df.loc[0] = 0
for col in input_encoded.columns:
    if col in final_df.columns:
        final_df[col] = input_encoded[col].values

input_scaled = scaler.transform(final_df)


# --- Tombol Prediksi & Tampilan Hasil ---
if st.sidebar.button("Analisis Sekarang", type="primary"):
    # --- BLOK BARU (GUNAKAN INI) ---
    # --- BLOK BARU & FINAL (GUNAKAN INI) ---

    # 5. Melakukan prediksi
    prediction = model.predict(input_scaled)
    prediction_proba = model.predict_proba(input_scaled)

    st.divider()
    st.subheader("Hasil Prediksi")

    # 6. Menampilkan hasil
    if prediction[0] == 1:
        st.error("Berisiko Tinggi Mengalami Gagal Jantung", icon="💔")
    else:
        st.success("Berisiko Rendah Mengalami Gagal Jantung", icon="❤️")

    st.write("Tingkat Keyakinan Model:")
    proba_df = pd.DataFrame(prediction_proba, columns=['Probabilitas Risiko Rendah', 'Probabilitas Risiko Tinggi'], index=['Hasil'])
    st.table(proba_df.style.format('{:.2%}'))

    st.divider()

    # --- INSIGHT LEVEL 1: Konteks Data (tetap sama) ---
    st.subheader("2. Konteks: Input Anda vs Populasi Data")
    # ... (kode untuk metrik perbandingan dengan populasi tidak perlu diubah) ...
    # ... (pastikan kode ini ada di app.py Anda dari jawaban sebelumnya) ...

    st.divider()

    # --- INSIGHT LEVEL 2 & 3: Penjelasan SHAP yang Diperbaiki ---
    st.subheader("3. Penjelasan Prediksi & Faktor Risiko Utama")
    st.write("""
    Grafik di bawah ini (SHAP Force Plot) menunjukkan faktor-faktor yang mendorong prediksi.
    - **Faktor pendorong ke arah 'Risiko Tinggi' (merah)** mendorong hasil ke kanan.
    - **Faktor pendorong ke arah 'Risiko Rendah' (biru)** mendorong hasil ke kiri.
    """)

    # --- Logika Cerdas untuk Menangani Output SHAP ---
    shap_values_list = explainer.shap_values(input_scaled)
    expected_value = explainer.expected_value

    # Cek apakah outputnya adalah list (untuk 2 kelas) atau array tunggal
    if isinstance(shap_values_list, list) and len(shap_values_list) == 2:
        shap_values_to_plot = shap_values_list[1] # Penjelasan untuk kelas 1 (positif)
        base_value = expected_value[1]
    else:
        shap_values_to_plot = shap_values_list
        base_value = expected_value

    # --- PERUBAHAN UTAMA DI SINI ---
    # Tampilkan SHAP force plot dengan memanggil shap.plots.force
    # Pastikan shap_values_to_plot adalah array 1D untuk satu prediksi
    p = shap.plots.force(
        base_value,
        shap_values_to_plot[0],
        features=final_df.iloc[0],
        matplotlib=True
    )
    st.pyplot(p, bbox_inches='tight', clear_figure=True)
    # --------------------------------

    st.divider()

    # Tampilkan Faktor Risiko Utama
    st.subheader("4. Faktor Risiko Paling Berpengaruh untuk Anda")
    # ... (kode untuk menampilkan faktor risiko utama tidak perlu diubah) ...
    # ... (pastikan kode ini ada di app.py Anda dari jawaban sebelumnya) ...