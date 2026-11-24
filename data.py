"""Data contoh & aturan validasi username (dipisah dari app.py agar bisa dipakai forms.py)."""
import re

# ---------- Data contoh ----------
USERS = {
    "admin_rental": {"nama": "Rina Wijaya", "peran": "Admin", "bergabung": "Januari 2023"},
    "member_dewi": {"nama": "Dewi Anggraini", "peran": "Member", "bergabung": "Maret 2024", "sewa": 14},
    "pelanggan_budi": {"nama": "Budi Santoso", "peran": "Pelanggan", "bergabung": "Agustus 2025", "sewa": 2},
}

ARMADA = [
    {"id": 1, "nama": "Toyota Avanza", "kelas": "MPV", "kursi": 7, "transmisi": "Manual / Otomatis",
     "harga": 350000, "stok": 4,
     "foto": "2019 Toyota Avanza 1.3 G (front), East Surabaya.jpg",
     "catatan": "Pilihan paling umum untuk keluarga dan perjalanan dalam kota."},
    {"id": 2, "nama": "Toyota Avanza Veloz", "kelas": "MPV", "kursi": 7, "transmisi": "Otomatis",
     "harga": 400000, "stok": 2,
     "foto": "2012 Toyota Avanza Veloz (Indonesia) front quarter view.jpg",
     "catatan": "Varian lebih lengkap dari Avanza biasa, nyaman untuk perjalanan jauh."},
    {"id": 3, "nama": "Honda Brio Satya", "kelas": "Hatchback", "kursi": 5, "transmisi": "Manual / Otomatis",
     "harga": 280000, "stok": 5,
     "foto": "2023 Honda Brio Satya E, Citraland, West Surabaya.jpg",
     "catatan": "Irit dan lincah di jalan sempit, cocok untuk 2 sampai 4 orang."},
    {"id": 4, "nama": "Toyota Kijang Innova", "kelas": "MPV", "kursi": 7, "transmisi": "Manual / Otomatis",
     "harga": 550000, "stok": 2,
     "foto": "2013 Toyota Kijang Innova 2.0 V Luxury (front), West Surabaya.jpg",
     "catatan": "Kabin luas dan suspensi empuk untuk rombongan keluarga."},
    {"id": 5, "nama": "Toyota Fortuner", "kelas": "SUV", "kursi": 7, "transmisi": "Otomatis",
     "harga": 900000, "stok": 1,
     "foto": "2016 Toyota Fortuner VRZ (front), West Surabaya.jpg",
     "catatan": "SUV bertenaga untuk medan menanjak atau perjalanan dinas."},
]

PESAN_MASUK = []   # menampung pesan dari form kontak
PASSWORD_HASH = {}  # username -> hash password (hanya untuk demo, bukan database sungguhan)

# ---------- Validasi username ----------
USERNAME_RE = re.compile(r"[a-z0-9_]{4,15}")
RESERVED = {"admin", "owner", "root", "system"}
ATURAN = "4 sampai 15 karakter; hanya huruf kecil, angka, dan garis bawah (_)."


def periksa_username(username):
    """Kembalikan (status, pesan). Status: tidak_valid, dicadangkan, terdaftar, tersedia."""
    if len(username) < 4:
        return "tidak_valid", "Terlalu pendek. Minimal 4 karakter."
    if len(username) > 15:
        return "tidak_valid", "Terlalu panjang. Maksimal 15 karakter."
    if not USERNAME_RE.fullmatch(username):
        return "tidak_valid", "Hanya boleh huruf kecil, angka, dan garis bawah (_)."
    if username in RESERVED:
        return "dicadangkan", "Nama ini dicadangkan oleh sistem dan tidak bisa dipakai."
    if username in USERS:
        return "terdaftar", "Username sudah dipakai."
    return "tersedia", "Username ini masih tersedia."
