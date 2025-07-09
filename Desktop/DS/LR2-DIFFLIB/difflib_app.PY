import difflib
import re # Diperlukan untuk parsing header

def dapatkan_input_multibaris(prompt):
    """
    Fungsi untuk mengambil input multibaris dari pengguna di terminal.
    """
    print(f"\n{prompt} (Ketik 'END' di baris baru dan tekan Enter untuk selesai):")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return lines

def jelaskan_perbedaan_dengan_nomor_baris(diff_generator):
    """
    Menganalisis hasil diff dan membuat penjelasan detail dengan nomor baris.
    """
    penjelasan = []
    diff_list = list(diff_generator)

    if not diff_list:
        return "Tidak ditemukan perbedaan. Kedua kode identik."

    penjelasan.append("Berikut adalah rincian perbedaannya:")
    
    # Inisialisasi nomor baris
    line_num_kode1 = 0
    line_num_kode2 = 0

    for line in diff_list:
        # Lewati header file standar
        if line.startswith('---') or line.startswith('+++'):
            continue
        
        # Parsing header hunk untuk mendapatkan nomor baris awal
        if line.startswith('@@'):
            match = re.search(r'@@ -(\d+),?\d* \+(\d+),?\d* @@', line)
            if match:
                # Set nomor baris awal untuk blok perubahan ini
                line_num_kode1 = int(match.group(1))
                line_num_kode2 = int(match.group(2))
                penjelasan.append(f"\n... Perubahan di sekitar baris {line_num_kode1} (Kode 1) ...")
            continue

        # Proses baris perubahan
        if line.startswith('-'):
            penjelasan.append(f"  [Baris {line_num_kode1} DIHAPUS dari Kode 1]: {line[1:]}")
            line_num_kode1 += 1
        elif line.startswith('+'):
            penjelasan.append(f"  [Baris {line_num_kode2} DITAMBAHKAN di Kode 2]: {line[1:]}")
            line_num_kode2 += 1
        elif line.startswith(' '): # Baris yang sama, untuk sinkronisasi hitungan
            line_num_kode1 += 1
            line_num_kode2 += 1
            
    return "\n".join(penjelasan)

def jalankan_pembanding():
    """
    Fungsi utama untuk menjalankan aplikasi pembanding kode.
    """
    print("Selamat datang di aplikasi pembanding kode")
    
    kode1_lines = dapatkan_input_multibaris("Masukkan kode 1")
    kode2_lines = dapatkan_input_multibaris("Masukkan kode 2")

    print("\nDeteksi perbedaan ...")
    print("="*40)

    # Buat perbandingan menggunakan difflib
    diff = difflib.unified_diff(
        kode1_lines,
        kode2_lines,
        fromfile='Kode 1',
        tofile='Kode 2',
        lineterm='',
    )

    # Jelaskan perbedaan secara detail dengan nomor baris
    penjelasan_detail = jelaskan_perbedaan_dengan_nomor_baris(diff)
    print(penjelasan_detail)
    print("="*40)

# Jalankan program utama
if __name__ == "__main__":
    jalankan_pembanding()