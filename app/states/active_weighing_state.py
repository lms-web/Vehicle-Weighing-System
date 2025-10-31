import reflex as rx
from typing import Optional
from app.states.weighing_state import WeighingState
from app.states.mpesa_state import MpesaState
from app.states.receipt_state import ReceiptState


class ActiveWeighingState(rx.State):
    """State for the active weighing process, separate from main WeighingState."""

    selected_vehicle_id: Optional[int] = None
    selected_driver_id: Optional[int] = None
    selected_customer_id: Optional[int] = None
    selected_material_id: Optional[int] = None
    transaction_type: str = "IN"
    tare_weight: float = 0.0
    gross_weight: float = 0.0
    net_weight: float = 0.0
    amount_due: float = 0.0
    current_ticket_number: str = ""
    weighing_stage: str = "IDLE"
    show_payment_modal: bool = False
    payment_method: str = "MPESA"
    phone_number: str = ""
    cash_amount_paid: float = 0.0
    change_due: float = 0.0
    is_processing_payment: bool = False
    payment_success: bool = False
    payment_error: str = ""

    @rx.var
    def current_weight(self) -> float:
        return 1234.5

    @rx.event
    async def load_driver_for_vehicle(self, vehicle_id: int):
        self.selected_vehicle_id = vehicle_id
        main_state = await self.get_state(WeighingState)
        vehicle = next((v for v in main_state.vehicles if v["id"] == vehicle_id), None)
        if vehicle and vehicle.get("driver_id"):
            self.selected_driver_id = vehicle["driver_id"]

    @rx.event
    async def capture_tare_weight(self):
        main_state = await self.get_state(WeighingState)
        self.tare_weight = main_state.current_weight
        self.weighing_stage = "TARE_CAPTURED"
        self.current_ticket_number = f"TICKET-{len(main_state.transactions) + 1}"

    @rx.event
    async def capture_gross_weight(self):
        main_state = await self.get_state(WeighingState)
        self.gross_weight = main_state.current_weight
        self.net_weight = abs(self.gross_weight - self.tare_weight)
        await self._calculate_amount()
        self.weighing_stage = "READY_FOR_PAYMENT"

    async def _calculate_amount(self):
        if not self.selected_material_id:
            return
        main_state = await self.get_state(WeighingState)
        rule = next(
            (
                r
                for r in main_state.pricing_rules
                if r["material_type_id"] == self.selected_material_id
            ),
            None,
        )
        if rule:
            self.amount_due = self.net_weight * rule["price_per_kg"]

    @rx.event
    def proceed_to_payment(self):
        self.show_payment_modal = True

    @rx.event
    async def process_payment(self):
        self.is_processing_payment = True
        if self.payment_method == "MPESA":
            mpesa = await self.get_state(MpesaState)
            yield mpesa.initiate_stk_push(self.phone_number, self.amount_due)
            self.payment_success = True
        elif self.payment_method == "Cash":
            if self.cash_amount_paid < self.amount_due:
                self.payment_error = "Cash paid is less than amount due."
                self.is_processing_payment = False
                return
            self.change_due = self.cash_amount_paid - self.amount_due
            self.payment_success = True
        if self.payment_success:
            await self._complete_transaction()
        self.is_processing_payment = False

    async def _complete_transaction(self):
        main_state = await self.get_state(WeighingState)
        new_transaction = {
            "id": len(main_state.transactions) + 1,
            "ticket_number": self.current_ticket_number,
            "transaction_type": self.transaction_type,
            "timestamp": "NOW",
            "vehicle_id": self.selected_vehicle_id,
            "customer_id": self.selected_customer_id,
            "material_type_id": self.selected_material_id,
        }
        main_state.transactions.append(new_transaction)
        receipt_state = await self.get_state(ReceiptState)
        receipt_state.transaction_id = new_transaction["id"]
        receipt_state.amount_paid = self.amount_due
        receipt_state.payment_method = self.payment_method
        yield receipt_state.generate_receipt
        self.show_payment_modal = False
        yield ActiveWeighingState.reset_weighing

    @rx.event
    def reset_weighing(self):
        self.selected_vehicle_id = None
        self.selected_driver_id = None
        self.selected_customer_id = None
        self.selected_material_id = None
        self.transaction_type = "IN"
        self.tare_weight = 0.0
        self.gross_weight = 0.0
        self.net_weight = 0.0
        self.amount_due = 0.0
        self.current_ticket_number = ""
        self.weighing_stage = "IDLE"
        self.show_payment_modal = False
        self.payment_method = "MPESA"
        self.phone_number = ""
        self.cash_amount_paid = 0.0
        self.change_due = 0.0
        self.is_processing_payment = False
        self.payment_success = False
        self.payment_error = ""