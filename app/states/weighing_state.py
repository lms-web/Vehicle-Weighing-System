import reflex as rx
from app.models import (
    Vehicle,
    Customer,
    MaterialType,
    WeightRecord,
    WeighingTransaction,
    Driver,
    User,
    Role,
    Payment,
    Receipt,
    PricingRule,
    AccountingEntry,
)
import datetime
import random
from typing import Optional
import asyncio


class WeighingState(rx.State):
    vehicles: list[dict] = []
    customers: list[dict] = []
    material_types: list[MaterialType] = []
    transactions: list[WeighingTransaction] = []
    drivers: list[dict] = []
    users: list[User] = []
    roles: list[Role] = []
    payments: list[Payment] = []
    receipts: list[Receipt] = []
    pricing_rules: list[PricingRule] = []
    accounting_entries: list[AccountingEntry] = []
    maintenance_logs: list[dict] = []
    active_page: str = "Dashboard"
    show_vehicle_modal: bool = False
    show_transaction_modal: bool = False
    search_query: str = ""
    filter_type: str = "ALL"
    is_loading: bool = True
    current_weight: float = 0.0
    is_simulating: bool = False
    weight_before: float = 0.0
    weight_after: float = 0.0
    net_weight: float = 0.0
    current_ticket_number: str = ""
    selected_vehicle_id: Optional[int] = None
    selected_customer_id: Optional[str] = None
    selected_material_id: Optional[str] = None
    transaction_type: str = "IN"
    selected_vehicle_detail: Optional[Vehicle] = None
    vehicle_history: list[WeighingTransaction] = []
    transaction_detail: Optional[WeighingTransaction] = None
    weighing_step: str = "start"
    amount_due: float = 0.0
    show_payment_modal: bool = False
    transaction_weight_record: Optional[WeightRecord] = None
    current_page: int = 1
    items_per_page: int = 10
    vehicles_current_page: int = 1
    vehicles_items_per_page: int = 10
    weighing_stage: str = "start"
    vehicle_filter_type: str = "ALL"
    vehicle_filter_status: str = "ALL"
    vehicle_filter_driver: str = "ALL"
    vehicle_search_query: str = ""

    def _create_mock_data(self):
        self.vehicles = [
            {
                "id": 1,
                "license_plate": "ABC-123",
                "vehicle_type": "Truck",
                "make": "Volvo",
                "model": "VNL",
                "color": "Blue",
                "status": "Active",
                "driver_id": 1,
            },
            {
                "id": 2,
                "license_plate": "XYZ-789",
                "vehicle_type": "Van",
                "make": "Ford",
                "model": "Transit",
                "color": "White",
                "status": "Under Maintenance",
                "driver_id": None,
            },
        ]
        self.customers = [
            {
                "id": 1,
                "customer_id": "C001",
                "customer_name": "BuildCo",
                "contact_info": "555-1234",
                "company": "BuildCo Inc.",
                "billing_address": "123 Industrial Way",
                "credit_limit": 200000.0,
            },
            {
                "id": 2,
                "customer_id": "C002",
                "customer_name": "AgriCorp",
                "contact_info": "555-5678",
                "company": "AgriCorp Ltd.",
                "billing_address": "456 Farm Lane",
                "credit_limit": 150000.0,
            },
        ]
        self.material_types = [
            {
                "id": 1,
                "material_code": "SAND",
                "material_name": "Sand",
                "category": "Aggregate",
            },
            {
                "id": 2,
                "material_code": "GRAVEL",
                "material_name": "Gravel",
                "category": "Aggregate",
            },
        ]
        self.transactions = [
            {
                "id": 101,
                "ticket_number": "T20240722-001",
                "transaction_type": "IN",
                "timestamp": datetime.datetime.now() - datetime.timedelta(days=1),
                "vehicle_id": 1,
                "customer_id": 1,
                "material_type_id": 1,
            },
            {
                "id": 102,
                "ticket_number": "T20240722-002",
                "transaction_type": "OUT",
                "timestamp": datetime.datetime.now() - datetime.timedelta(hours=5),
                "vehicle_id": 2,
                "customer_id": 2,
                "material_type_id": 2,
            },
        ]
        self.drivers = [
            {
                "id": 1,
                "name": "John Doe",
                "license_number": "DL12345",
                "phone": "+254712345678",
                "id_number": "12345678",
                "photo": "/placeholder.svg",
                "associated_vehicle_ids": [1],
            }
        ]
        self.roles = [
            {"role_name": "Admin", "permissions_list": ["*"]},
            {
                "role_name": "Operator",
                "permissions_list": ["weighing", "register_vehicle"],
            },
        ]
        self.users = [
            {
                "id": 1,
                "username": "admin",
                "email": "admin@weighbridge.com",
                "role": "Admin",
                "password_hash": "hashed_password_admin",
                "is_active": True,
            },
            {
                "id": 2,
                "username": "operator1",
                "email": "op1@weighbridge.com",
                "role": "Operator",
                "password_hash": "hashed_password_op1",
                "is_active": True,
            },
        ]
        self.pricing_rules = [
            {
                "id": 1,
                "material_type_id": 1,
                "price_per_kg": 0.5,
                "vehicle_type": None,
                "effective_date": datetime.date.today() - datetime.timedelta(days=30),
                "is_active": True,
            },
            {
                "id": 2,
                "material_type_id": 2,
                "price_per_kg": 0.75,
                "vehicle_type": "Truck",
                "effective_date": datetime.date.today() - datetime.timedelta(days=30),
                "is_active": True,
            },
        ]
        self.maintenance_logs = [
            {
                "id": 1,
                "vehicle_id": 1,
                "service_date": "2024-06-25",
                "service_type": "Oil Change",
                "notes": "Replaced oil and filter.",
                "cost": 5000.0,
                "next_service_due": "2024-12-25",
            },
            {
                "id": 2,
                "vehicle_id": 1,
                "service_date": "2024-07-15",
                "service_type": "Tire Rotation",
                "notes": "Rotated tires, checked pressure.",
                "cost": 2500.0,
                "next_service_due": "2025-01-15",
            },
            {
                "id": 3,
                "vehicle_id": 2,
                "service_date": "2024-07-01",
                "service_type": "Brake Inspection",
                "notes": "Inspected brake pads and fluid.",
                "cost": 3000.0,
                "next_service_due": None,
            },
        ]

    @rx.event
    def load_all_data(self):
        self.is_loading = True
        self._create_mock_data()
        self.filter_transactions()
        self.calculate_statistics()
        self.is_loading = False
        if not self.is_simulating:
            return WeighingState.start_weight_simulation

    @rx.event(background=True)
    async def start_weight_simulation(self):
        async with self:
            self.is_simulating = True
        while True:
            async with self:
                if not self.is_simulating:
                    break
                self.current_weight = round(random.uniform(5000, 5200), 2)
            await asyncio.sleep(1)

    @rx.var
    def today_transactions(self) -> int:
        today = datetime.date.today()
        return len([t for t in self.transactions if t["timestamp"].date() == today])

    @rx.var
    def total_vehicles(self) -> int:
        return len(self.vehicles)

    @rx.var
    def avg_net_weight(self) -> float:
        return 12550.5

    @rx.var
    def active_weighings(self) -> int:
        return 1

    @rx.event
    def calculate_statistics(self):
        pass

    @rx.var
    def filtered_transactions(self) -> list[WeighingTransaction]:
        if not self.vehicles:
            return []
        return [
            t
            for t in self.transactions
            if (
                self.search_query.lower()
                in self.vehicle_plates.get(t["vehicle_id"], "").lower()
                or self.search_query == ""
            )
            and (self.filter_type == "ALL" or t["transaction_type"] == self.filter_type)
        ]

    @rx.var
    def paginated_transactions(self) -> list[WeighingTransaction]:
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.filtered_transactions[start:end]

    @rx.var
    def total_pages(self) -> int:
        return -(-len(self.filtered_transactions) // self.items_per_page)

    @rx.event
    def filter_transactions(self):
        self.current_page = 1

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    def start_weighing(self):
        self.weight_before = self.current_weight
        self.current_ticket_number = f"T{datetime.datetime.now().strftime('%Y%m%d')}-{len(self.transactions) + 1:03d}"
        self.weighing_stage = "tare_captured"

    @rx.event
    def complete_weighing(self):
        self.weight_after = self.current_weight
        self.net_weight = abs(self.weight_after - self.weight_before)
        self.weighing_stage = "gross_captured"
        self._calculate_amount_due()
        self.show_payment_modal = True

    def _calculate_amount_due(self):
        if self.selected_material_id:
            rule = next(
                (
                    r
                    for r in self.pricing_rules
                    if r["material_type_id"] == int(self.selected_material_id)
                ),
                None,
            )
            if rule:
                self.amount_due = self.net_weight * rule["price_per_kg"]

    @rx.event
    def process_payment_and_complete(self):
        """This will be triggered after payment is confirmed"""
        new_transaction = {
            "id": len(self.transactions) + 103,
            "ticket_number": self.current_ticket_number,
            "transaction_type": self.transaction_type,
            "timestamp": datetime.datetime.now(),
            "vehicle_id": int(self.selected_vehicle_id)
            if self.selected_vehicle_id
            else None,
            "customer_id": int(self.selected_customer_id)
            if self.selected_customer_id
            else None,
            "material_type_id": int(self.selected_material_id)
            if self.selected_material_id
            else None,
        }
        self.transactions.insert(0, new_transaction)
        self.filter_transactions()
        self.calculate_statistics()
        self.show_payment_modal = False
        return WeighingState.show_receipt(new_transaction["id"])

    @rx.event
    async def show_receipt(self, transaction_id: int):
        from app.states.receipt_state import ReceiptState

        receipt_state = await self.get_state(ReceiptState)
        receipt_state.transaction_id = transaction_id
        receipt_state.amount_paid = self.amount_due
        receipt_state.payment_method = "Cash"
        self.reset_weighing_form()
        return receipt_state.generate_receipt

    @rx.event
    def set_selected_vehicle_id(self, vehicle_id: str):
        self.selected_vehicle_id = vehicle_id

    @rx.event
    def set_selected_customer_id(self, customer_id: str):
        self.selected_customer_id = customer_id

    @rx.event
    def set_selected_material_id(self, material_id: str):
        self.selected_material_id = material_id

    @rx.event
    def close_payment_modal(self):
        self.show_payment_modal = False

    @rx.event
    def reset_weighing_form(self):
        self.weight_before = 0.0
        self.weight_after = 0.0
        self.net_weight = 0.0
        self.current_ticket_number = ""
        self.selected_vehicle_id = None
        self.selected_customer_id = None
        self.selected_material_id = None
        self.weighing_stage = "start"
        self.amount_due = 0.0

    @rx.event
    def view_vehicle_details(self, vehicle_id: int):
        self.selected_vehicle_detail = next(
            (v for v in self.vehicles if v["id"] == vehicle_id), None
        )
        self.vehicle_history = [
            t for t in self.transactions if t["vehicle_id"] == vehicle_id
        ]
        self.active_page = "Vehicles"

    @rx.var
    def filtered_vehicles(self) -> list[Vehicle]:
        query = self.vehicle_search_query.lower()
        return [
            v
            for v in self.vehicles
            if (
                self.vehicle_filter_status == "ALL"
                or v["status"] == self.vehicle_filter_status
            )
            and (
                self.vehicle_filter_type == "ALL"
                or v["vehicle_type"] == self.vehicle_filter_type
            )
            and (
                self.vehicle_filter_driver == "ALL"
                or str(v.get("driver_id")) == self.vehicle_filter_driver
            )
            and (
                query == ""
                or query in v["license_plate"].lower()
                or query in v["make"].lower()
            )
        ]

    @rx.var
    def paginated_vehicles(self) -> list[Vehicle]:
        start = (self.vehicles_current_page - 1) * self.vehicles_items_per_page
        end = start + self.vehicles_items_per_page
        return self.filtered_vehicles[start:end]

    @rx.var
    def total_vehicle_pages(self) -> int:
        return (
            -(-len(self.filtered_vehicles) // self.vehicles_items_per_page)
            if self.filtered_vehicles
            else 1
        )

    @rx.event
    def next_vehicle_page(self):
        if self.vehicles_current_page < self.total_vehicle_pages:
            self.vehicles_current_page += 1

    @rx.event
    def prev_vehicle_page(self):
        if self.vehicles_current_page > 1:
            self.vehicles_current_page -= 1

    @rx.event
    def view_transaction_detail(self, transaction_id: int):
        self.transaction_detail = next(
            (t for t in self.transactions if t["id"] == transaction_id), None
        )
        self.transaction_weight_record = {
            "tare_weight": 5100.5,
            "gross_weight": 18230.0,
            "net_weight": 13129.5,
            "weight_before": 5100.5,
            "weight_after": 18230.0,
            "unit_of_measure": "kg",
        }
        self.show_transaction_modal = True

    @rx.event
    def close_transaction_modal(self):
        self.show_transaction_modal = False
        self.transaction_detail = None
        self.transaction_weight_record = None

    @rx.var
    def vehicle_plates(self) -> dict[str, str]:
        return {str(v["id"]): v["license_plate"] for v in self.vehicles}

    @rx.event
    def get_vehicle_plate(self, vehicle_id: int) -> str:
        vehicle = next((v for v in self.vehicles if v["id"] == vehicle_id), None)
        return vehicle["license_plate"] if vehicle else "N/A"

    @rx.event
    def get_customer_name(self, customer_id: int) -> str:
        customer = next((c for c in self.customers if c["id"] == customer_id), None)
        return customer["customer_name"] if customer else "N/A"

    @rx.event
    def get_material_name(self, material_id: int) -> str:
        material = next(
            (m for m in self.material_types if m["id"] == material_id), None
        )
        return material["material_name"] if material else "N/A"

    @rx.event
    def vehicle_transaction_count(self, vehicle_id: int) -> int:
        return len([t for t in self.transactions if t.get("vehicle_id") == vehicle_id])

    @rx.event
    def vehicle_total_weight(self, vehicle_id: int) -> float:
        return sum(
            (12550.5 for t in self.transactions if t.get("vehicle_id") == vehicle_id)
        )

    @rx.event
    def vehicle_revenue(self, vehicle_id: int) -> float:
        return sum(
            (16411.88 for t in self.transactions if t.get("vehicle_id") == vehicle_id)
        )

    @rx.var
    def selected_vehicle_maintenance_logs(self) -> list[dict]:
        if not self.selected_vehicle_detail:
            return []
        return [
            log
            for log in self.maintenance_logs
            if log.get("vehicle_id") == self.selected_vehicle_detail["id"]
        ]

    @rx.var
    def selected_vehicle_transaction_count(self) -> int:
        if not self.selected_vehicle_detail:
            return 0
        return len(
            [
                t
                for t in self.transactions
                if t.get("vehicle_id") == self.selected_vehicle_detail["id"]
            ]
        )

    @rx.var
    def selected_vehicle_total_weight(self) -> float:
        if not self.selected_vehicle_detail:
            return 0.0
        return sum(
            (
                12550.5
                for t in self.transactions
                if t.get("vehicle_id") == self.selected_vehicle_detail["id"]
            )
        )

    @rx.var
    def selected_vehicle_revenue(self) -> float:
        if not self.selected_vehicle_detail:
            return 0.0
        return sum(
            (
                16411.88
                for t in self.transactions
                if t.get("vehicle_id") == self.selected_vehicle_detail["id"]
            )
        )