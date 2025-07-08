print("Masukkan dataset 1 (tekan ENTER kosong untuk selesai):")

# Input baris demi baris (dataset 1)
dataset1 = []
while True:
    line = input()
    if line.strip() == "":
        break
    dataset1.append(line.strip())

print(f"Dataset 1 diterima berisi {len(dataset1)} baris")

# Cek duplikat
unique_dataset = list(dict.fromkeys(dataset1))  # Hilangkan duplikat sambil jaga urutan
duplicate_count = len(dataset1) - len(unique_dataset)

if duplicate_count > 0:
    print(f"Ditemukan {duplicate_count} baris duplikat, hapus duplikat? (y/n)")
    jawab = input().strip().lower()
    if jawab == "y":
        dataset1 = unique_dataset

print("Membuat string...")

# Minta nama list
nama_list = input("Masukkan nama list: ").strip()

# Bentuk string
items_str = ", ".join(f'"{item}"' for item in dataset1)
final_str = f"{nama_list} = {{ {items_str} }}"

# Cetak hasil
print(final_str)
print(f"List berhasil dibuat dengan jumlah {len(dataset1)}!")
