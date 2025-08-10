# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Inisialisasi aplikasi FastAPI
app = FastAPI(title="API Prediksi Iris")

# Muat model dan kolom yang sudah disimpan
model = joblib.load('model.pkl')
model_columns = joblib.load('model_columns.pkl')

# Definisikan struktur data untuk input request
# Pydantic akan otomatis memvalidasi tipe data
class IrisData(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Buat endpoint untuk prediksi
@app.post("/predict")
def predict(data: IrisData):
    """
    Menerima data bunga iris dan mengembalikan prediksi spesiesnya.
    """
    # Ubah data input menjadi array numpy sesuai urutan kolom saat training
    input_data = np.array([[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]])
    
    # Lakukan prediksi
    prediction_code = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0].tolist()

    # Ubah kode prediksi menjadi nama spesies
    species_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    species_name = species_map[prediction_code]
    
    return {
        "prediction": species_name,
        "prediction_code": int(prediction_code),
        "confidence_probability": prediction_proba
    }

# Endpoint sederhana untuk memastikan API berjalan
@app.get("/")
def read_root():
    return {"message": "Selamat datang di API Prediksi Iris!"}