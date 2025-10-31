import reflex as rx
from typing import Optional, TypedDict


class Customer(TypedDict):
    id: int
    customer_id: str
    customer_name: str
    contact_info: Optional[str]
    company: Optional[str]
    billing_address: Optional[str]
    credit_limit: float


class CustomerManagementState(rx.State):
    """Manages customer registration and data."""

    customers: list[Customer] = []
    show_registration_modal: bool = False
    show_detail_modal: bool = False
    selected_customer_detail: Optional[Customer] = None
    outstanding_balance: float = 0.0
    customer_search_query: str = ""
    customers_page_current: int = 1
    customers_items_per_page: int = 10

    @rx.event
    def load_customers(self):
        if not self.customers:
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

    @rx.event
    def toggle_registration_modal(self):
        self.show_registration_modal = not self.show_registration_modal

    @rx.event
    def register_customer(self, form_data: dict):
        new_id = len(self.customers) + 1
        new_customer = {
            "id": new_id,
            "customer_id": f"C{new_id:03d}",
            "customer_name": form_data["customer_name"],
            "company": form_data["company"],
            "contact_info": form_data["contact_info"],
            "billing_address": form_data["billing_address"],
            "credit_limit": float(form_data.get("credit_limit", 0.0)),
        }
        self.customers.append(new_customer)
        self.show_registration_modal = False

    @rx.event
    def view_customer_details(self, customer_id: int):
        self.selected_customer_detail = next(
            (c for c in self.customers if c["id"] == customer_id), None
        )
        self.outstanding_balance = 55000.75
        self.show_detail_modal = True

    @rx.event
    def close_detail_modal(self):
        self.show_detail_modal = False
        self.selected_customer_detail = None

    @rx.var
    def filtered_customers(self) -> list[Customer]:
        query = self.customer_search_query.lower()
        if not query:
            return self.customers
        return [
            c
            for c in self.customers
            if query in c["customer_name"].lower()
            or query in c["company"].lower()
            or query in c["contact_info"].lower()
        ]

    @rx.var
    def paginated_customers(self) -> list[Customer]:
        start = (self.customers_page_current - 1) * self.customers_items_per_page
        end = start + self.customers_items_per_page
        return self.filtered_customers[start:end]

    @rx.var
    def total_customer_pages(self) -> int:
        return -(-len(self.filtered_customers) // self.customers_items_per_page)

    @rx.event
    def next_customer_page(self):
        if self.customers_page_current < self.total_customer_pages:
            self.customers_page_current += 1

    @rx.event
    def prev_customer_page(self):
        if self.customers_page_current > 1:
            self.customers_page_current -= 1