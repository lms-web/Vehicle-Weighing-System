import reflex as rx
from typing import TypedDict, Optional, Literal
import datetime
from app.models import WeighingTransaction, WeightRecord


class TransactionDetail(TypedDict):
    transaction: WeighingTransaction
    weight_record: WeightRecord
    vehicle_plate: str
    customer_name: str
    material_name: str


PaymentStatus = Literal["ALL", "Pending", "Completed", "Paid", "Overdue"]


class TransactionsState(rx.State):
    """Manages the transactions page with advanced filtering and details."""

    all_transactions: list[WeighingTransaction] = []
    search_query: str = ""
    filter_date_start: str = (
        datetime.date.today() - datetime.timedelta(days=30)
    ).isoformat()
    filter_date_end: str = datetime.date.today().isoformat()
    filter_transaction_type: str = "ALL"
    filter_payment_status: PaymentStatus = "ALL"
    selected_transaction_detail: Optional[TransactionDetail] = None
    show_detail_modal: bool = False
    current_page: int = 1
    items_per_page: int = 15

    @rx.event
    async def load_transactions(self):
        from app.states.weighing_state import WeighingState

        weighing_state = await self.get_state(WeighingState)
        self.all_transactions = weighing_state.transactions

    @rx.var
    def filtered_transactions(self) -> list[WeighingTransaction]:
        start_date = datetime.datetime.fromisoformat(self.filter_date_start).date()
        end_date = datetime.datetime.fromisoformat(self.filter_date_end).date()
        return [
            t
            for t in self.all_transactions
            if start_date <= t["timestamp"].date() <= end_date
            and (
                self.filter_transaction_type == "ALL"
                or t["transaction_type"] == self.filter_transaction_type
            )
            and (
                self.search_query == ""
                or self.search_query.lower() in t["ticket_number"].lower()
            )
        ]

    @rx.var
    def paginated_transactions(self) -> list[WeighingTransaction]:
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_transactions[start:end]

    @rx.var
    def total_pages(self) -> int:
        total_items = len(self.filtered_transactions)
        return -(-total_items // self.items_per_page) if total_items > 0 else 1

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    async def view_transaction_details(self, transaction_id: int):
        from app.states.weighing_state import WeighingState

        weighing_state = await self.get_state(WeighingState)
        transaction = next(
            (t for t in self.all_transactions if t["id"] == transaction_id), None
        )
        if not transaction:
            return
        weight_record = {
            "tare_weight": 5100.5,
            "gross_weight": 18230.0,
            "net_weight": 13129.5,
            "weight_before": 5100.5,
            "weight_after": 18230.0,
            "unit_of_measure": "kg",
            "id": transaction_id,
            "weighing_transaction_id": transaction_id,
        }
        self.selected_transaction_detail = {
            "transaction": transaction,
            "weight_record": weight_record,
            "vehicle_plate": await weighing_state.get_vehicle_plate(
                transaction["vehicle_id"]
            ),
            "customer_name": await weighing_state.get_customer_name(
                transaction["customer_id"]
            ),
            "material_name": await weighing_state.get_material_name(
                transaction["material_type_id"]
            ),
        }
        self.show_detail_modal = True

    @rx.event
    def close_detail_modal(self):
        self.show_detail_modal = False
        self.selected_transaction_detail = None