import reflex as rx
import datetime
from typing import TypedDict, Optional


class ReceiptData(TypedDict):
    id: int
    receipt_number: str
    transaction_id: int
    issued_date: str
    amount_paid: float
    payment_method: str
    mpesa_code: Optional[str]


class ReceiptState(rx.State):
    """Manages receipt generation and viewing."""

    receipts: list[ReceiptData] = []
    current_receipt: Optional[ReceiptData] = None
    show_receipt_modal: bool = False
    transaction_id: Optional[int] = None
    amount_paid: float = 0.0
    payment_method: str = ""
    mpesa_code: Optional[str] = None

    @rx.event
    def generate_receipt(self):
        if not self.transaction_id:
            return
        receipt_number = f"RCT-{datetime.datetime.now().strftime('%Y%m%d')}-{len(self.receipts) + 1:03d}"
        new_receipt = {
            "id": len(self.receipts) + 1,
            "receipt_number": receipt_number,
            "transaction_id": self.transaction_id,
            "issued_date": datetime.datetime.now().isoformat(),
            "amount_paid": self.amount_paid,
            "payment_method": self.payment_method,
            "mpesa_code": self.mpesa_code,
        }
        self.receipts.append(new_receipt)
        self.current_receipt = new_receipt
        self.show_receipt_modal = True
        self._reset_fields()

    def _reset_fields(self):
        self.transaction_id = None
        self.amount_paid = 0.0
        self.payment_method = ""
        self.mpesa_code = None

    @rx.event
    def view_receipt(self, receipt_id: int):
        receipt = next((r for r in self.receipts if r["id"] == receipt_id), None)
        if receipt:
            self.current_receipt = receipt
            self.show_receipt_modal = True

    @rx.event
    def close_receipt_modal(self):
        self.show_receipt_modal = False
        self.current_receipt = None