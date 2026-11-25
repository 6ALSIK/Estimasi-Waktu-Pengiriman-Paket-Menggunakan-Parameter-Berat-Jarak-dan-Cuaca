import csv

nama_file = "package_delivery_data.csv"

kolom = [
    "distance_km", "package_weight_kg", "traffic_level", "weather", "vehicle_type", "warehouse_delay_hours"
, "handling_time_hours", "priority", "delivery_time_hours"
]

def baca_data():
    with open(nama_file, "r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def simpan_data(data):
    with open(nama_file, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=kolom)
        w.writeheader()
        w.writerows(data)

def tabel(data):
    garis = "-" * 120
    print(garis)
    print(f"{'No':<3} | {'Jarak':<10} | {'Berat':<10} | {'Traffic':<10} | {'Cuaca':<8} | {'Kendaraan':<10} | {'Delay':<9} | {'Handling':<10} | {'Prioritas':<10} | {'estimasi Waktu':<10}" )
    print(garis)

    no = 1
    
    for row in data:
            print(f"{no:<3} | {row['distance_km']:<10} | {row['package_weight_kg']:<10} | {row['traffic_level']:<10} | {row['weather']:<8} | {row['vehicle_type']:<10} | {row['warehouse_delay_hours']:<9} | {row['handling_time_hours']:<10} | {row['priority']:<10} | {row['delivery_time_hours']:<10}")
    
            no += 1
            print("-" * 120)

def estimasi(data):
    jarak = float(input("Masukkan jarak: "))
    berat = float(input("Masukkan berat: "))
    cuaca = input("Masukkan cuaca (Clear/Rain/Storm): ").strip().title()

    cocok = [d for d in data if d["weather"] == cuaca and abs(float(d["distance_km"]) - jarak) <= 10]

    if not cocok:
        print("Data dengan jarak dan cuaca yang sesuai tidak ditemukan.")
        return

    rata_waktu = sum(float(d["delivery_time_hours"]) for d in cocok) / len(cocok)
    rata_berat = sum(float(d["package_weight_kg"]) for d in cocok) / len(cocok)
    prediksi = rata_waktu + (berat - rata_berat) * 0.03

    print("Estimasi waktu:", round(prediksi, 2), "jam")

def tampilkan(data):
    i = 0
    while i < len(data):
        tabel(data[i:i + 20])
        i += 20
        if i < len(data):
            break        

def tambah(data):
    baru = {}
    for k in kolom:
        baru[k] = input("Masukkan " + k + ": ").strip()

    data.append(baru)
    simpan_data(data)
    print("Data berhasil ditambahkan.")

def ubah(data):
    no = int(input("Masukkan nomor data: "))

    if no >= 1 and no <= len(data):
        tabel([data[no - 1]])

        print("Kolom yang tersedia:")

        for nama in kolom:
            print(nama)

        nama = input("Kolom yang ingin diubah: ")

        if nama in kolom:
            nilai = input("Masukkan nilai baru: ")

            data[no - 1][nama] = nilai
            simpan_data(data)

            print("Data berhasil diubah.")
            tabel([data[no - 1]])
        else:
            print("Kolom tidak ditemukan.")
    else:
        print("Nomor data tidak ditemukan.")

def hapus(data):
    no = int(input("Masukkan nomor data: "))

    if no >= 1 and no <= len(data):
        tabel([data[no - 1]])

        pilih = input("Yakin hapus data? (y/n): ")

        if pilih == "y":
            data.pop(no - 1)
            simpan_data(data)
            print("Data berhasil dihapus.")
        else:
            print("Penghapusan dibatalkan.")
    else:
        print("Nomor data tidak ditemukan.")

def cari(data):
    print("1. Berdasarkan jarak")
    print("2. Berdasarkan berat")
    pilih = input("Pilih 1/2: ").strip()

    if pilih == "1":
        k = "distance_km"
    elif pilih == "2":
        k = "package_weight_kg"
    else:
        print("Pilihan tidak tersedia.")
        return

    batas_min = float(input("Nilai minimum: "))
    batas_max = float(input("Nilai maksimum: "))

    hasil = [d for d in data if batas_min <= float(d[k]) <= batas_max]

    if hasil:
        tabel(hasil)
        print("Jumlah data:", len(hasil))
    else:
        print("Data tidak ditemukan.")    

def statistik(data):
    print("Jumlah data:", len(data))
    if not data:
        return

    for k in ["distance_km", "package_weight_kg", "delivery_time_hours"]:
        nilai = [float(d[k]) for d in data]
        print("\n" + k)
        print("Rata-rata:", round(sum(nilai) / len(nilai), 2))
        print("Minimum:", min(nilai))
        print("Maksimum:", max(nilai))

def filter_cuaca(data):
    cuaca = input("Masukkan cuaca (Clear/Rain/Storm): ").strip().upper()
    hasil = [d for d in data if d["weather"] == cuaca]

    if hasil:
        tabel(hasil)
        print("Jumlah data:", len(hasil))
    else:
        print("Data tidak ditemukan.")   

def urutkan(data):
    print("1. Jarak")
    print("2. Berat")
    print("3. Waktu pengiriman")

    pilih = input("Pilih kolom: ")

    if pilih == "1":
        nama = "distance_km"
    elif pilih == "2":
        nama = "package_weight_kg"
    elif pilih == "3":
        nama = "delivery_time_hours"
    else:
        print("Pilihan tidak tersedia.")
        return

    arah = input("1. Kecil ke besar" 
    "2. Besar ke kecil\nPilih: ")

    if arah != "1" and arah != "2":
        print("Pilihan tidak tersedia.")
        return

    hasil = data.copy()

    for i in range(len(hasil)):
        for j in range(i + 1, len(hasil)):
            angka1 = float(hasil[i][nama])
            angka2 = float(hasil[j][nama])

            if arah == "1" and angka1 > angka2:
                hasil[i], hasil[j] = hasil[j], hasil[i]

            elif arah == "2" and angka1 < angka2:
                hasil[i], hasil[j] = hasil[j], hasil[i]

    tampilkan(hasil)

data = baca_data()

while True:
    print
    print("\n===== MENU PENGIRIMAN =====")
    print("1. Estimasi Waktu Pengiriman")
    print("2. Tampilkan Data Pengiriman")
    print("3. Tambah Data Pengiriman")
    print("4. Ubah Data Pengiriman")
    print("5. Hapus Data Pengiriman")
    print("6. Cari Data Pengiriman")
    print("7. Statistik Pengiriman")
    print("8. Filter Berdasarkan Cuaca")
    print("9. Urutkan Data Pengiriman")
    print("10. Keluar")

    menu = input("Pilih menu: ").strip()

    if menu == "1":
        estimasi(data)
    elif menu == "2":
        tampilkan(data)
    elif menu == "3":
        tambah(data)
    elif menu == "4":
        ubah(data)
    elif menu == "5":
        hapus(data)
    elif menu == "6":
        cari(data)
    elif menu == "7":
        statistik(data)
    elif menu == "8":
        filter_cuaca(data)
    elif menu == "9":
        urutkan(data)
    elif menu == "10":
        print("Terima kasih telah menggunakan program!")
        break
    else:
        print("Menu tidak tersedia.")