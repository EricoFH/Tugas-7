import os
from urllib.parse import quote

from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for)
from flask_wtf.csrf import CSRFError, CSRFProtect
from werkzeug.security import generate_password_hash

from data import (ARMADA, ATURAN, PASSWORD_HASH, PESAN_MASUK, USERNAME_RE,
                  USERS, periksa_username)
from forms import DaftarForm, KontakForm, ProdukForm

app = Flask(__name__)
# SECRET_KEY wajib untuk session, flash(), dan token CSRF.
# Di production simpan di environment variable (lihat pertemuan 13).
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "kunci-dev-ganti-di-production")
CSRFProtect(app)  # CSRF aktif untuk semua request POST


# ---------------------------------------------------------------- Filter template
@app.template_filter("rupiah")
def rupiah(nilai):
    return "Rp" + f"{nilai:,}".replace(",", ".")


@app.template_filter("foto")
def foto(nama_file, lebar=800):
    """Alamat gambar di Wikimedia Commons (sudah diperkecil ke `lebar` piksel)."""
    return ("https://commons.wikimedia.org/wiki/Special:FilePath/"
            + quote(nama_file.replace(" ", "_")) + f"?width={lebar}")


@app.template_filter("halaman_foto")
def halaman_foto(nama_file):
    """Halaman file di Commons (berisi nama fotografer dan lisensi)."""
    return "https://commons.wikimedia.org/wiki/File:" + quote(nama_file.replace(" ", "_"))


# ---------------------------------------------------------------- Route statis
@app.route("/")
def beranda():
    return render_template("beranda.html", unggulan=ARMADA[:3], hero=ARMADA[1], aturan=ATURAN)


@app.route("/tentang")
def tentang():
    return render_template("tentang.html")


@app.route("/produk")
def produk():
    return render_template("produk.html", daftar=ARMADA)


@app.route("/produk/<int:id>")
def produk_detail(id):
    mobil = next((m for m in ARMADA if m["id"] == id), None)
    if mobil is None:
        abort(404)
    return render_template("produk_detail.html", m=mobil)


# ---------------------------------------------------------------- FORM 1: Kontak (publik)
@app.route("/kontak", methods=["GET", "POST"])
def kontak():
    form = KontakForm()
    if form.validate_on_submit():
        PESAN_MASUK.append({
            "nama": form.nama.data,
            "email": form.email.data,
            "telepon": form.telepon.data,
            "mobil_id": form.mobil.data,
            "pesan": form.pesan.data,
        })
        flash(f"Terima kasih, {form.nama.data}! Pesan Anda sudah kami terima.", "success")
        return redirect(url_for("kontak"))  # PRG: aman di-refresh
    if request.method == "POST":
        flash("Pesan belum terkirim. Periksa kembali isian yang ditandai merah.", "danger")
    return render_template("kontak.html", form=form)


# ---------------------------------------------------------------- FORM 2: Daftar (publik)
@app.route("/daftar", methods=["GET", "POST"])
def daftar():
    form = DaftarForm()
    if request.method == "GET" and request.args.get("username"):
        # Datang dari halaman /cek: isi otomatis username yang barusan dicek
        form.username.data = request.args["username"].strip().lower()
    if form.validate_on_submit():
        USERS[form.username.data] = {
            "nama": form.nama.data, "peran": "Pelanggan",
            "bergabung": "Baru saja", "sewa": 0,
        }
        PASSWORD_HASH[form.username.data] = generate_password_hash(form.password.data)
        flash(f"Pendaftaran berhasil! Selamat datang, {form.nama.data}.", "success")
        return redirect(url_for("user_profile", username=form.username.data))  # PRG
    if request.method == "POST":
        flash("Pendaftaran gagal. Periksa kembali isian yang ditandai merah.", "danger")
    return render_template("daftar.html", form=form, aturan=ATURAN)


# ---------------------------------------------------------------- FORM 3: Dashboard admin
@app.route("/admin/produk")
def admin_produk():
    return render_template("admin_produk.html", daftar=ARMADA)


@app.route("/admin/produk/tambah", methods=["GET", "POST"])
def admin_produk_tambah():
    form = ProdukForm()
    if form.validate_on_submit():
        ARMADA.append({
            "id": max((m["id"] for m in ARMADA), default=0) + 1,
            "nama": form.nama.data,
            "kelas": form.kelas.data,
            "kursi": form.kursi.data,
            "transmisi": form.transmisi.data,
            "harga": form.harga.data,
            "stok": form.stok.data,
            "foto": None,
            "catatan": form.catatan.data or "Belum ada deskripsi.",
        })
        flash(f"Mobil “{form.nama.data}” berhasil ditambahkan.", "success")
        return redirect(url_for("admin_produk"))  # PRG
    if request.method == "POST":
        flash("Data belum tersimpan. Periksa kembali isian yang ditandai merah.", "danger")
    return render_template("admin_produk_tambah.html", form=form)


# ---------------------------------------------------------------- Cek username (route dinamis)
@app.route("/cek")
def cek_form():
    """Form pencarian (GET). Jika format valid, arahkan ke URL kanonik /cek/<username>."""
    q = request.args.get("username", "").strip().lower()
    if not q:
        return render_template("cek.html", username=None, aturan=ATURAN)
    if USERNAME_RE.fullmatch(q):
        return redirect(url_for("cek", username=q))
    status, pesan = periksa_username(q)
    return render_template("cek.html", username=q, status=status, pesan=pesan,
                           aturan=ATURAN), 400


@app.route("/cek/<username>")
def cek(username):
    kanonik = username.lower()
    if kanonik != username:  # /cek/Member_Dewi -> /cek/member_dewi
        return redirect(url_for("cek", username=kanonik), code=301)
    status, pesan = periksa_username(username)
    kode = 400 if status in ("tidak_valid", "dicadangkan") else 200
    return render_template("cek.html", username=username, status=status,
                           pesan=pesan, aturan=ATURAN), kode


@app.route("/user/<username>")
def user_profile(username):
    nama = username.lower()
    if not USERNAME_RE.fullmatch(nama):
        return redirect(url_for("cek", username=nama))
    data = USERS.get(nama)
    if data is None:
        abort(404)
    return render_template("user.html", username=nama, u=data)


# ---------------------------------------------------------------- Halaman 404
@app.errorhandler(404)
def halaman_tidak_ditemukan(error):
    return render_template("404.html"), 404


@app.errorhandler(CSRFError)
def csrf_gagal(error):
    # Token CSRF hilang / salah / kedaluwarsa -> request palsu ditolak
    return render_template("400.html", alasan="Token CSRF tidak valid atau sudah kedaluwarsa."), 400


if __name__ == "__main__":
    app.run(debug=True)
