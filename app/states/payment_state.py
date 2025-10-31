import reflex as rx
import datetime
from typing import TypedDict, Optional, Literal

PaymentStatus = Literal["Pending", "Completed", "Failed"]


class PaymentData(TypedDict):
    id: int
    transaction_id: int
    amount: float
    payment_method: str
    mpesa_code: Optional[str]
    status: PaymentStatus
    timestamp: str


class PaymentState(rx.State):
    """Manages payment tracking and status."""

    payments: list[PaymentData] = []
    filter_status: str = "ALL"
    transaction_id: Optional[int] = None
    amount: float = 0.0
    payment_method: str = ""
    mpesa_code: Optional[str] = None

    @rx.event
    def add_payment(self, status: PaymentStatus):
        if not self.transaction_id:
            return
        new_payment = {
            "id": len(self.payments) + 1,
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "mpesa_code": self.mpesa_code,
            "status": status,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        self.payments.append(new_payment)
        self._reset_fields()

    def _reset_fields(self):
        self.transaction_id = None
        self.amount = 0.0
        self.payment_method = ""
        self.mpesa_code = None

    @rx.var
    def filtered_payments(self) -> list[PaymentData]:
        if self.filter_status == "ALL":
            return self.payments
        return [p for p in self.payments if p["status"] == self.filter_status]

    @rx.var
    def completed_count(self) -> int:
        return len([p for p in self.payments if p["status"] == "Completed"])

    @rx.var
    def pending_count(self) -> int:
        return len([p for p in self.payments if p["status"] == "Pending"])

    @rx.var
    def failed_count(self) -> int:
        return len([p for p in self.payments if p["status"] == "Failed"])