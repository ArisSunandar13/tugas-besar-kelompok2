import json
from uuid import uuid4


class Produk:
    def __init__(self, kode, nama, harga):
        self.id = str(uuid4())
        self.kode = kode
        self.nama = nama
        self.harga = harga

    def to_dict(self):
        return {
            "id": self.id,
            "kode": self.kode,
            "nama": self.nama,
            "harga": self.harga
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["kode"], data["nama"], data["harga"])


class Kasir:
    def __init__(self):
        self.produk_list = []
        self.order_list = []

    def tambah_produk(self, kode, nama, harga):
        produk = Produk(kode, nama, harga)
        self.produk_list.append(produk)
        self.simpan_database_produk()
        print("Produk berhasil ditambahkan!")

    def update_produk(self, kode, nama, harga):
        for produk in self.produk_list:
            if produk.kode == kode:
                produk.nama = nama
                produk.harga = harga
                self.simpan_database_produk()
                print("Produk berhasil diperbarui!")
                return
        print("Produk tidak ditemukan!")

    def hapus_produk(self, nama):
        for produk in self.produk_list:
            if produk.nama.lower() == nama.lower():
                self.produk_list.remove(produk)
                self.simpan_database_produk()
                print("Produk berhasil dihapus!")
                return
        print("Produk tidak ditemukan!")

    def customer_order(self):
        order = {}
        total_harga = 0

        print("=== PEMESANAN PELANGGAN ===")
        while True:
            nama_produk = input("Masukkan nama produk (0 untuk selesai): ")
            if nama_produk == "0":
                break

            jumlah_produk = int(input("Masukkan jumlah produk: "))

            ditemukan = False
            for produk in self.produk_list:
                if produk.nama.lower() == nama_produk.lower():
                    subtotal = produk.harga * jumlah_produk
                    order[produk.nama] = jumlah_produk
                    total_harga += subtotal
                    ditemukan = True
                    break

            if not ditemukan:
                print("Produk tidak ditemukan!")

        print("\n=== DETAIL PESANAN ===")
        for produk in self.produk_list:
            if produk.nama in order:
                print("Produk: ", produk.nama)
                print("Harga: ", produk.harga)
                print("Jumlah: ", order[produk.nama])
                print()

        print("Total Harga: ", total_harga)

        while True:
            uang = int(input("\nMasukkan jumlah uang: "))
            if uang >= total_harga:
                kembalian = uang - total_harga
                print("Kembalian: ", kembalian)
                order["total_harga"] = total_harga
                order["uang"] = uang
                order["kembalian"] = kembalian
                break
            else:
                print("Jumlah uang kurang!")

        self.order_list.append(order)
        self.simpan_database_struk()
        print("Pesanan berhasil ditambahkan!")

    def cetak_struk(self):
        print("=== STRUK TRANSAKSI ===")
        for order in self.order_list:
            print("\n=== DETAIL PESANAN ===")
            for produk in self.produk_list:
                if produk.nama in order:
                    print("Produk: ", produk.nama)
                    print("Harga: ", produk.harga)
                    print("Jumlah: ", order[produk.nama])
                    print("Subtotal: ", produk.harga * order[produk.nama])
                    print()
            print("Total Harga: ", order.get("total_harga", 0))
            print("Jumlah Uang: ", order.get("uang", 0))
            print("Kembalian: ", order.get("kembalian", 0))
            print("--------------------")

    def simpan_database_produk(self):
        with open("./database/db_produk.json", "w") as file:
            produk_data = []
            for produk in self.produk_list:
                produk_data.append({
                    "kode": produk.kode,
                    "nama": produk.nama,
                    "harga": produk.harga
                })
            json.dump(produk_data, file)
        print("Database produk berhasil disimpan!")

    def simpan_database_struk(self):
        with open("./database/db_struk.json", "w") as file:
            struk_data = []
            for order in self.order_list:
                order_data = {}
                for produk_nama, jumlah in order.items():
                    order_data[produk_nama] = jumlah
                struk_data.append(order_data)
            json.dump(struk_data, file)
        print("Database struk berhasil disimpan!")

    def load_database_produk(self):
        try:
            with open("./database/db_produk.json", "r") as file:
                produk_data = json.load(file)
                for data in produk_data:
                    produk = Produk.from_dict(data)
                    self.produk_list.append(produk)
            print("Database produk berhasil dimuat!")
        except FileNotFoundError:
            print("Database produk tidak ditemukan.")

    def load_database_struk(self):
        try:
            with open("./database/db_struk.json", "r") as file:
                struk_data = json.load(file)
                for order_data in struk_data:
                    order = {}
                    for produk_nama, jumlah in order_data.items():
                        for produk in self.produk_list:
                            if produk.nama == produk_nama:
                                order[produk.nama] = jumlah
                                break
                    self.order_list.append(order)
            print("Database struk berhasil dimuat!")
        except FileNotFoundError:
            print("Database struk tidak ditemukan.")

    def list_produk(self):
        print("=== DAFTAR PRODUK ===")
        if len(self.produk_list) == 0:
            print("Tidak ada produk yang tersedia.")
        else:
            for produk in self.produk_list:
                print("Kode: ", produk.kode)
                print("Nama: ", produk.nama)
                print("Harga: ", produk.harga)
                print("--------------------")

    def cari_produk(self, keyword):
        print("=== CARI PRODUK ===")
        found = False
        for produk in self.produk_list:
            if keyword.lower() in produk.nama.lower():
                print("Kode: ", produk.kode)
                print("Nama: ", produk.nama)
                print("Harga: ", produk.harga)
                print("--------------------")
                found = True
        if not found:
            print("Produk tidak ditemukan.")


def main():
    kasir = Kasir()
    kasir.load_database_produk()
    kasir.load_database_struk()

    while True:
        print("\n=== MENU KASIR ===")
        print("1. Tambah Produk")
        print("2. Update Produk")
        print("3. Hapus Produk")
        print("4. Pesanan Pelanggan")
        print("5. Cetak Struk")
        print("6. Daftar Produk")
        print("7. Cari Produk")
        print("0. Keluar")

        pilihan = input("Masukkan pilihan: ")

        if pilihan == "1":
            kode = input("Masukkan kode produk: ")
            nama = input("Masukkan nama produk: ")
            harga = int(input("Masukkan harga produk: "))
            kasir.tambah_produk(kode, nama, harga)
        elif pilihan == "2":
            kode = input("Masukkan kode produk yang akan diperbarui: ")
            nama = input("Masukkan nama baru produk: ")
            harga = int(input("Masukkan harga baru produk: "))
            kasir.update_produk(kode, nama, harga)
        elif pilihan == "3":
            nama = input("Masukkan nama produk yang akan dihapus: ")
            kasir.hapus_produk(nama)
        elif pilihan == "4":
            kasir.customer_order()
        elif pilihan == "5":
            kasir.cetak_struk()
        elif pilihan == "6":
            kasir.list_produk()
        elif pilihan == "7":
            keyword = input("Masukkan kata kunci produk: ")
            kasir.cari_produk(keyword)
        elif pilihan == "0":
            kasir.simpan_database_produk()
            kasir.simpan_database_struk()
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()
