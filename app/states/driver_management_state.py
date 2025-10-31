import reflex as rx
from typing import Optional, TypedDict


class Driver(TypedDict):
    id: int
    name: str
    license_number: str
    phone: str
    id_number: str
    photo: Optional[str]
    associated_vehicle_ids: list[int]


class DriverManagementState(rx.State):
    """Manages driver registration and data."""

    drivers: list[Driver] = []
    show_registration_modal: bool = False
    show_detail_modal: bool = False
    selected_driver_detail: Optional[Driver] = None
    driver_search_query: str = ""
    drivers_page_current: int = 1
    drivers_items_per_page: int = 10

    @rx.event
    def load_drivers(self):
        if not self.drivers:
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

    @rx.event
    def toggle_registration_modal(self):
        self.show_registration_modal = not self.show_registration_modal

    @rx.event
    def register_driver(self, form_data: dict):
        new_id = len(self.drivers) + 1
        vehicle_ids = form_data.get("vehicle_ids", [])
        if not isinstance(vehicle_ids, list):
            vehicle_ids = [vehicle_ids]
        new_driver = {
            "id": new_id,
            "name": form_data["name"],
            "license_number": form_data["license_number"],
            "phone": form_data["phone"],
            "id_number": form_data["id_number"],
            "photo": "/placeholder.svg",
            "associated_vehicle_ids": [int(vid) for vid in vehicle_ids if vid],
        }
        self.drivers.append(new_driver)
        self.show_registration_modal = False

    @rx.event
    def view_driver_details(self, driver_id: int):
        self.selected_driver_detail = next(
            (d for d in self.drivers if d["id"] == driver_id), None
        )
        self.show_detail_modal = True

    @rx.event
    def close_detail_modal(self):
        self.show_detail_modal = False
        self.selected_driver_detail = None

    @rx.var
    def filtered_drivers(self) -> list[Driver]:
        query = self.driver_search_query.lower()
        if not query:
            return self.drivers
        return [
            d
            for d in self.drivers
            if query in d["name"].lower()
            or query in d["license_number"].lower()
            or query in d["phone"].lower()
        ]

    @rx.var
    def paginated_drivers(self) -> list[Driver]:
        start = (self.drivers_page_current - 1) * self.drivers_items_per_page
        end = start + self.drivers_items_per_page
        return self.filtered_drivers[start:end]

    @rx.var
    def total_driver_pages(self) -> int:
        return -(-len(self.filtered_drivers) // self.drivers_items_per_page)

    @rx.event
    def next_driver_page(self):
        if self.drivers_page_current < self.total_driver_pages:
            self.drivers_page_current += 1

    @rx.event
    def prev_driver_page(self):
        if self.drivers_page_current > 1:
            self.drivers_page_current -= 1