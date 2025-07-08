# Kombinasi 2 dataset menjadi satu dictionary string

# Input Dataset 1
print("Masukkan dataset 1 (ketik 'SELESAI!' untuk berhenti):")
dataset1 = []
while True:
    line = input()
    if line.strip().upper() == "SELESAI!":
        break
    dataset1.append(line)

print(f"Dataset 1 diterima berisi {len(dataset1)} baris")

# Input Dataset 2
print("Masukkan dataset 2 (ketik 'SELESAI!' untuk berhenti):")
dataset2 = []
while True:
    line = input()
    if line.strip().upper() == "SELESAI!":
        break
    dataset2.append(line)

print(f"Dataset 2 diterima berisi {len(dataset2)} baris")

# Pastikan jumlah baris sama
if len(dataset1) != len(dataset2):
    print("Error: Jumlah baris pada kedua dataset tidak sama!")
    exit()

# Membentuk pasangan
combined = list(zip(dataset1, dataset2))

# Mencari duplikat
unique_combined = list(dict.fromkeys(combined))  # Hilangkan duplikat
duplicate_count = len(combined) - len(unique_combined)

if duplicate_count > 0:
    print(f"Ditemukan {duplicate_count} baris duplikat, hapus duplikat? (y/n)")
    jawab = input().strip().lower()
    if jawab != 'y':
        unique_combined = combined  # tetap pakai data duplikat

# Membuat dictionary
result_dict = {}
for d1, d2 in unique_combined:
    result_dict[d1] = d2

# Membentuk string dictionary
dict_items = [f'"{k}" : "{v}"' for k, v in result_dict.items()]
dict_str = "{ " + ", ".join(dict_items) + " }"

# Minta nama list
print("Masukkan nama list:")
nama_list = input().strip()

# Cetak hasil
print(f"{nama_list} = {dict_str}")
print(f"List berhasil dibuat dengan jumlah {len(result_dict)}!")
