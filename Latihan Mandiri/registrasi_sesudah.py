import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Konfigurasi Logging 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(name)s %(message)s'
)
LOGGER = logging.getLogger('CheckoutSystem')

@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

class IPaymentProcessor(ABC):
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

class INotificationService(ABC):
    @abstractmethod
    def send(self, order: Order):
        pass

class CheckoutService:
    """Kelas high-level untuk mengkoordinasi proses transaksi pembayaran. 
    
    Kelas ini memisahkan logika pembayaran dan notifikasi (memenuhi SRP). 
    """

    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        """Menginisialisasi CheckoutService dengan dependensi yang diperlukan. 

        Args:
            payment_processor (IPaymentProcessor): Implementasi interface pembayaran. 
            notifier (INotificationService): Implementasi interface notifikasi. 
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order) -> bool:
        """Menjalankan proses checkout dan memvalidasi pembayaran. 

        Args:
            order (Order): Objek pesanan yang akan diproses. 

        Returns:
            bool: True jika checkout sukses, False jika gagal. 
        """
        LOGGER.info(f"Memulai checkout untuk {order.customer_name}. Total: {order.total_price}") 
        
        payment_success = self.payment_processor.process(order) 
        
        if payment_success: 
            order.status = "paid" 
            self.notifier.send(order) 
            LOGGER.info("Checkout Sukses. Status pesanan: PAID.") 
            return True 
        else:
            LOGGER.error("Pembayaran gagal. Transaksi dibatalkan.") 
            return False 

# Implementasi konkrit untuk testing
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        pass

if __name__ == "__main__":
    order_andi = Order("Andi", 500000)
    service = CheckoutService(CreditCardProcessor(), EmailNotifier())
    service.run_checkout(order_andi)