import reflex as rx
from app.states.dashboard_state import DashboardState
from app.states.weighing_state import WeighingState


def sidebar_nav_item(item: dict[str, str], active: str) -> rx.Component:
    is_active = item["label"] == active
    return rx.el.a(
        rx.icon(item["icon"], class_name="h-5 w-5"),
        rx.el.span(item["label"]),
        href="#",
        on_click=WeighingState.set_active_page(item["label"]),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-purple-100 px-3 py-2 text-purple-600 transition-all hover:text-purple-600",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
        font_family="Roboto",
    )


def sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("truck", class_name="h-6 w-6 text-purple-600"),
                rx.el.span("WeighBridge", class_name="sr-only"),
                href="#",
                class_name="flex items-center gap-2 text-lg font-semibold",
            ),
            rx.el.nav(
                rx.foreach(
                    DashboardState.nav_items,
                    lambda item: sidebar_nav_item(item, WeighingState.active_page),
                ),
                class_name="grid items-start px-4 text-sm font-medium",
            ),
            class_name="flex-1 overflow-auto py-2",
        ),
        class_name="hidden border-r bg-gray-100/40 md:block w-64",
    )


def stat_card(icon: str, title: str, value: rx.Var, change: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                title, class_name="text-sm font-medium tracking-tight text-gray-500"
            ),
            rx.icon(icon, class_name="h-4 w-4 text-gray-400"),
            class_name="flex flex-row items-center justify-between space-y-0 pb-2",
        ),
        rx.el.div(
            rx.el.span(value, class_name="text-2xl font-bold text-gray-900"),
            rx.el.p(change, class_name="text-xs text-gray-500"),
            class_name="",
        ),
        class_name="rounded-xl border bg-white p-4 shadow-sm",
    )


from app.components.camera_alert_modal import camera_toggle_button


def dashboard_content() -> rx.Component:
    return rx.el.main(
        camera_toggle_button(),
        rx.el.div(
            stat_card(
                "receipt-text",
                "Today's Transactions",
                WeighingState.today_transactions.to_string(),
                "+10% from yesterday",
            ),
            stat_card(
                "truck",
                "Total Vehicles",
                WeighingState.total_vehicles.to_string(),
                "+2 new vehicles",
            ),
            stat_card(
                "scale",
                "Avg. Net Weight",
                f"{WeighingState.avg_net_weight.to_string()} kg",
                "-2% from yesterday",
            ),
            stat_card(
                "activity",
                "Active Weighings",
                WeighingState.active_weighings.to_string(),
                "1 on bridge now",
            ),
            class_name="grid gap-4 md:grid-cols-2 lg:grid-cols-4",
        ),
        rx.el.div(
            active_weighing_interface(),
            transaction_history_table(),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6",
        ),
        class_name="flex flex-col gap-4 p-4 sm:px-6 sm:py-0",
    )


def active_weighing_interface() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Active Weighing", class_name="text-lg font-semibold mb-4 text-gray-800"
        ),
        rx.el.div(
            rx.el.p("Live Weight", class_name="text-sm text-gray-500"),
            rx.el.div(
                rx.el.span(
                    WeighingState.current_weight.to_string(),
                    class_name="text-5xl font-bold text-purple-600",
                ),
                rx.el.span("kg", class_name="text-lg font-medium text-gray-600 ml-2"),
                class_name="flex items-baseline justify-center p-6 bg-gray-50 rounded-lg",
            ),
            class_name="text-center mb-4",
        ),
        rx.match(
            WeighingState.weighing_stage,
            (
                "start",
                rx.el.div(
                    rx.el.div(
                        rx.el.label("Vehicle", class_name="text-sm font-medium"),
                        rx.el.select(
                            rx.el.option("Select Vehicle", value="", disabled=True),
                            rx.foreach(
                                WeighingState.vehicles,
                                lambda v: rx.el.option(
                                    v["license_plate"], value=v["id"]
                                ),
                            ),
                            on_change=WeighingState.set_selected_vehicle_id,
                            value=WeighingState.selected_vehicle_id.to_string(),
                            class_name="w-full p-2 border rounded-lg bg-white text-sm",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Customer", class_name="text-sm font-medium"),
                        rx.el.select(
                            rx.el.option("Select Customer", value="", disabled=True),
                            rx.foreach(
                                WeighingState.customers,
                                lambda c: rx.el.option(
                                    c["customer_name"], value=c["id"]
                                ),
                            ),
                            on_change=WeighingState.set_selected_customer_id,
                            value=WeighingState.selected_customer_id.to_string(),
                            class_name="w-full p-2 border rounded-lg bg-white text-sm",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Material", class_name="text-sm font-medium"),
                        rx.el.select(
                            rx.el.option("Select Material", value="", disabled=True),
                            rx.foreach(
                                WeighingState.material_types,
                                lambda m: rx.el.option(
                                    m["material_name"], value=m["id"]
                                ),
                            ),
                            on_change=WeighingState.set_selected_material_id,
                            value=WeighingState.selected_material_id.to_string(),
                            class_name="w-full p-2 border rounded-lg bg-white text-sm",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.button(
                        "Capture Tare Weight",
                        on_click=WeighingState.start_weighing,
                        class_name="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition mt-4",
                    ),
                ),
            ),
            (
                "tare_captured",
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Tare Weight:", class_name="font-semibold"),
                        rx.el.p(f"{WeighingState.weight_before} kg"),
                        class_name="flex justify-between text-sm p-2 bg-gray-100 rounded-md",
                    ),
                    rx.el.button(
                        "Capture Gross Weight",
                        on_click=WeighingState.complete_weighing,
                        class_name="w-full bg-green-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-green-700 transition mt-4",
                    ),
                    rx.el.button(
                        "Cancel",
                        on_click=WeighingState.reset_weighing_form,
                        class_name="w-full bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition mt-2",
                    ),
                ),
            ),
            (
                "gross_captured",
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Tare Weight:", class_name="font-semibold"),
                        rx.el.p(f"{WeighingState.weight_before} kg"),
                        class_name="flex justify-between text-sm p-2 bg-gray-100 rounded-md mb-2",
                    ),
                    rx.el.div(
                        rx.el.p("Gross Weight:", class_name="font-semibold"),
                        rx.el.p(f"{WeighingState.weight_after} kg"),
                        class_name="flex justify-between text-sm p-2 bg-gray-100 rounded-md mb-2",
                    ),
                    rx.el.div(
                        rx.el.p("Net Weight:", class_name="font-bold"),
                        rx.el.p(
                            f"{WeighingState.net_weight} kg", class_name="font-bold"
                        ),
                        class_name="flex justify-between text-sm p-2 bg-blue-50 rounded-md mb-2",
                    ),
                    rx.el.div(
                        rx.el.p("Amount Due:", class_name="font-bold"),
                        rx.el.p(
                            f"Ksh {WeighingState.amount_due.to_string()}",
                            class_name="font-bold text-green-600",
                        ),
                        class_name="flex justify-between text-lg p-3 bg-green-50 rounded-md mb-4",
                    ),
                    rx.el.button(
                        "Proceed to Payment",
                        on_click=WeighingState.process_payment_and_complete,
                        class_name="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition mt-4",
                    ),
                ),
            ),
        ),
        class_name="md:col-span-1 bg-white p-6 rounded-xl border shadow-sm",
    )


def transaction_history_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Transaction History", class_name="text-lg font-semibold mb-4 text-gray-800"
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Search by plate...",
                on_change=WeighingState.set_search_query,
                class_name="w-full md:w-1/3 p-2 border rounded-lg",
            ),
            rx.el.select(
                rx.el.option("All Types", value="ALL"),
                rx.el.option("IN", value="IN"),
                rx.el.option("OUT", value="OUT"),
                on_change=WeighingState.set_filter_type,
                default_value="ALL",
                class_name="p-2 border rounded-lg bg-white",
            ),
            class_name="flex gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Ticket",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Plate",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Type",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Timestamp",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        WeighingState.paginated_transactions,
                        lambda transaction: rx.el.tr(
                            rx.el.td(
                                transaction["ticket_number"], class_name="p-3 text-sm"
                            ),
                            rx.el.td(
                                WeighingState.vehicle_plates[
                                    transaction["vehicle_id"].to_string()
                                ],
                                class_name="p-3 text-sm font-medium text-gray-800",
                            ),
                            rx.el.td(
                                transaction["transaction_type"],
                                class_name="p-3 text-sm",
                            ),
                            rx.el.td(
                                transaction["timestamp"].to_string(),
                                class_name="p-3 text-sm",
                            ),
                            class_name="border-b hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="w-full",
            ),
            class_name="overflow-x-auto rounded-lg border",
        ),
        rx.el.div(
            rx.el.p(
                f"Page {WeighingState.current_page} of {WeighingState.total_pages}",
                class_name="text-sm text-gray-600",
            ),
            rx.el.div(
                rx.el.button(
                    "Previous",
                    on_click=WeighingState.prev_page,
                    disabled=WeighingState.current_page <= 1,
                    class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                ),
                rx.el.button(
                    "Next",
                    on_click=WeighingState.next_page,
                    disabled=WeighingState.current_page >= WeighingState.total_pages,
                    class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                ),
                class_name="flex gap-2",
            ),
            class_name="flex justify-between items-center mt-4",
        ),
        class_name="md:col-span-2 bg-white p-6 rounded-xl border shadow-sm",
    )


from app.components.finance_dashboard import finance_dashboard
from app.states.finance_state import FinanceState
from app.components.payments_page import payments_page
from app.components.receipt_modal import receipt_modal
from app.components.camera_alert_modal import camera_alert_modal
from app.components.vehicle_registration_modal import vehicle_registration_modal
from app.components.camera_page import camera_page
from app.components.vehicles_page import vehicles_page
from app.states.camera_state import CameraState
from app.components.drivers_page import drivers_page
from app.components.customers_page import customers_page
from app.components.settings_page import settings_page
from app.components.payment_modal import payment_modal
from app.components.reports_page import reports_page
from app.components.transactions_page import transactions_page


def dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.cond(
            WeighingState.is_loading,
            rx.el.div(
                rx.el.p("Loading dashboard..."),
                class_name="flex-1 flex items-center justify-center",
            ),
            rx.el.div(
                rx.match(
                    WeighingState.active_page,
                    ("Dashboard", dashboard_content()),
                    ("Finance", finance_dashboard()),
                    ("Payments", payments_page()),
                    ("Camera", camera_page()),
                    ("Transactions", transactions_page()),
                    ("Vehicles", vehicles_page()),
                    ("Drivers", drivers_page()),
                    ("Customers", customers_page()),
                    ("Reports", reports_page()),
                    ("Settings", settings_page()),
                    rx.el.div(
                        f"Content for {WeighingState.active_page}",
                        class_name="flex-1 p-6",
                    ),
                ),
                receipt_modal(),
                camera_alert_modal(),
                vehicle_registration_modal(),
                payment_modal(),
                class_name="relative flex-1",
            ),
        ),
        class_name="grid min-h-screen w-full lg:grid-cols-[280px_1fr] font-['Roboto']",
        font_family="Roboto",
    )