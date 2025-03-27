import pandas as pd
import os

data_file = "dataSales.csv"

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

# Fungsi CRUD
def add_data():
    df = read_data()
    new_id = input("Masukkan ID Sales: ")
    nama = input("Masukkan Nama Sales: ")
    tanggal = input("Masukkan Tanggal (YYYY-MM-DD): ")
    total = float(input("Masukkan Total Terjual (Rp): "))
    jumlah_barang = int(input("Masukkan Jumlah Barang Terjual: "))
    df = df.append({"ID": new_id, "Nama": nama, "Tanggal": tanggal, "Total Terjual": total, "Jumlah Barang Terjual": jumlah_barang}, ignore_index=True)
    save_data(df)
    print("Data berhasil ditambahkan!")

def view_data():
    df = read_data()
    if df.empty:
        print("Tidak ada data sales.")
        return
    print("Data Sales:")
    print(df)
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
    print(df)

def update_data():
    df = read_data()
    id_sales = input("Masukkan ID Sales yang ingin diubah: ")
    if id_sales not in df["ID"].values:
        print("ID tidak ditemukan!")
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

def delete_data():
    df = read_data()
    id_sales = input("Masukkan ID Sales yang ingin dihapus: ")
    if id_sales not in df["ID"].values:
        print("ID tidak ditemukan!")
        return
    df = df[df["ID"] != id_sales]
    save_data(df)
    print("Data berhasil dihapus!")

def search_data():
    df = read_data()
    print("Cari berdasarkan:")
    print("1. ID Sales")
    print("2. Nama Sales")
    choice = input("Pilihan: ")
    if choice == "1":
        id_sales = input("Masukkan ID Sales: ")
        result = binary_search(df, "ID", id_sales)
    elif choice == "2":
        nama = input("Masukkan Nama Sales: ")
        result = df[df["Nama"].str.contains(nama, case=False, na=False)]
    else:
        print("Pilihan tidak valid!")
        return
    print(result if not result.empty else "Data tidak ditemukan!")

def main():
    while True:
        print("\nMenu:")
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
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
