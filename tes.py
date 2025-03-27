import pandas as pd
import os
from prettytable import PrettyTable
from termcolor import colored
data_file = "dataSales.csv"

def clear(): #buat clear terminal
    os.system('cls || clear')


def readData():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    return pd.DataFrame(columns=["ID", "Nama", "Tanggal", "Total Terjual", "Jumlah Barang Terjual"])


def saveDF(df):
    df.to_csv(data_file, index=False)

def dis(df):
    if df.empty:
        print("Tidak ada data sales.")
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "Nama", "Tanggal", "Total Terjual", "Jumlah Barang Terjual"]
    
    for _, row in df.iterrows():
        table.add_row([
            row['ID'], 
            row['Nama'], 
            row['Tanggal'], 
            f"Rp {row['Total Terjual']:,.2f}", 
            row['Jumlah Barang Terjual']
        ])
    
    print(table)

def add():
    clear()
    df = readData()
    
    while True:
        idBaru = input("Masukkan ID Sales: ").strip()
        if not idBaru:
            print("ID Sales tidak boleh kosong!")
            continue
        
        if idBaru in df['ID'].values:
            print("ID Sales sudah ada. Silakan masukkan ID yang berbeda.")
            continue
        
        break
    
    while True:
        nama = input("Masukkan Nama Sales: ").strip()
        if not nama:
            print("Nama Sales tidak boleh kosong!")
            continue
        break
    
    while True:
        tanggal = input("Masukkan Tanggal (YYYY-MM-DD): ").strip()
        try:
            pd.to_datetime(tanggal)
            break
        except ValueError:
            print("Format tanggal salah. Gunakan format YYYY-MM-DD.")
    
    while True:
        try:
            total = float(input("Masukkan Total Terjual (Rp): "))
            if total < 0:
                print("Total terjual tidak boleh negatif!")
                continue
            break
        except ValueError:
            print("Masukkan angka yang valid!")
    
    while True:
        try:
            jumlahBarang = int(input("Masukkan Jumlah Barang Terjual: "))
            if jumlahBarang < 0:
                print("Jumlah barang tidak boleh negatif!")
                continue
            break
        except ValueError:
            print("Masukkan angka bulat yang valid!")
    
    dataBaru = pd.DataFrame({
        "ID": [idBaru], 
        "Nama": [nama], 
        "Tanggal": [tanggal], 
        "Total Terjual": [total], 
        "Jumlah Barang Terjual": [jumlahBarang]
    })
    
    df = pd.concat([df, dataBaru], ignore_index=True)
    saveDF(df)
    
    clear()
    print("Data berhasil ditambahkan!")
    input("\nTekan Enter untuk melanjutkan...")
    clear()

def tabel():
    clear()
    df = readData()
    if df.empty:
        print("Tidak ada data sales.")
        input("\nTekan Enter untuk melanjutkan...")
        return
    
    print("Data Sales:")
    dis(df)
    
    print("\nPilih Sortir:")
    print("1. Tanggal")
    print("2. Total Terjual")
    print("3. ID Sales")
    print("4. Jumlah Barang Terjual")
    print("0. Kembali")
    
    choice = input("Pilihan: ")
    
    if choice == "0":
        return
    
    kolomDF = {
        "1": "Tanggal", 
        "2": "Total Terjual", 
        "3": "ID", 
        "4": "Jumlah Barang Terjual"
    }
    
    if choice not in kolomDF:
        print("Pilihan tidak valid!")
        input("\nTekan Enter untuk melanjutkan...")
        clear()
        return
    
    while True:
        ascending_input = input("Urutkan Ascending? (Y/N): ").lower()
        if ascending_input in ['y', 'n']:
            ascending = ascending_input == 'y'
            break
        else:
            print("Masukan tidak valid. Silakan ketik Y atau N.")
    
    sortingDF = kolomDF[choice]
    
    if sortingDF in ["Total Terjual", "Jumlah Barang Terjual"]:
        df[sortingDF] = pd.to_numeric(df[sortingDF], errors='coerce')
    
    sortDF = df.sort_values(by=sortingDF, ascending=ascending)
    
    clear()
    print(f"Data diurutkan berdasarkan {sortingDF} {'(Ascending)' if ascending else '(Descending)'}:")
    dis(sortDF)
    
    input("\nTekan Enter untuk melanjutkan...")
    clear()

def update():
    clear()
    df = readData()
    
    dis(df)
    
    idSales = input("Masukkan ID Sales yang ingin diubah: ").strip()
    
    cariData = df[df["ID"] == idSales]
    
    if cariData.empty:
        print("ID tidak ditemukan!")
        input("\nTekan Enter untuk melanjutkan...")
        clear()
        return
    
    index = cariData.index[0]
    
    print("\nData Saat Ini:")
    dis(cariData)
    
    print("\nKosongkan input jika tidak ingin mengubah")
    
    nama = input(f"Nama Sales baru (sekarang: {df.at[index, 'Nama']}): ").strip()
    if nama:
        df.at[index, "Nama"] = nama
    
    while True:
        tanggal = input(f"Tanggal baru (sekarang: {df.at[index, 'Tanggal']}): ").strip()
        if not tanggal:
            break
        try:
            pd.to_datetime(tanggal)
            df.at[index, "Tanggal"] = tanggal
            break
        except ValueError:
            print("Format tanggal salah. Gunakan format YYYY-MM-DD.")
    
    while True:
        total = input(f"Total Terjual baru (sekarang: Rp {df.at[index, 'Total Terjual']:,.2f}): ").strip()
        if not total:
            break
        try:
            totalTerjual = float(total)
            if totalTerjual < 0:
                print("Total terjual harus lebih dari 0!")
                continue
            df.at[index, "Total Terjual"] = totalTerjual
            break
        except ValueError:
            print("Masukkan angka yang valid!")
    
    while True:
        jumlahBarang = input(f"Jumlah Barang Terjual baru (sekarang: {df.at[index, 'Jumlah Barang Terjual']}): ").strip()
        if not jumlahBarang:
            break
        try:
            jumlahBarang_int = int(jumlahBarang)
            if jumlahBarang_int < 0:
                print("Jumlah barang tidak boleh negatif!")
                continue
            df.at[index, "Jumlah Barang Terjual"] = jumlahBarang_int
            break
        except ValueError:
            print("Masukkan angka bulat yang valid!")
    
    saveDF(df)
    
    clear()
    print("Data berhasil diperbarui!")
    input("\nTekan Enter untuk melanjutkan...")
    clear()

def hapus():
    clear()
    df = readData()
    dis(df)
    
    idSales = input("Masukkan ID Sales yang ingin dihapus: ").strip()
    
    cariData = df[df["ID"] == idSales]
    
    if cariData.empty:
        print("ID tidak ditemukan!")
        input("\nTekan Enter untuk melanjutkan...")
        clear()
        return
    
    konfirmasi = input(f"Anda yakin ingin menghapus data sales dengan ID {idSales}? (Y/N): ").lower()
    
    if konfirmasi == 'y':
        df = df[df["ID"] != idSales]
        saveDF(df)
        
        clear()
        print("Data berhasil dihapus!")
    else:
        clear()
        print("Penghapusan dibatalkan.")
    
    input("\nTekan Enter untuk melanjutkan...")
    clear()

def find():
    clear()
    df = readData()
    
    print("Cari berdasarkan:")
    print("1. ID Sales")
    print("2. Nama Sales")
    print("3. Rentang Tanggal")
    print("4. Rentang Total Terjual")
    print("0. Kembali")
    
    choice = input("Pilihan: ")
    
    if choice == "0":
        return
    
    if choice == "1":
        idSales = input("Masukkan ID Sales: ").strip()
        result = df[df["ID"] == idSales]
    
    elif choice == "2":
        nama = input("Masukkan Nama Sales: ").strip()
        result = df[df["Nama"].str.contains(nama, case=False, na=False)]
    
    elif choice == "3":
        try:
            tanggalMulai = input("Masukkan tanggal awal (YYYY-MM-DD): ").strip()
            tanggalAkhir = input("Masukkan tanggal akhir (YYYY-MM-DD): ").strip()
            
            tanggalMulai = pd.to_datetime(tanggalMulai)
            tanggalAkhir = pd.to_datetime(tanggalAkhir)
            
            df['Tanggal'] = pd.to_datetime(df['Tanggal'])
            result = df[(df['Tanggal'] >= tanggalMulai) & (df['Tanggal'] <= tanggalAkhir)]
        except ValueError:
            print("Format tanggal salah!")
            input("\nTekan Enter untuk melanjutkan...")
            clear()
            return
    
    elif choice == "4":
        try:
            minTotal = float(input("Masukkan total minimum: "))
            maxTotal = float(input("Masukkan total maksimum: "))
            
            result = df[(df['Total Terjual'] >= minTotal) & (df['Total Terjual'] <= maxTotal)]
        except ValueError:
            print("Masukkan angka yang valid!")
            input("\nTekan Enter untuk melanjutkan...")
            clear()
            return
    
    else:
        print("Pilihan tidak valid!")
        input("\nTekan Enter untuk melanjutkan...")
        clear()
        return
    
    clear()
    if result.empty:
        print("Tidak ada data yang ditemukan.")
    else:
        print("Hasil Pencarian:")
        dis(result)
    
    input("\nTekan Enter untuk melanjutkan...")
    clear()

def main():
    clear()
    while True:
        menu_table = PrettyTable()
        menu_table.field_names = [colored("APLIKASI MANAJEMEN DATA SALES", "white")]
        menu_table.align[menu_table.field_names[0]] = 'c'
        menu_table.header = True
        menu_table.border = True
        menu_table.hrules = 1  
        
        menu_table.horizontal_char = colored('─', 'yellow')
        menu_table.vertical_char = colored('│', 'yellow')
        menu_table.junction_char = colored('┼', 'yellow')

        # Format menu items dengan lebar yang konsisten
        menu_items = [
            colored("1. [📋] Lihat Data", "light_cyan").ljust(25),
            colored("2. [➕] Tambah Data", "light_cyan").ljust(25), 
            colored("3. [✏️] Ubah Data", "light_cyan").ljust(25),
            colored("4. [🗑️] Hapus Data", "light_cyan").ljust(25), 
            colored("5. [🔍] Cari Data", "light_cyan").ljust(25),
            colored("0. [❌] Keluar", "light_red").ljust(25)
        ]

        for item in menu_items:
            menu_table.add_row([item])

        print("\n" + str(menu_table) + "\n")
        
        choice = input("Pilihan: ").strip()
        
        if choice == "1":
            tabel()
        elif choice == "2":
            add()
        elif choice == "3":
            update()
        elif choice == "4":
            hapus()
        elif choice == "5":
            find()
        elif choice == "0":
            print("Terima kasih telah menggunakan aplikasi!")
            break
        else:
            clear()
            print("Pilihan tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")
            clear()

if __name__ == "__main__":
    main()

