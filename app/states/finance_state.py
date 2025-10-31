import reflex as rx
import datetime
from typing import TypedDict


class RevenueData(TypedDict):
    date: str
    revenue: float


class AccountingEntry(TypedDict):
    id: int
    date: str
    description: str
    debit: float
    credit: float
    category: str


class FinanceState(rx.State):
    """State for the finance dashboard."""

    daily_revenue: list[RevenueData] = []
    weekly_revenue: list[RevenueData] = []
    monthly_revenue: list[RevenueData] = []
    accounting_entries: list[AccountingEntry] = []
    total_revenue: float = 0.0
    total_expenses: float = 0.0
    net_profit: float = 0.0
    filter_category: str = "ALL"

    @rx.event
    def load_finance_data(self):
        self.daily_revenue = [
            {
                "date": (datetime.date.today() - datetime.timedelta(days=i)).strftime(
                    "%b %d"
                ),
                "revenue": 1500 - i * 100,
            }
            for i in range(7)
        ][::-1]
        self.weekly_revenue = [
            {"date": f"Week {i}", "revenue": 10000 - i * 500} for i in range(4)
        ][::-1]
        self.monthly_revenue = [
            {"date": f"Month {i}", "revenue": 40000 - i * 2000} for i in range(3)
        ][::-1]
        self.accounting_entries = [
            {
                "id": 1,
                "date": "2024-07-22",
                "description": "Sale from T20240722-001",
                "debit": 0,
                "credit": 1250.0,
                "category": "Revenue",
            },
            {
                "id": 2,
                "date": "2024-07-22",
                "description": "Fuel Expense",
                "debit": 100.0,
                "credit": 0,
                "category": "Expense",
            },
            {
                "id": 3,
                "date": "2024-07-21",
                "description": "Sale from T20240721-050",
                "debit": 0,
                "credit": 800.0,
                "category": "Revenue",
            },
        ]
        self.total_revenue = sum((e["credit"] for e in self.accounting_entries))
        self.total_expenses = sum((e["debit"] for e in self.accounting_entries))
        self.net_profit = self.total_revenue - self.total_expenses

    @rx.var
    def filtered_accounting_entries(self) -> list[AccountingEntry]:
        if self.filter_category == "ALL":
            return self.accounting_entries
        return [
            entry
            for entry in self.accounting_entries
            if entry["category"] == self.filter_category
        ]