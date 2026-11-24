# Millena Car Rental (Fase 1, 2 & Tugas Individu 7 – Forms)

Aplikasi Flask rental mobil. Fase 1 & 2 (routing + cek username) dipertahankan,
ditambah **form dengan Flask-WTF** sesuai Pertemuan 12.

## Cara Menjalankan
```bash
python -m venv venv
venv\Scripts\activate          # Windows  (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python app.py
```
Buka http://127.0.0.1:5000

## Route
| Route | Keterangan |
|---|---|
| `/`, `/tentang`, `/produk`, `/produk/<int:id>` | Halaman publik |
| `/cek`, `/cek/<username>`, `/user/<username>` | Cek username & profil |
| `/kontak` | **Form 1** – kontak / pemesanan (publik) |
| `/daftar` | **Form 2** – pendaftaran akun (publik) |
| `/admin/produk` | Dashboard admin: tabel armada |
| `/admin/produk/tambah` | **Form 3** – tambah mobil (dashboard admin) |

## Checklist Tugas Individu 7
| # | Ketentuan | Implementasi |
|---|---|---|
| 1 | Minimal 2 form | `KontakForm`, `DaftarForm`, `ProdukForm` (`forms.py`) |
| 2 | Flask-WTF, min. 4 validator berbeda | `DataRequired`, `InputRequired`, `Length`, `Email`, `EqualTo`, `NumberRange`, `Regexp`, `Optional` + validator kustom (`validate_username`, `validate_nama`) |
| 3 | CSRF aktif di semua form | `{{ form.hidden_tag() }}` di tiap form POST + `CSRFProtect(app)` |
| 4 | Error di bawah field, input benar tetap terisi | macro `field()` di `templates/_macros.html` (`is-invalid` + `invalid-feedback`) |
| 5 | PRG + flash | `redirect(url_for(...))` setelah POST sukses + `flash()` kategori success/danger |
| 6 | Bootstrap | Bootstrap 5.3 (CDN) di `base.html` |

> Form pencarian di `/cek` memakai **GET** sehingga tidak memerlukan token CSRF.
> Data disimpan di list/dict Python, jadi hilang saat server restart.

## Struktur
```
app.py            route & logika
data.py           data contoh + aturan validasi username
forms.py          class form Flask-WTF
templates/        base.html, _macros.html, kontak.html, daftar.html, admin_produk*.html, ...
```

## Production
Set `SECRET_KEY` lewat environment variable:
```bash
set SECRET_KEY=isi-kunci-acak-panjang        # Windows
export SECRET_KEY=isi-kunci-acak-panjang     # Mac/Linux
```
