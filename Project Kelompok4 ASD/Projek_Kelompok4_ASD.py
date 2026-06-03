import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.json")

print("Database:", DATABASE)
print("Lokasi program:", os.getcwd())
print("File ditemukan?", os.path.exists(DATABASE))

# ============================================================
# DOUBLE LINKED LIST - Struktur Data Utama untuk Playlist
# ============================================================

class Node:
    """Node untuk Double Linked List"""
    def __init__(self, judul):
        self.judul = judul
        self.prev = None  # Pointer ke node sebelumnya
        self.next = None  # Pointer ke node berikutnya


class DoubleLinkedList:
    """Double Linked List untuk menyimpan playlist lagu"""

    def __init__(self):
        self.head = None   # Node pertama
        self.tail = None   # Node terakhir
        self.current = None  # Node yang sedang diputar
        self.size = 0

    def tambah(self, judul):
        """Tambah lagu ke akhir linked list"""
        node_baru = Node(judul)
        if self.head is None:
            self.head = node_baru
            self.tail = node_baru
        else:
            node_baru.prev = self.tail
            self.tail.next = node_baru
            self.tail = node_baru
        self.size += 1

    def hapus(self, judul):
        """Hapus lagu dari linked list berdasarkan judul"""
        current = self.head
        while current:
            if current.judul == judul:
                # Jika node yang dihapus adalah current yang sedang diputar
                if self.current == current:
                    self.current = current.next or current.prev

                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next  # Hapus head

                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev  # Hapus tail

                self.size -= 1
                return True
            current = current.next
        return False

    def ubah(self, judul_lama, judul_baru):
        """Ubah judul lagu di linked list"""
        current = self.head
        while current:
            if current.judul == judul_lama:
                current.judul = judul_baru
                return True
            current = current.next
        return False

    def ke_list(self):
        """Konversi linked list ke list Python biasa"""
        result = []
        current = self.head
        while current:
            result.append(current.judul)
            current = current.next
        return result

    def dari_list(self, data_list):
        """Isi linked list dari list Python"""
        self.head = None
        self.tail = None
        self.current = None
        self.size = 0
        for judul in data_list:
            self.tambah(judul)

    def get_node_by_index(self, index):
        """Ambil node berdasarkan index (0-based)"""
        current = self.head
        i = 0
        while current:
            if i == index:
                return current
            current = current.next
            i += 1
        return None

    def cari(self, keyword):
        """Cari lagu berdasarkan kata kunci"""
        keyword = keyword.lower()
        hasil = []
        current = self.head
        while current:
            if keyword in current.judul.lower():
                hasil.append(current.judul)
            current = current.next
        return hasil

    def sort_az(self):
        """Urutkan A-Z menggunakan bubble sort pada linked list"""
        if self.size <= 1:
            return
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current and current.next:
                if current.judul > current.next.judul:
                    current.judul, current.next.judul = current.next.judul, current.judul
                    swapped = True
                current = current.next

    def sort_za(self):
        """Urutkan Z-A menggunakan bubble sort pada linked list"""
        if self.size <= 1:
            return
        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current and current.next:
                if current.judul < current.next.judul:
                    current.judul, current.next.judul = current.next.judul, current.judul
                    swapped = True
                current = current.next

    def next_lagu(self, looping=False):
        """
        Pindah ke lagu berikutnya.
        Jika looping=True dan sudah di akhir, kembali ke awal.
        """
        if self.current is None:
            return None
        if self.current.next:
            self.current = self.current.next
        elif looping and self.head:
            self.current = self.head  # Loop ke awal
        else:
            return None  # Sudah di akhir, tidak loop
        return self.current.judul

    def prev_lagu(self, looping=False):
        """
        Pindah ke lagu sebelumnya.
        Jika looping=True dan sudah di awal, loncat ke akhir.
        """
        if self.current is None:
            return None
        if self.current.prev:
            self.current = self.current.prev
        elif looping and self.tail:
            self.current = self.tail  # Loop ke akhir
        else:
            return None  # Sudah di awal, tidak loop
        return self.current.judul


# ============================================================
# VARIABEL GLOBAL
# ============================================================

dll_playlist = DoubleLinkedList()  # Double Linked List utama
mode_looping = False  # Status looping


# ============================================================
# LOAD & SAVE DATA
# ============================================================

def load_data():
    global favorit, riwayat, play_count, mode_looping
    if os.path.exists(DATABASE):
        with open(DATABASE, "r", encoding="utf-8") as f:
            data = json.load(f)
            dll_playlist.dari_list(data.get("playlist", []))
            mode_looping = data.get("mode_looping", False)

def save_data():
    with open(DATABASE, "w", encoding="utf-8") as f:
        json.dump({
            "playlist": dll_playlist.ke_list(),
            "mode_looping": mode_looping
        }, f, indent=4, ensure_ascii=False)


# ============================================================
# FUNGSI-FUNGSI FITUR
# ============================================================

def lihat_playlist():
    lagu_list = dll_playlist.ke_list()
    if not lagu_list:
        print("Playlist kosong!")
        return
    print("\n--- PLAYLIST ---")
    for i, lagu in enumerate(lagu_list, 1):
        # Tandai lagu yang sedang diputar
        if dll_playlist.current and dll_playlist.current.judul == lagu:
            print(f"{i}. ▶ {lagu}  [Sedang Diputar]")
        else:
            print(f"{i}. {lagu}")
    print(f"\nMode Looping: {'ON 🔁' if mode_looping else 'OFF'}")


def tambah_lagu():
    judul = input("Judul lagu: ").strip()
    if judul:
        dll_playlist.tambah(judul)
        save_data()
        print(f"✓ '{judul}' ditambahkan ke playlist.")


def ubah_lagu():
    lihat_playlist()
    lagu_list = dll_playlist.ke_list()
    try:
        n = int(input("Nomor lagu yang ingin diubah: "))
        if 1 <= n <= len(lagu_list):
            judul_lama = lagu_list[n - 1]
            judul_baru = input("Judul baru: ").strip()
            if judul_baru:
                dll_playlist.ubah(judul_lama, judul_baru)
                save_data()
                print(f"✓ Berhasil diubah menjadi '{judul_baru}'.")
        else:
            print("Nomor tidak valid.")
    except ValueError:
        print("Input harus angka!")


def hapus_lagu():
    lihat_playlist()
    lagu_list = dll_playlist.ke_list()
    try:
        n = int(input("Nomor lagu yang ingin dihapus: "))
        if 1 <= n <= len(lagu_list):
            judul = lagu_list[n - 1]
            dll_playlist.hapus(judul)
            save_data()
            print(f"✓ '{judul}' dihapus dari playlist.")
        else:
            print("Nomor tidak valid.")
    except ValueError:
        print("Input harus angka!")


def cari_lagu():
    key = input("Kata kunci: ").strip()
    hasil = dll_playlist.cari(key)
    if hasil:
        print("\nHasil pencarian:")
        for lagu in hasil:
            print(f"  - {lagu}")
    else:
        print("Tidak ditemukan.")


def sort_az():
    dll_playlist.sort_az()
    save_data()
    print("✓ Playlist diurutkan A-Z.")


def sort_za():
    dll_playlist.sort_za()
    save_data()
    print("✓ Playlist diurutkan Z-A.")



def _putar(lagu):
    save_data()
    print(f"\n♪ Sedang memutar: {lagu}")
    if mode_looping:
        print("  [Mode Looping: ON 🔁]")


def putar_lagu():
    """Pilih lagu dari playlist untuk diputar"""
    lihat_playlist()
    lagu_list = dll_playlist.ke_list()
    if not lagu_list:
        return
    try:
        n = int(input("Pilih nomor lagu: "))
        if 1 <= n <= len(lagu_list):
            node = dll_playlist.get_node_by_index(n - 1)
            dll_playlist.current = node
            _putar(node.judul)
        else:
            print("Nomor tidak valid.")
    except:
        print("Input tidak valid.")


def next_lagu():
    """Pindah ke lagu berikutnya (mendukung looping)"""
    if dll_playlist.current is None:
        print("Belum ada lagu yang diputar. Pilih lagu terlebih dahulu (menu 5).")
        return
    judul = dll_playlist.next_lagu(looping=mode_looping)
    if judul:
        _putar(judul)
    else:
        print("Sudah di lagu terakhir. Aktifkan looping untuk kembali ke awal.")


def prev_lagu():
    """Pindah ke lagu sebelumnya (mendukung looping)"""
    if dll_playlist.current is None:
        print("Belum ada lagu yang diputar. Pilih lagu terlebih dahulu (menu 5).")
        return
    judul = dll_playlist.prev_lagu(looping=mode_looping)
    if judul:
        _putar(judul)
    else:
        print("Sudah di lagu pertama. Aktifkan looping untuk loncat ke akhir.")


def toggle_looping():
    """Aktifkan / matikan mode looping"""
    global mode_looping
    mode_looping = not mode_looping
    save_data()
    status = "ON 🔁" if mode_looping else "OFF"
    print(f"✓ Mode Looping sekarang: {status}")



# ============================================================
# PROGRAM UTAMA
# ============================================================

load_data()

while True:
    print("""
===== MP3 PLAYER (Double Linked List) =====
--- Manajemen Playlist ---
1.  Lihat Playlist
2.  Tambah Lagu
3.  Ubah Lagu
4.  Hapus Lagu
5.  Cari Lagu
6.  Urutkan A-Z
7.  Urutkan Z-A

--- Putar Lagu ---
8.  Putar Lagu (Pilih)
9. Next Lagu  ⏭
10. Previous Lagu  ⏮
11. Toggle Looping (ON/OFF)

--- Lainnya ---
0.  Keluar
============================================
""")

    menu = input("Pilih menu: ").strip()

    if menu == "1":
        lihat_playlist()
    elif menu == "2":
        tambah_lagu()
    elif menu == "3":
        ubah_lagu()
    elif menu == "4":
        hapus_lagu()
    elif menu == "5":
        cari_lagu()
    elif menu == "6":
        sort_az()
    elif menu == "7":
        sort_za()
    elif menu == "8":
        putar_lagu()
    elif menu == "9":
        next_lagu()
    elif menu == "10":
        prev_lagu()
    elif menu == "11":
        toggle_looping()
    elif menu == "0":
        print("Sampai jumpa!")
        break
    else:
        print("Menu tidak valid.")