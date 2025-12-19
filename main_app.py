import logging
from repositories import ProductRepository
from services import IPaymentProcessor, ShoppingCart, CashPayment, DebitCardPayment
from models import Product # Diperlukan untuk type hint

# Inisialisasi Logger untuk file ini [cite: 158]
LOGGER = logging.getLogger('MAIN_APP')

class PosApp:
    """
    Kelas Orchestrator (Aplikasi Utama). 
    Tugasnya mengkoordinasi alur kerja dan menerapkan Dependency Injection (DI)[cite: 167].
    """
    
    def __init__(self, repository: ProductRepository, payment_processor: IPaymentProcessor):
        # Menerima komponen dari luar (Dependency Injection) [cite: 25, 168, 169]
        self.repository = repository
        self.payment_processor = payment_processor
        self.cart = ShoppingCart()
        LOGGER.info("POS Application Initialized.")

    def _display_menu(self):
        """Menampilkan daftar produk yang tersedia di repository[cite: 182]."""
        LOGGER.info("\n--- DAFTAR PRODUK ---")
        for p in self.repository.get_all():
            LOGGER.info(f"[{p.id}] {p.name} - Rp{p.price:,.0f}")

    def _handle_add_item(self):
        """Menangani input pengguna untuk menambah barang ke keranjang[cite: 198]."""
        product_id = input("Masukkan ID Produk: ").strip().upper()
        product = self.repository.get_by_id(product_id)
        
        if not product:
            LOGGER.warning("Produk tidak ditemukan.")
            return
        
        try:
            qty_input = input("Jumlah (default 1): ")
            quantity = int(qty_input) if qty_input else 1
            if quantity <= 0: 
                raise ValueError
            self.cart.add_item(product, quantity)
        except ValueError:
            LOGGER.error("Jumlah tidak valid.")

    def handle_checkout(self):
        """Melakukan proses pembayaran menggunakan payment processor yang di-inject[cite: 236]."""
        total = self.cart.total_price
        if total == 0:
            LOGGER.warning("Keranjang kosong.")
            return
            
        LOGGER.info(f"\nTotal Belanja: Rp{total:,.0f}")
        
        # Memanggil metode process tanpa peduli apakah itu Cash atau Debit (Polimorfisme) [cite: 242]
        success = self.payment_processor.process(total)
        
        if success:
            LOGGER.info("TRANSAKSI BERHASIL.")
            self._print_receipt()
            self.cart = ShoppingCart() # Reset keranjang setelah sukses [cite: 246]
        else:
            LOGGER.error("TRANSAKSI GAGAL.")

    def _print_receipt(self):
        """Mencetak struk belanja ke terminal[cite: 249]."""
        LOGGER.info("\n--- STRUK PEMBELIAN ---")
        for item in self.cart.get_items():
            LOGGER.info(f"{item.product.name} x{item.quantity} = Rp{item.subtotal:,.0f}")
        LOGGER.info("-----------------------")
        LOGGER.info(f"TOTAL AKHIR: Rp{self.cart.total_price:,.0f}")
        LOGGER.info("-----------------------")

# TITIK MASUK UTAMA (Orchestration) [cite: 273]
if __name__ == "__main__":
    # 1. Konfigurasi Logging agar muncul di terminal [cite: 276]
    logging.basicConfig(level=logging.INFO, format='%(name)s %(levelname)s %(message)s')
    
    # 2. Instansiasi Lapisan Data [cite: 278]
    repo = ProductRepository()
    
    # 3. Tantangan Latihan Mandiri: Menggunakan DebitCardPayment (Bukan CashPayment) 
    # Ini membuktikan kita bisa ganti fitur tanpa ubah class PosApp (Prinsip OCP/DIP)
    payment_method = DebitCardPayment() 
    
    # 4. Memasukkan (Inject) objek ke dalam Aplikasi Utama [cite: 282]
    app = PosApp(repository=repo, payment_processor=payment_method)
    
    # 5. Loop Menu CLI [cite: 284]
    while True:
        print("\nMenu Utama:")
        print("1. Tampilkan Produk")
        print("2. Tambah ke Keranjang")
        print("3. Checkout")
        print("4. Keluar")
        
        choice = input("Pilih opsi (1-4): ")
        
        if choice == "1":
            app._display_menu()
        elif choice == "2":
            app._handle_add_item()
        elif choice == "3":
            app.handle_checkout()
        elif choice == "4":
            LOGGER.info("Aplikasi dihentikan.")
            break
        else:
            LOGGER.warning("Pilihan tidak valid.")
