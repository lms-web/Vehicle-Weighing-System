import reflex as rx
from app.states.reports_state import ReportsState


def report_type_selector_button(name: str, current_type: rx.Var[str]) -> rx.Component:
    is_active = name == current_type
    return rx.el.button(
        name,
        on_click=ReportsState.set_report_type(name),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 text-sm font-semibold text-white bg-purple-600 rounded-lg shadow-sm",
            "px-4 py-2 text-sm font-medium text-gray-600 bg-white border rounded-lg hover:bg-gray-50",
        ),
    )


def financial_report_view() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Financial Summary", class_name="text-xl font-semibold mb-4"),
        rx.el.div(
            rx.el.p(f"Total Revenue: {ReportsState.total_revenue}"),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
            rx.recharts.x_axis(data_key="date"),
            rx.recharts.y_axis(),
            rx.recharts.tooltip(),
            rx.recharts.line(
                type="monotone", data_key="total_revenue", stroke="#8884d8"
            ),
            data=ReportsState.daily_summary_data,
            height=300,
            class_name="mt-6",
        ),
        class_name="p-6 mt-6 bg-white rounded-lg border shadow-sm",
    )


def vehicles_report_view() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Vehicle Analytics", class_name="text-xl font-semibold mb-4"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Plate"),
                    rx.el.th("Transactions"),
                    rx.el.th("Total Weight (kg)"),
                    rx.el.th("Total Revenue (Ksh)"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    ReportsState.vehicle_report,
                    lambda item: rx.el.tr(
                        rx.el.td(item["license_plate"]),
                        rx.el.td(item["transaction_count"]),
                        rx.el.td(item["total_weight"]),
                        rx.el.td(item["total_revenue"]),
                    ),
                )
            ),
        ),
        class_name="p-6 mt-6 bg-white rounded-lg border shadow-sm",
    )


def customers_report_view() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Customer Analytics", class_name="text-xl font-semibold mb-4"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Customer"),
                    rx.el.th("Transactions"),
                    rx.el.th("Total Spent (Ksh)"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    ReportsState.customer_report,
                    lambda item: rx.el.tr(
                        rx.el.td(item["customer_name"]),
                        rx.el.td(item["transaction_count"]),
                        rx.el.td(item["total_spent"]),
                    ),
                )
            ),
        ),
        class_name="p-6 mt-6 bg-white rounded-lg border shadow-sm",
    )


def materials_report_view() -> rx.Component:
    return rx.el.div(
        "Materials Report Content",
        class_name="p-6 mt-6 bg-white rounded-lg border shadow-sm",
    )


def drivers_report_view() -> rx.Component:
    return rx.el.div(
        "Drivers Report Content",
        class_name="p-6 mt-6 bg-white rounded-lg border shadow-sm",
    )


def reports_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Reports & Analytics", class_name="text-3xl font-bold text-gray-800"),
        rx.el.div(
            report_type_selector_button("Financial", ReportsState.report_type),
            report_type_selector_button("Vehicles", ReportsState.report_type),
            report_type_selector_button("Customers", ReportsState.report_type),
            report_type_selector_button("Materials", ReportsState.report_type),
            report_type_selector_button("Drivers", ReportsState.report_type),
            class_name="flex gap-2 p-1 bg-gray-100 rounded-lg w-fit mt-6",
        ),
        rx.el.div(
            rx.match(
                ReportsState.report_type,
                ("Financial", financial_report_view()),
                ("Vehicles", vehicles_report_view()),
                ("Customers", customers_report_view()),
                ("Materials", materials_report_view()),
                ("Drivers", drivers_report_view()),
            )
        ),
        class_name="p-6",
        on_mount=ReportsState.load_report_data,
    )