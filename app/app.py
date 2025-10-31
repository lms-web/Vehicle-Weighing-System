import reflex as rx
from app.components.dashboard import dashboard_page
from app.states.weighing_state import WeighingState


def index() -> rx.Component:
    return dashboard_page()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.states.finance_state import FinanceState
from app.states.camera_state import CameraState
from app.states.vehicle_registration_state import VehicleRegistrationState
from app.states.driver_management_state import DriverManagementState
from app.states.customer_management_state import CustomerManagementState
from app.states.settings_state import SettingsState
from app.states.reports_state import ReportsState
from app.states.transactions_state import TransactionsState

app.add_page(
    index,
    route="/",
    on_load=[
        WeighingState.load_all_data,
        FinanceState.load_finance_data,
        DriverManagementState.load_drivers,
        CustomerManagementState.load_customers,
    ],
)