## Petunjuk Instalasi dan Penggunaan Aplikasi Apotek

Berikut adalah langkah-langkah untuk menginstal dan menjalankan aplikasi apotek:

### Clone Repo

Clone repository aplikasi apotek dari GitHub:

```bash
git clone <URL_repo_apotek>
```

### Import Database

Import file SQL `apotek.sql` ke dalam sistem database Anda. Anda dapat menggunakan manajemen database yang Anda pilih untuk mengimpor file SQL ini. Pastikan untuk membuat database dengan nama yang sesuai sebelum mengimpor.

### Buat dan Aktifkan Virtual Environment

Buat virtual environment di dalam direktori proyek Anda dan aktifkan:

```bash
cd nama_direktori_proyek
python -m venv env
env\Scripts\activate  # untuk Windows
source env/bin/activate  # untuk macOS/Linux
```

### Install Dependensi

Instal semua dependensi yang diperlukan untuk aplikasi dengan menjalankan perintah:

```bash
pip install -r requirements.txt
```

### Jalankan Aplikasi

Jalankan aplikasi menggunakan perintah:

```bash
python run.py
```

Setelah menjalankan perintah tersebut, aplikasi apotek akan berjalan dan dapat diakses melalui browser web pada alamat yang ditampilkan di terminal.

Dengan mengikuti langkah-langkah di atas, Anda akan dapat menginstal dan menjalankan aplikasi apotek dengan sukses.