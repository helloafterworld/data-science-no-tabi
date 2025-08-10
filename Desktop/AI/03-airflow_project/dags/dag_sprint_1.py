# sprint_pertama_dag.py
from __future__ import annotations

import json
from datetime import datetime

import pandas as pd
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

# --- FUNGSI UNTUK SETIAP TUGAS ---

def extract_data():
    """
    Tugas 1: Mengambil data dari API publik.
    Ini adalah langkah 'Extract'.
    """
    import requests

    url = "https://jsonplaceholder.typicode.com/todos"
    response = requests.get(url)
    data = response.json()

    # Simpan data ke file sementara untuk diteruskan ke tugas selanjutnya
    with open('/opt/airflow/dags/temp_todos.json', 'w') as f:
        json.dump(data, f)
    print("Data berhasil diekstrak dan disimpan sementara.")

def transform_data():
    """
    Tugas 2: Membaca data mentah, mengubahnya, dan menyimpan kembali.
    Ini adalah langkah 'Transform'.
    """
    with open('/opt/airflow/dags/temp_todos.json', 'r') as f:
        data = json.load(f)

    # Buat DataFrame pandas dari data
    df = pd.DataFrame(data)

    # Transformasi sederhana: pilih beberapa kolom dan ubah status 'completed'
    df_transformed = df[['userId', 'id', 'title', 'completed']]
    df_transformed['status'] = df_transformed['completed'].apply(lambda x: 'Selesai' if x else 'Belum Selesai')
    df_transformed = df_transformed.drop(columns=['completed'])

    # Simpan hasil transformasi ke file CSV
    df_transformed.to_csv('/opt/airflow/dags/todos_bersih.csv', index=False)
    print("Data berhasil ditransformasi dan disimpan sebagai CSV.")

def load_data():
    """
    Tugas 3: Memuat data (dalam kasus ini, kita hanya menampilkan isinya).
    Ini adalah langkah 'Load'.
    """
    df = pd.read_csv('/opt/airflow/dags/todos_bersih.csv')
    print("Data berhasil dimuat! Berikut 5 baris pertama:")
    print(df.head())

# --- DEFINISI DAG ---

with DAG(
    dag_id="sprint_pertama_etl_todos",
    description="DAG sederhana untuk proses ETL data To-Do list",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",  # Akan berjalan setiap hari
    catchup=False,
    tags=["sprint", "etl", "pemula"],
) as dag:

    task_extract = PythonOperator(
        task_id="extract_data_from_api",
        python_callable=extract_data,
    )

    task_transform = PythonOperator(
        task_id="transform_raw_data",
        python_callable=transform_data,
    )

    task_load = PythonOperator(
        task_id="load_and_show_clean_data",
        python_callable=load_data,
    )

    # Atur urutan tugas: extract -> transform -> load
    task_extract >> task_transform >> task_load