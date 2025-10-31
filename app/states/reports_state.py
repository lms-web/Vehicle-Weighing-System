import reflex as rx
from typing import Literal, TypedDict, Optional
import datetime
import random
from app.models import (
    WeighingTransaction,
    Vehicle,
    Customer,
    MaterialType,
    Driver,
    PricingRule,
    Payment,
)


class DailySummary(TypedDict):
    date: str
    total_transactions: int
    total_revenue: float
    total_weight: float


class VehicleReportData(TypedDict):
    vehicle_id: int
    license_plate: str
    transaction_count: int
    total_weight: float
    total_revenue: float


class CustomerReportData(TypedDict):
    customer_id: int
    customer_name: str
    transaction_count: int
    total_spent: float


class MaterialReportData(TypedDict):
    material_id: int
    material_name: str
    weight_in: float
    weight_out: float
    net_weight: float


class DriverReportData(TypedDict):
    driver_id: int
    driver_name: str
    transaction_count: int
    total_weight_handled: float


class ReportsState(rx.State):
    """State for managing the reports page."""

    report_type: Literal[
        "Financial", "Vehicles", "Customers", "Materials", "Drivers"
    ] = "Financial"
    transactions: list[WeighingTransaction] = []
    vehicles: list[Vehicle] = []
    customers: list[Customer] = []
    material_types: list[MaterialType] = []
    drivers: list[Driver] = []
    pricing_rules: list[PricingRule] = []
    payments: list[Payment] = []
    start_date: str = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    end_date: str = datetime.date.today().isoformat()

    @rx.event
    async def load_report_data(self):
        from app.states.weighing_state import WeighingState
        from app.states.finance_state import FinanceState

        weighing_state = await self.get_state(WeighingState)
        finance_state = await self.get_state(FinanceState)
        self.transactions = weighing_state.transactions
        self.vehicles = weighing_state.vehicles
        self.customers = weighing_state.customers
        self.material_types = weighing_state.material_types
        self.drivers = weighing_state.drivers
        self.pricing_rules = weighing_state.pricing_rules
        self.payments = weighing_state.payments

    @rx.var
    def filtered_transactions_by_date(self) -> list[WeighingTransaction]:
        start = datetime.date.fromisoformat(self.start_date)
        end = datetime.date.fromisoformat(self.end_date)
        return [t for t in self.transactions if start <= t["timestamp"].date() <= end]

    @rx.var
    def total_revenue(self) -> float:
        return sum(
            (
                p["amount"]
                for p in self.payments
                if p.get("payment_status") == "Completed"
            )
        )

    @rx.var
    def daily_summary_data(self) -> list[DailySummary]:
        return [
            {
                "date": (
                    datetime.date.today() - datetime.timedelta(days=i)
                ).isoformat(),
                "total_transactions": random.randint(10, 50),
                "total_revenue": random.uniform(10000, 50000),
                "total_weight": random.uniform(100000, 500000),
            }
            for i in range(30)
        ][::-1]

    @rx.var
    def vehicle_report(self) -> list[VehicleReportData]:
        return [
            {
                "vehicle_id": v["id"],
                "license_plate": v["license_plate"],
                "transaction_count": random.randint(5, 20),
                "total_weight": random.uniform(50000, 150000),
                "total_revenue": random.uniform(25000, 75000),
            }
            for v in self.vehicles
        ]

    @rx.var
    def customer_report(self) -> list[CustomerReportData]:
        return [
            {
                "customer_id": c["id"],
                "customer_name": c["customer_name"],
                "transaction_count": random.randint(2, 10),
                "total_spent": random.uniform(10000, 100000),
            }
            for c in self.customers
        ]

    @rx.event
    def set_report_type(self, report_type: str):
        self.report_type = report_type