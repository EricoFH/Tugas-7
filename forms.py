"""Form class Flask-WTF untuk Millena Car Rental (Tugas Individu 7)."""
from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, InputRequired,
                                Length, NumberRange, Optional, Regexp,
                                ValidationError)

from data import ARMADA, periksa_username


class AngkaField(IntegerField):
    """IntegerField dengan pesan error berbahasa Indonesia (dan tidak dobel saat kosong)."""

    def process_formdata(self, valuelist):
        if not valuelist or not valuelist[0].strip():
            self.data = None
            return
        try:
            self.data = int(valuelist[0])
        except ValueError:
            self.data = None
            raise ValueError("Harus berupa angka bulat")


def _bersihkan(nilai):
    """Filter: hapus spasi di awal/akhir."""
    return nilai.strip() if isinstance(nilai, str) else nilai


# ======================================================================
# FORM 1 (publik): Kontak / pemesanan  ->  /kontak
# ======================================================================
class KontakForm(FlaskForm):
    nama = StringField("Nama lengkap", filters=[_bersihkan], validators=[
        DataRequired(message="Nama wajib diisi"),
        Length(min=3, max=50, message="Nama harus 3 sampai 50 karakter")])
    email = StringField("Email", filters=[_bersihkan], validators=[
        DataRequired(message="Email wajib diisi"),
        Email(message="Format email tidak valid")])
    telepon = StringField("No. WhatsApp (opsional)", filters=[_bersihkan], validators=[
        Optional(),
        Regexp(r"^(\+62|62|0)8[0-9]{7,12}$",
               message="Contoh format: 081234567890")])
    mobil = SelectField("Mobil yang diminati", coerce=int, default=0)
    pesan = TextAreaField("Pesan / kebutuhan sewa", filters=[_bersihkan], validators=[
        DataRequired(message="Pesan wajib diisi"),
        Length(min=10, max=500, message="Pesan harus 10 sampai 500 karakter")])
    submit = SubmitField("Kirim Pesan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mobil.choices = [(0, "-- Belum menentukan --")] + [
            (m["id"], m["nama"]) for m in ARMADA]


# ======================================================================
# FORM 2 (publik): Pendaftaran akun  ->  /daftar
# ======================================================================
class DaftarForm(FlaskForm):
    nama = StringField("Nama lengkap", filters=[_bersihkan], validators=[
        DataRequired(message="Nama wajib diisi"),
        Length(min=3, max=50, message="Nama harus 3 sampai 50 karakter")])
    username = StringField(
        "Username",
        filters=[lambda x: x.strip().lower() if isinstance(x, str) else x],
        validators=[
            DataRequired(message="Username wajib diisi"),
            Length(min=4, max=15, message="Username harus 4 sampai 15 karakter"),
            Regexp(r"^[a-z0-9_]*$",
                   message="Hanya huruf kecil, angka, dan garis bawah (_)")])
    email = StringField("Email", filters=[_bersihkan], validators=[
        DataRequired(message="Email wajib diisi"),
        Email(message="Format email tidak valid")])
    umur = AngkaField("Umur", validators=[
        InputRequired(message="Umur wajib diisi (angka)"),
        NumberRange(min=17, max=99, message="Umur harus 17 sampai 99 tahun")])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password wajib diisi"),
        Length(min=8, message="Password minimal 8 karakter")])
    konfirmasi = PasswordField("Ulangi password", validators=[
        DataRequired(message="Konfirmasi password wajib diisi"),
        EqualTo("password", message="Password tidak sama")])
    submit = SubmitField("Daftar")

    # Validator kustom: memakai aturan username yang sama dengan halaman /cek
    def validate_username(self, field):
        status, pesan = periksa_username(field.data or "")
        if status in ("dicadangkan", "terdaftar"):
            raise ValidationError(pesan)


# ======================================================================
# FORM 3 (dashboard admin): Tambah armada  ->  /admin/produk/tambah
# ======================================================================
class ProdukForm(FlaskForm):
    nama = StringField("Nama mobil", filters=[_bersihkan], validators=[
        DataRequired(message="Nama mobil wajib diisi"),
        Length(min=3, max=50, message="Nama harus 3 sampai 50 karakter")])
    kelas = SelectField("Kategori / kelas", choices=[
        ("MPV", "MPV"), ("SUV", "SUV"), ("Hatchback", "Hatchback"),
        ("Sedan", "Sedan"), ("City Car", "City Car")])
    kursi = AngkaField("Jumlah kursi", validators=[
        InputRequired(message="Jumlah kursi wajib diisi (angka)"),
        NumberRange(min=2, max=12, message="Jumlah kursi 2 sampai 12")])
    transmisi = SelectField("Transmisi", choices=[
        ("Manual", "Manual"), ("Otomatis", "Otomatis"),
        ("Manual / Otomatis", "Manual / Otomatis")])
    harga = AngkaField("Harga sewa per hari (Rp)", validators=[
        InputRequired(message="Harga wajib diisi (angka)"),
        NumberRange(min=1, message="Harga harus lebih dari 0")])
    stok = AngkaField("Stok unit", validators=[
        InputRequired(message="Stok wajib diisi (angka)"),
        NumberRange(min=0, message="Stok tidak boleh negatif")])
    catatan = TextAreaField("Deskripsi", filters=[_bersihkan], validators=[
        Optional(),
        Length(max=200, message="Deskripsi maksimal 200 karakter")])
    submit = SubmitField("Simpan Mobil")

    def validate_nama(self, field):
        if any(m["nama"].lower() == (field.data or "").lower() for m in ARMADA):
            raise ValidationError("Mobil dengan nama ini sudah ada")
