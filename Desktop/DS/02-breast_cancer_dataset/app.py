import streamlit as st
import pandas as pd
import numpy as np
import pickle

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Prediksi Kanker Payudara",
    page_icon="🔬",
    layout="wide"
)

# --- Memuat Model & Scaler ---
@st.cache_resource
def load_model_scaler():
    with open('bc_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('bc_scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    return model, scaler

model, scaler = load_model_scaler()

# --- Daftar Fitur Terpenting (Berdasarkan analisis Anda sebelumnya) ---
# Urutan ini PENTING dan harus sama dengan data saat training
important_features = [
    'perimeter_worst', 'concave points_worst', 'area_worst', 'radius_worst', 
    'concave points_mean', 'radius_mean', 'area_mean', 'perimeter_mean', 
    'concavity_worst', 'concavity_mean'
]

# --- Antarmuka Pengguna (UI) ---
st.title("🔬 Aplikasi Prediksi Dini Kanker Payudara")
st.write("""
Aplikasi ini menggunakan Machine Learning untuk memprediksi apakah sebuah tumor bersifat ganas (Malignant) atau jinak (Benign) berdasarkan fitur-fitur pengukuran inti sel yang paling berpengaruh.
**Disclaimer:** Ini adalah alat bantu edukasi dan tidak bisa menggantikan diagnosis medis profesional.
""")
st.sidebar.header("Parameter Input (10 Fitur Teratas)")

def user_input_features():
    # Membuat slider dan input box untuk 10 fitur terpenting
    inputs = {}
    inputs['perimeter_worst'] = st.sidebar.slider("Perimeter Terburuk", 50.0, 260.0, 107.0, 0.1)
    inputs['concave points_worst'] = st.sidebar.slider("Poin Cekung Terburuk", 0.0, 0.3, 0.11, 0.01)
    inputs['area_worst'] = st.sidebar.slider("Area Terburuk", 180.0, 4300.0, 880.0, 1.0)
    inputs['radius_worst'] = st.sidebar.slider("Radius Terburuk", 5.0, 40.0, 16.0, 0.1)
    inputs['concave points_mean'] = st.sidebar.slider("Poin Cekung Rata-rata", 0.0, 0.25, 0.05, 0.01)
    inputs['radius_mean'] = st.sidebar.slider("Radius Rata-rata", 5.0, 30.0, 14.0, 0.1)
    inputs['area_mean'] = st.sidebar.slider("Area Rata-rata", 140.0, 2500.0, 650.0, 1.0)
    inputs['perimeter_mean'] = st.sidebar.slider("Perimeter Rata-rata", 40.0, 200.0, 92.0, 0.1)
    inputs['concavity_worst'] = st.sidebar.slider("Cekungan Terburuk", 0.0, 1.5, 0.27, 0.01)
    inputs['concavity_mean'] = st.sidebar.slider("Cekungan Rata-rata", 0.0, 0.5, 0.09, 0.01)

    features = pd.DataFrame(inputs, index=[0])
    return features

input_df = user_input_features()

# --- Menyiapkan DataFrame Penuh dengan 30 Fitur ---
# Kita perlu membuat DataFrame dengan semua 30 fitur seperti saat training
# Fitur yang tidak diinput oleh pengguna akan kita isi dengan nilai median dari data asli
# (Ini adalah pendekatan imputasi sederhana yang baik)

# Nilai median ini dihitung dari notebook Anda
# Untuk kesederhanaan, kita hardcode di sini
all_features_median = {
    'radius_mean': 13.37, 'texture_mean': 18.84, 'perimeter_mean': 86.24, 'area_mean': 551.1,
    'smoothness_mean': 0.09587, 'compactness_mean': 0.09263, 'concavity_mean': 0.06154,
    'concave points_mean': 0.0335, 'symmetry_mean': 0.1792, 'fractal_dimension_mean': 0.06154,
    'radius_se': 0.2464, 'texture_se': 1.108, 'perimeter_se': 1.884, 'area_se': 24.53,
    'smoothness_se': 0.00638, 'compactness_se': 0.02045, 'concavity_se': 0.02589,
    'concave points_se': 0.01179, 'symmetry_se': 0.01873, 'fractal_dimension_se': 0.003187,
    'radius_worst': 14.97, 'texture_worst': 25.41, 'perimeter_worst': 97.66, 'area_worst': 686.5,
    'smoothness_worst': 0.1313, 'compactness_worst': 0.2119, 'concavity_worst': 0.2267,
    'concave points_worst': 0.09993, 'symmetry_worst': 0.2822, 'fractal_dimension_worst': 0.08004
}
full_df = pd.DataFrame(all_features_median, index=[0])

# Update DataFrame dengan input dari pengguna
for col in important_features:
    full_df[col] = input_df[col].values

# --- Tombol Prediksi & Tampilan Hasil ---
if st.sidebar.button("Lakukan Prediksi", type="primary"):
    
    # Lakukan penskalaan pada data final
    input_scaled = scaler.transform(full_df)
    
    # Prediksi
    prediction = model.predict(input_scaled)
    prediction_proba = model.predict_proba(input_scaled)
    
    st.divider()
    st.subheader("Hasil Prediksi Model")

    if prediction[0] == 1:
        st.error("Terdiagnosis Ganas (Malignant)", icon="🔬")
    else:
        st.success("Terdiagnosis Jinak (Benign)", icon=("✅"))
                   
    st.write("Tingkat Keyakinan Model:")
    proba_df = pd.DataFrame(prediction_proba, columns=['Probabilitas Jinak', 'Probabilitas Ganas'], index=['Hasil'])
    st.table(proba_df.style.format('{:.2%}'))

    st.divider()
    with st.expander("Lihat detail fitur yang Anda masukkan"):
        st.dataframe(input_df.T.rename(columns={0: 'Nilai Input'}))

else:
    st.info("Silakan isi parameter di sidebar kiri dan klik tombol 'Prediksi' untuk melihat hasilnya.")