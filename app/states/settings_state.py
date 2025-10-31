import reflex as rx
from typing import TypedDict, Literal


class PricingRule(TypedDict):
    id: int
    material_name: str
    price_per_kg: float
    vehicle_type: str
    effective_date: str
    is_active: bool


class User(TypedDict):
    id: int
    username: str
    email: str
    role: str
    is_active: bool


class SettingsState(rx.State):
    """Manages application settings, including pricing, users, and system configuration."""

    active_tab: Literal["Pricing", "Users", "System", "Camera", "Notifications"] = (
        "Pricing"
    )
    pricing_rules: list[PricingRule] = [
        {
            "id": 1,
            "material_name": "Sand",
            "price_per_kg": 0.5,
            "vehicle_type": "All",
            "effective_date": "2024-01-01",
            "is_active": True,
        },
        {
            "id": 2,
            "material_name": "Gravel",
            "price_per_kg": 0.75,
            "vehicle_type": "Truck",
            "effective_date": "2024-01-01",
            "is_active": True,
        },
        {
            "id": 3,
            "material_name": "Gravel",
            "price_per_kg": 0.85,
            "vehicle_type": "Heavy-Duty Truck",
            "effective_date": "2024-06-01",
            "is_active": False,
        },
    ]
    users: list[User] = [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@weighbridge.com",
            "role": "Admin",
            "is_active": True,
        },
        {
            "id": 2,
            "username": "operator1",
            "email": "op1@weighbridge.com",
            "role": "Operator",
            "is_active": True,
        },
        {
            "id": 3,
            "username": "accountant",
            "email": "acc@weighbridge.com",
            "role": "Accountant",
            "is_active": False,
        },
    ]