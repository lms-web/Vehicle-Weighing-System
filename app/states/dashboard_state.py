import reflex as rx
from typing import TypedDict


class NavItem(TypedDict):
    label: str
    icon: str
    href: str


class DashboardState(rx.State):
    """State for the dashboard and sidebar."""

    nav_items: list[NavItem] = [
        {"label": "Dashboard", "icon": "layout-dashboard", "href": "/"},
        {"label": "Finance", "icon": "landmark", "href": "#"},
        {"label": "Payments", "icon": "credit-card", "href": "#"},
        {"label": "Camera", "icon": "camera", "href": "#"},
        {"label": "Transactions", "icon": "receipt-text", "href": "#"},
        {"label": "Vehicles", "icon": "truck", "href": "#"},
        {"label": "Drivers", "icon": "user", "href": "#"},
        {"label": "Customers", "icon": "users", "href": "#"},
        {"label": "Reports", "icon": "bar-chart-3", "href": "#"},
        {"label": "Settings", "icon": "settings", "href": "#"},
    ]