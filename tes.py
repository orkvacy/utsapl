import pandas as pd
import os
from prettytable import PrettyTable
from termcolor import colored

data_file = "dataSales.csv"

def mergeSort(arr, key='ID', ascending=True):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    left = mergeSort(left, key, ascending)
    right = mergeSort(right, key, ascending)

    return merge(left, right, key, ascending)

def merge(left, right, key, ascending):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if key == 'Tanggal':
            left_val = pd.Timestamp(left[i][key])
            right_val = pd.Timestamp(right[j][key])
        else:
            left_val = left[i][key]
            right_val = right[j][key]
        
        if ascending:
            comparison = left_val <= right_val
        else:
            comparison = left_val >= right_val
        
        if comparison:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result

def binarySearch(arr, target, key='ID'):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = arr[mid][key]

        if mid_value == target:
            return mid
        elif mid_value < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  

def clear(): 
    os.system('cls || clear')

def readData():
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)
        df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%Y-%m-%d')
        return df
    return pd.DataFrame(columns=["ID", "Nama", "Tanggal", "Total Terjual", "Jumlah Barang Terjual"])

def saveDF(df):
    df_save = df.copy()
    df_save['Tanggal'] = df_save['Tanggal'].dt.strftime('%Y-%m-%d')
    df_save.to_csv(data_file, index=False)

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
            row['Tanggal'].strftime('%Y-%m-%d'), 
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
        
        df_list = df.to_dict('records')
        sorted_df = mergeSort(df_list, key='ID')
        
        if binarySearch(sorted_df, idBaru) != -1:
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
            pd.to_datetime(tanggal, format='%Y-%m-%d')
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
        "Tanggal": [pd.to_datetime(tanggal)], 
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
    
    df_list = df.to_dict('records')
    sorted_list = mergeSort(df_list, key=sortingDF, ascending=ascending)
    
    sortDF = pd.DataFrame(sorted_list)
    
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
    
    df_list = df.to_dict('records')
    sorted_df = mergeSort(df_list, key='ID')
    
    index_result = binarySearch(sorted_df, idSales)
    
    if index_result == -1:
        print("ID tidak ditemukan!")
        input("\nTekan Enter untuk melanjutkan...")
        clear()
        return
    
    index = df[df['ID'] == idSales].index[0]
    
    print("\nData Saat Ini:")
    dis(df.loc[df['ID'] == idSales])
    
    print("\nKosongkan input jika tidak ingin mengubah")
    
    nama = input(f"Nama Sales baru (sekarang: {df.at[index, 'Nama']}): ").strip()
    if nama:
        df.at[index, "Nama"] = nama
    
    while True:
        tanggal = input(f"Tanggal baru (sekarang: {df.at[index, 'Tanggal'].strftime('%Y-%m-%d')}): ").strip()
        if not tanggal:
            break
        try:
            df.at[index, "Tanggal"] = pd.to_datetime(tanggal, format='%Y-%m-%d')
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
    
    df_list = df.to_dict('records')
    sorted_df = mergeSort(df_list, key='ID')
    
    index_result = binarySearch(sorted_df, idSales)
    
    if index_result == -1:
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
        
        df_list = df.to_dict('records')
        sorted_df = mergeSort(df_list, key='ID')
        
        index_result = binarySearch(sorted_df, idSales)
        
        result = df[df["ID"] == idSales] if index_result != -1 else pd.DataFrame()
    
    elif choice == "2":
        nama = input("Masukkan Nama Sales: ").strip()
        result = df[df["Nama"].str.contains(nama, case=False, na=False)]
    
    elif choice == "3":
        try:
            tanggalMulai = input("Masukkan tanggal awal (YYYY-MM-DD): ").strip()
            tanggalAkhir = input("Masukkan tanggal akhir (YYYY-MM-DD): ").strip()
            
            tanggalMulai = pd.to_datetime(tanggalMulai, format='%Y-%m-%d')
            tanggalAkhir = pd.to_datetime(tanggalAkhir, format='%Y-%m-%d')
            
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