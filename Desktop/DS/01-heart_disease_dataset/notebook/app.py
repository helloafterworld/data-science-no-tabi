import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Analisis Risiko Jantung",
    page_icon="❤️",
    layout="wide"
)

# --- Memuat Aset ---
@st.cache_resource
def load_assets():
    # Pastikan semua file ini berada di folder yang sama dengan app.py
    with open('heart_failure_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('heart_failure_scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    # Ganti path ini jika file heart.csv Anda ada di tempat lain
    original_df = pd.read_csv('../data/heart.csv') 
    return model, scaler, original_df

model, scaler, original_df = load_assets()

# --- Antarmuka Pengguna (UI) ---
st.title("❤️ Analisis & Prediksi Risiko Gagal Jantung")
st.write("""
Aplikasi ini membantu melakukan skrining awal risiko penyakit jantung. Masukkan parameter medis Anda di sidebar untuk melihat prediksi dan perbandingan profil.
**Disclaimer:** Ini adalah alat bantu edukasi, bukan pengganti diagnosis medis profesional.
""")

st.sidebar.header("Parameter Input Pasien")
def user_input_features():
    Age = st.sidebar.slider("Umur (Tahun)", 28, 77, 54)
    Sex = st.sidebar.selectbox("Jenis Kelamin", ["M", "F"])
    ChestPainType = st.sidebar.selectbox("Tipe Nyeri Dada", ["ASY", "NAP", "ATA", "TA"])
    RestingBP = st.sidebar.slider("Tekanan Darah Istirahat (mm Hg)", 92, 200, 132)
    Cholesterol = st.sidebar.slider("Kolesterol (mm/dl)", 85, 603, 244)
    FastingBS = st.sidebar.selectbox("Gula Darah Puasa > 120 mg/dl", [0, 1])
    RestingECG = st.sidebar.selectbox("Hasil EKG Istirahat", ["Normal", "ST", "LVH"])
    MaxHR = st.sidebar.slider("Detak Jantung Maksimal", 60, 202, 137)
    ExerciseAngina = st.sidebar.selectbox("Angina Akibat Olahraga", ["N", "Y"])
    Oldpeak = st.sidebar.slider("Oldpeak (Depresi ST)", -2.6, 6.2, 0.9, 0.1)
    ST_Slope = st.sidebar.selectbox("Slope Segmen ST", ["Flat", "Up", "Down"])
    
    data = {'Age': Age, 'Sex': Sex, 'ChestPainType': ChestPainType, 'RestingBP': RestingBP,
            'Cholesterol': Cholesterol, 'FastingBS': FastingBS, 'RestingECG': RestingECG,
            'MaxHR': MaxHR, 'ExerciseAngina': ExerciseAngina, 'Oldpeak': Oldpeak, 'ST_Slope': ST_Slope}
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# --- Tombol Prediksi & Tampilan Hasil ---
if st.sidebar.button("Analisis Sekarang", type="primary"):
    
    # --- Preprocessing & Prediksi ---
    model_feature_names = scaler.get_feature_names_out()
    input_encoded = pd.get_dummies(input_df, drop_first=True)
    final_df = pd.DataFrame(columns=model_feature_names, index=[0]).fillna(0)
    for col in input_encoded.columns:
        if col in final_df.columns:
            final_df[col] = input_encoded[col].values
    input_scaled = scaler.transform(final_df)
    prediction = model.predict(input_scaled)
    prediction_proba = model.predict_proba(input_scaled)

    # --- Tampilan Hasil Prediksi ---
    st.divider()
    st.subheader("Hasil Prediksi Anda")
    if prediction[0] == 1:
        st.error("Berisiko Tinggi Mengalami Gagal Jantung", icon="💔")
    else:
        st.success("Berisiko Rendah Mengalami Gagal Jantung", icon="❤️")
    proba_df = pd.DataFrame(prediction_proba, columns=['Probabilitas Risiko Rendah', 'Probabilitas Risiko Tinggi'], index=['Hasil'])
    st.table(proba_df.style.format('{:.2%}'))
    st.divider()
    
    # --- BAGIAN INSIGHT YANG DISEMPURNAKAN ---
    st.subheader("Profil Pasien Berdasarkan Hasil Prediksi Anda")

    if prediction[0] == 1:
        st.warning("Anda memiliki beberapa karakteristik yang mirip dengan kelompok **'Risiko Tinggi'** dalam data kami. Berikut adalah perbandingan profil Anda:")
        profile_df = original_df[original_df['HeartDisease'] == 1]
        comparison_group_name = "Rata-rata Kelompok Berisiko Tinggi"
    else:
        st.success("Anda memiliki beberapa karakteristik yang mirip dengan kelompok **'Risiko Rendah'** dalam data kami. Berikut adalah perbandingan profil Anda:")
        profile_df = original_df[original_df['HeartDisease'] == 0]
        comparison_group_name = "Rata-rata Kelompok Berisiko Rendah"

    # Hitung statistik deskriptif dari kelompok tersebut
    avg_profile = profile_df[['Age', 'RestingBP', 'Cholesterol', 'MaxHR']].mean()

    # Tampilkan perbandingan metrik dalam 2 kolom
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"Umur Anda vs. {comparison_group_name}",
                  value=f"{input_df['Age'].iloc[0]} Tahun",
                  delta=f"{input_df['Age'].iloc[0] - avg_profile['Age']:.0f} Tahun")
        
        st.metric(label=f"Tekanan Darah Istirahat Anda vs. {comparison_group_name}",
                  value=f"{input_df['RestingBP'].iloc[0]}",
                  delta=f"{input_df['RestingBP'].iloc[0] - avg_profile['RestingBP']:.0f}")

    with col2:
        st.metric(label=f"Kolesterol Anda vs. {comparison_group_name}",
                  value=f"{input_df['Cholesterol'].iloc[0]}",
                  delta=f"{input_df['Cholesterol'].iloc[0] - avg_profile['Cholesterol']:.0f}",
                  delta_color="inverse") # "inverse" membuat nilai positif menjadi merah (berbahaya)
        
        st.metric(label=f"Detak Jantung Maks. Anda vs. {comparison_group_name}",
                  value=f"{input_df['MaxHR'].iloc[0]}",
                  delta=f"{input_df['MaxHR'].iloc[0] - avg_profile['MaxHR']:.0f}")

    # Tambahkan visualisasi perbandingan yang lebih kaya
    st.write("---")
    st.write("**Visualisasi Perbandingan Anda dengan Distribusi Kelompok**")
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    sns.set_style("whitegrid")

    # Plot untuk Kolesterol
    sns.kdeplot(profile_df['Cholesterol'], ax=axes[0], fill=True, label=f"Distribusi {comparison_group_name}", color='skyblue')
    axes[0].axvline(input_df['Cholesterol'].iloc[0], color='red', linestyle='--', label='Kolesterol Anda')
    axes[0].set_title("Perbandingan Kolesterol")
    axes[0].legend()

    # Plot untuk Detak Jantung Maksimal
    sns.kdeplot(profile_df['MaxHR'], ax=axes[1], fill=True, label=f"Distribusi {comparison_group_name}", color='lightgreen')
    axes[1].axvline(input_df['MaxHR'].iloc[0], color='red', linestyle='--', label='MaxHR Anda')
    axes[1].set_title("Perbandingan Detak Jantung Maksimal")
    axes[1].legend()

    st.pyplot(fig)

    # --- (KODE INI DITEMPELKAN DI BAGIAN AKHIR BLOK "IF") ---

    st.divider()
    st.subheader("Analisis Faktor Risiko Kategorikal")
    st.write("Grafik di bawah ini menunjukkan bagaimana kategori fitur tertentu lebih berisiko daripada yang lain berdasarkan data historis. Semakin tinggi bar, semakin besar proporsi pasien di kategori tersebut yang menderita penyakit jantung.")

    # Membuat 3 kolom agar rapi
    col1, col2, col3 = st.columns(3)

    # --- Plot 1: Tipe Nyeri Dada (ChestPainType) ---
    with col1:
        # Hitung proporsi risiko per kategori
        pain_risk = original_df.groupby('ChestPainType')['HeartDisease'].mean().reset_index().sort_values('HeartDisease', ascending=False)
        
        # Buat kanvas plot
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        
        # Buat bar plot
        sns.barplot(x='ChestPainType', y='HeartDisease', data=pain_risk, ax=ax1, palette='coolwarm')
        ax1.set_title('Risiko per Tipe Nyeri Dada')
        ax1.set_xlabel('Tipe Nyeri Dada')
        ax1.set_ylabel('Rata-rata Risiko Penyakit Jantung')
        ax1.set_ylim(0, 1) # Set sumbu y dari 0 hingga 1 (0% hingga 100%)
        
        # Tampilkan plot di Streamlit
        st.pyplot(fig1)
        st.info(f"Pilihan Anda: **{input_df['ChestPainType'].iloc[0]}**")


    # --- Plot 2: Slope Segmen ST (ST_Slope) ---
    with col2:
        slope_risk = original_df.groupby('ST_Slope')['HeartDisease'].mean().reset_index().sort_values('HeartDisease', ascending=False)
        fig2, ax2 = plt.subplots(figsize=(6, 5))
        sns.barplot(x='ST_Slope', y='HeartDisease', data=slope_risk, ax=ax2, palette='viridis')
        ax2.set_title('Risiko per Slope Segmen ST')
        ax2.set_xlabel('Slope Segmen ST')
        ax2.set_ylabel('') # Kosongkan agar tidak tumpang tindih
        ax2.set_ylim(0, 1)
        st.pyplot(fig2)
        st.info(f"Pilihan Anda: **{input_df['ST_Slope'].iloc[0]}**")

    # --- Plot 3: Angina Akibat Olahraga (ExerciseAngina) ---
    with col3:
        angina_risk = original_df.groupby('ExerciseAngina')['HeartDisease'].mean().reset_index().sort_values('HeartDisease', ascending=False)
        fig3, ax3 = plt.subplots(figsize=(6, 5))
        sns.barplot(x='ExerciseAngina', y='HeartDisease', data=angina_risk, ax=ax3, palette='plasma')
        ax3.set_title('Risiko per Angina Akibat Olahraga')
        ax3.set_xlabel('Mengalami Angina (Y/N)')
        ax3.set_ylabel('') # Kosongkan
        ax3.set_ylim(0, 1)
        st.pyplot(fig3)
        st.info(f"Pilihan Anda: **{input_df['ExerciseAngina'].iloc[0]}**")

else:
    st.info("Silakan isi parameter di sidebar kiri dan klik tombol 'Analisis Sekarang' untuk melihat hasilnya.")