# [INF2153] Proyek Integrasi Sistem POS (Point-of-Sale)
## Pertemuan 13 - Membangun Aplikasi Multi Komponen

### Deskripsi Proyek
Proyek ini merupakan tahap integrasi dari berbagai komponen yang telah dibangun pada pertemuan sebelumnya menjadi sebuah sistem kasir (POS) yang utuh. Fokus utama praktikum ini adalah penerapan **Arsitektur Berlapis (Layered Architecture)** dan **Dependency Injection (DI)** untuk menciptakan sistem yang fleksibel dan mudah dikembangkan.

### Struktur File
Proyek ini dibagi menjadi beberapa modul untuk memisahkan tanggung jawab (Separation of Concerns):
- models.py: Mendefinisikan struktur data (Product dan CartItem) menggunakan Python Dataclasses.
- repositories.py: Lapisan data (Repository) yang menangani penyimpanan dan pengambilan data produk.
- services.py: Lapisan logika bisnis yang berisi sistem keranjang belanja dan antarmuka pembayaran (IPaymentProcessor).
- main_app.py: Kelas **Orchestrator** (PosApp) yang merakit seluruh komponen menggunakan Dependency Injection.

### Fitur Utama (Challenge OCP/DIP)
Proyek ini mendemonstrasikan **Open-Closed Principle** dengan penambahan fitur pembayaran baru:
- **DebitCardPayment**: Implementasi metode pembayaran kartu debit yang disuntikkan (*injected*) ke dalam sistem tanpa mengubah kode inti pada kelas PosApp.

### Cara Menjalankan
1. Pastikan Python 3.x telah terinstal di perangkat Anda.
2. Pastikan keempat file di atas berada dalam satu direktori yang sama.
3. Jalankan aplikasi melalui terminal:
   ```bash
   python main_app.py

### Histori Perubahan
Kode dikelola menggunakan Git. Lihat [https://github.com/Nabiilah527/P13_PBO/commits/main/]
