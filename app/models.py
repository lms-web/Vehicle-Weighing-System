import reflex as rx
from typing import Optional, TypedDict
import datetime


class Vehicle(TypedDict):
    id: Optional[int]
    license_plate: str
    vehicle_type: str
    make: str
    model: str
    color: str
    status: str


class Customer(TypedDict):
    id: Optional[int]
    customer_id: str
    customer_name: str
    contact_info: Optional[str]
    company: Optional[str]
    billing_address: Optional[str]
    credit_limit: Optional[float]


class MaterialType(TypedDict):
    id: Optional[int]
    material_code: str
    material_name: str
    category: str


class WeightRecord(TypedDict):
    id: Optional[int]
    tare_weight: Optional[float]
    gross_weight: Optional[float]
    net_weight: Optional[float]
    weight_before: float
    weight_after: float
    unit_of_measure: str
    weighing_transaction_id: Optional[int]


class WeighingTransaction(TypedDict):
    id: Optional[int]
    ticket_number: str
    transaction_type: str
    timestamp: datetime.datetime
    vehicle_id: Optional[int]
    customer_id: Optional[int]
    material_type_id: Optional[int]


class Driver(TypedDict):
    id: Optional[int]
    name: str
    license_number: str
    phone: str
    id_number: str
    photo: Optional[str]
    associated_vehicle_ids: list[int]


class Role(TypedDict):
    role_name: str
    permissions_list: list[str]


class User(TypedDict):
    id: Optional[int]
    username: str
    email: str
    role: str
    password_hash: str
    is_active: bool


class Payment(TypedDict):
    id: Optional[int]
    weighing_transaction_id: int
    amount: float
    payment_method: str
    mpesa_code: Optional[str]
    payment_status: str
    timestamp: datetime.datetime


class Receipt(TypedDict):
    id: Optional[int]
    weighing_transaction_id: int
    receipt_number: str
    issued_date: datetime.datetime
    amount_paid: float
    payment_method: str


class PricingRule(TypedDict):
    id: Optional[int]
    material_type_id: int
    price_per_kg: float
    vehicle_type: Optional[str]
    effective_date: datetime.date
    is_active: bool


class AccountingEntry(TypedDict):
    id: Optional[int]
    transaction_date: datetime.date
    debit_amount: float
    credit_amount: float
    category: str
    description: str