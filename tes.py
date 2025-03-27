import pandas as pd
import os
from prettytable import PrettyTable

data_file = "dataSales.csv"

# Fungsi untuk membersihkan layar terminal
def clear_screen():
    # Untuk Windows
    if os.name == 'nt':
        os.system('cls')
    # Untuk Unix/Linux/MacOS
    else:
        os.system('clear')

# Fungsi untuk membaca data dari CSV
def read_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    return pd.DataFrame(columns=["ID", "Nama", "Tanggal", "Total Terjual", "Jumlah Barang Terjual"])

# Fungsi untuk menyimpan data ke CSV
def save_data(df):
    df.to_csv(data_file, index=False)

# Fungsi Merge Sort
def merge_sort(df, column, ascending=True):
    if len(df) <= 1:
        return df
    mid = len(df) // 2
    left = merge_sort(df.iloc[:mid], column, ascending)
    right = merge_sort(df.iloc[mid:], column, ascending)
    return merge(left, right, column, ascending)

def merge(left, right, column, ascending):
    result = pd.DataFrame(columns=left.columns)
    i = j = 0
    while i < len(left) and j < len(right):
        if (left.iloc[i][column] <= right.iloc[j][column]) if ascending else (left.iloc[i][column] >= right.iloc[j][column]):
            result = pd.concat([result, left.iloc[i:i+1]])
            i += 1
        else:
            result = pd.concat([result, right.iloc[j:j+1]])
            j += 1
    result = pd.concat([result, left.iloc[i:]])
    result = pd.concat([result, right.iloc[j:]])
    return result

# Fungsi Binary Search
def binary_search(df, column, value):
    df_sorted = merge_sort(df, column, ascending=True)
    low, high = 0, len(df_sorted) - 1
    while low <= high:
        mid = (low + high) // 2
        if df_sorted.iloc[mid][column] == value:
            return df_sorted.iloc[mid]
        elif df_sorted.iloc[mid][column] < value:
            low = mid + 1
        else:
            high = mid - 1
    return None

# Fungsi untuk menampilkan data dengan PrettyTable
def display_data(df):
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

# Fungsi CRUD
def add_data():
    clear_screen()
    df = read_data()
    new_id = input("Masukkan ID Sales: ")
    nama = input("Masukkan Nama Sales: ")
    tanggal = input("Masukkan Tanggal (YYYY-MM-DD): ")
    total = float(input("Masukkan Total Terjual (Rp): "))
    jumlah_barang = int(input("Masukkan Jumlah Barang Terjual: "))
    
    new_row = pd.DataFrame({
        "ID": [new_id], 
        "Nama": [nama], 
        "Tanggal": [tanggal], 
        "Total Terjual": [total], 
        "Jumlah Barang Terjual": [jumlah_barang]
    })
    
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    print("Data berhasil ditambahkan!")
    input("\nTekan Enter untuk melanjutkan...")
    clear_screen()

def view_data():
    clear_screen()
    df = read_data()
    if df.empty:
        print("Tidak ada data sales.")
        input("\nTekan Enter untuk melanjutkan...")
        return
    
    print("Data Sales:")
    display_data(df)
    
    print("\nPilih Sortir:")
    print("1. Tanggal")
    print("2. Total Terjual")
    print("3. ID Sales")
    print("4. Jumlah Barang Terjual")
    choice = input("Pilihan: ")
    ascending = input("Ascending (Y/N)?: ").lower() == 'y'
    
    columns = {"1": "Tanggal", "2": "Total Terjual", "3": "ID", "4": "Jumlah Barang Terjual"}
    if choice in columns:
        df = merge_sort(df, columns[choice], ascending)
        clear_screen()
        print(f"Data diurutkan berdasarkan {columns[choice]} {'(Ascending)' if ascending else '(Descending)'}:")
        display_data(df)
    
    input("\nTekan Enter untuk melanjutkan...")
    clear_screen()

def update_data():
    clear_screen()
    df = read_data()
    id_sales = input("Masukkan ID Sales yang ingin diubah: ")
    if id_sales not in df["ID"].values:
        print("ID tidak ditemukan!")
        input("\nTekan Enter untuk melanjutkan...")
        clear_screen()
        return
    
    index = df[df["ID"] == id_sales].index[0]
    nama = input("Masukkan Nama Sales baru (kosong untuk tidak mengubah): ")
    tanggal = input("Masukkan Tanggal baru (kosong untuk tidak mengubah): ")
    total = input("Masukkan Total Terjual baru (kosong untuk tidak mengubah): ")
    jumlah_barang = input("Masukkan Jumlah Barang Terjual baru (kosong untuk tidak mengubah): ")
    
    if nama:
        df.at[index, "Nama"] = nama
    if tanggal:
        df.at[index, "Tanggal"] = tanggal
    if total:
        df.at[index, "Total Terjual"] = float(total)
    if jumlah_barang:
        df.at[index, "Jumlah Barang Terjual"] = int(jumlah_barang)
    
    save_data(df)
    print("Data berhasil diperbarui!")
    input("\nTekan Enter untuk melanjutkan...")
    clear_screen()

def delete_data():
    clear_screen()
    df = read_data()
    id_sales = input("Masukkan ID Sales yang ingin dihapus: ")
    if id_sales not in df["ID"].values:
        print("ID tidak ditemukan!")
        input("\nTekan Enter untuk melanjutkan...")
        clear_screen()
        return
    
    df = df[df["ID"] != id_sales]
    save_data(df)
    print("Data berhasil dihapus!")
    input("\nTekan Enter untuk melanjutkan...")
    clear_screen()

def search_data():
    clear_screen()
    df = read_data()
    print("Cari berdasarkan:")
    print("1. ID Sales")
    print("2. Nama Sales")
    choice = input("Pilihan: ")
    
    if choice == "1":
        id_sales = input("Masukkan ID Sales: ")
        result = binary_search(df, "ID", id_sales)
        if result is not None:
            result_df = pd.DataFrame([result])
            clear_screen()
            print("Data ditemukan:")
            display_data(result_df)
        else:
            print("Data tidak ditemukan!")
    elif choice == "2":
        nama = input("Masukkan Nama Sales: ")
        result = df[df["Nama"].str.contains(nama, case=False, na=False)]
        clear_screen()
        if not result.empty:
            print(f"Hasil pencarian untuk nama: {nama}")
            display_data(result)
        else:
            print("Data tidak ditemukan!")
    else:
        print("Pilihan tidak valid!")
    
    input("\nTekan Enter untuk melanjutkan...")
    clear_screen()

def main():
    clear_screen()
    while True:
        print("\nAplikasi Manajemen Data Sales")
        print("==============================")
        print("1. Lihat Data")
        print("2. Tambah Data")
        print("3. Ubah Data")
        print("4. Hapus Data")
        print("5. Cari Data")
        print("0. Keluar")
        
        choice = input("Pilihan: ")
        
        if choice == "1":
            view_data()
        elif choice == "2":
            add_data()
        elif choice == "3":
            update_data()
        elif choice == "4":
            delete_data()
        elif choice == "5":
            search_data()
        elif choice == "0":
            print("Terima kasih telah menggunakan aplikasi!")
            break
        else:
            clear_screen()
            print("Pilihan tidak valid!")
            input("\nTekan Enter untuk melanjutkan...")
            clear_screen()

if __name__ == "__main__":
    main()