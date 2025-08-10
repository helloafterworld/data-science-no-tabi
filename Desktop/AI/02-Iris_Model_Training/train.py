# train.py
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import joblib

# Muat dataset Iris
iris = load_iris()
X, y = iris.data, iris.target
df = pd.DataFrame(X, columns=iris.feature_names)

# Latih model regresi logistik sederhana
model = LogisticRegression(max_iter=200)
model.fit(X, y)

print("✅ Model berhasil dilatih!")

# Simpan model ke dalam file
joblib.dump(model, 'model.pkl')
print("✅ Model berhasil disimpan sebagai model.pkl")

# Simpan juga nama kolom untuk referensi di API
joblib.dump(list(df.columns), 'model_columns.pkl')
print("✅ Kolom model berhasil disimpan sebagai model_columns.pkl")