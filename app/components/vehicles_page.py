import reflex as rx
from app.states.weighing_state import WeighingState


def vehicle_status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Active",
                "px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full",
            ),
            (
                "Inactive",
                "px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-100 rounded-full",
            ),
            (
                "Under Maintenance",
                "px-2 py-1 text-xs font-semibold text-yellow-800 bg-yellow-100 rounded-full",
            ),
            (
                "Blacklisted",
                "px-2 py-1 text-xs font-semibold text-red-800 bg-red-100 rounded-full",
            ),
            "px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-100 rounded-full",
        ),
    )


def vehicle_analytics_card(title: str, value: rx.Var, icon: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="h-6 w-6 text-gray-400"),
        rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        class_name="flex flex-col gap-1 p-4 bg-gray-50 rounded-lg",
    )


def vehicle_detail_view() -> rx.Component:
    v = WeighingState.selected_vehicle_detail
    return rx.el.div(
        rx.el.button(
            rx.icon("arrow_left", class_name="h-4 w-4 mr-2"),
            "Back to Vehicle List",
            on_click=WeighingState.set_selected_vehicle_detail(None),
            class_name="flex items-center text-sm font-medium text-purple-600 hover:underline mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.image(
                    src="/placeholder.svg",
                    class_name="w-32 h-32 rounded-lg object-cover",
                ),
                rx.el.div(
                    rx.el.h2(
                        v["license_plate"],
                        class_name="text-3xl font-bold text-gray-800",
                    ),
                    vehicle_status_badge(v["status"]),
                    class_name="flex items-center gap-4",
                ),
                rx.el.p(
                    f"{v['make']} {v['model']} ({v['vehicle_type']}) - {v['color']}",
                    class_name="text-gray-600",
                ),
                class_name="flex flex-col gap-2",
            ),
            class_name="p-6 bg-white rounded-xl border shadow-sm flex items-center gap-6",
        ),
        rx.el.div(
            vehicle_analytics_card(
                "Total Transactions",
                WeighingState.selected_vehicle_transaction_count,
                "receipt-text",
            ),
            vehicle_analytics_card(
                "Total Weight Moved",
                f"{WeighingState.selected_vehicle_total_weight.to_string()} kg",
                "weight",
            ),
            vehicle_analytics_card(
                "Revenue Generated",
                f"Ksh {WeighingState.selected_vehicle_revenue.to_string()}",
                "banknote",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6",
        ),
        vehicle_maintenance_table(),
        vehicle_history_table(WeighingState.vehicle_history),
    )


def vehicle_history_table(history: rx.Var[list[dict]]) -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Weighing History", class_name="text-lg font-semibold mb-4 text-gray-800"
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Ticket"),
                        rx.el.th("Type"),
                        rx.el.th("Timestamp"),
                        class_name="text-left text-sm font-semibold text-gray-600",
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        history,
                        lambda transaction: rx.el.tr(
                            rx.el.td(transaction["ticket_number"], class_name="p-3"),
                            rx.el.td(transaction["transaction_type"], class_name="p-3"),
                            rx.el.td(
                                transaction["timestamp"].to_string(), class_name="p-3"
                            ),
                            class_name="border-b text-sm",
                        ),
                    )
                ),
                class_name="w-full",
            ),
            class_name="overflow-x-auto rounded-lg border",
        ),
        class_name="p-6 bg-white rounded-xl border shadow-sm mt-6",
    )


def vehicle_maintenance_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Maintenance Logs", class_name="text-lg font-semibold mb-4"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Date"),
                        rx.el.th("Service Type"),
                        rx.el.th("Notes"),
                        rx.el.th("Cost"),
                        rx.el.th("Next Due"),
                        class_name="text-left text-sm font-semibold text-gray-600",
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        WeighingState.selected_vehicle_maintenance_logs,
                        lambda log: rx.el.tr(
                            rx.el.td(log["service_date"], class_name="p-3"),
                            rx.el.td(log["service_type"], class_name="p-3"),
                            rx.el.td(log["notes"], class_name="p-3"),
                            rx.el.td(
                                f"Ksh {log['cost'].to_string()}", class_name="p-3"
                            ),
                            rx.el.td(log["next_service_due"], class_name="p-3"),
                            class_name="border-b text-sm",
                        ),
                    )
                ),
                class_name="w-full",
            ),
            class_name="overflow-x-auto rounded-lg border",
        ),
        class_name="p-6 bg-white rounded-xl border shadow-sm mt-6",
    )


def vehicle_list_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Vehicle Registry", class_name="text-3xl font-bold text-gray-800"),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                "Register New Vehicle",
                class_name="flex items-center bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Search by plate, make...",
                on_change=WeighingState.set_vehicle_search_query,
                class_name="p-2 border rounded-lg w-full",
            ),
            rx.el.select(
                rx.el.option("All Types", value="ALL"),
                rx.el.option("Truck", value="Truck"),
                rx.el.option("Van", value="Van"),
                on_change=WeighingState.set_vehicle_filter_type,
                class_name="p-2 border rounded-lg bg-white",
            ),
            rx.el.select(
                rx.el.option("All Statuses", value="ALL"),
                rx.el.option("Active", value="Active"),
                rx.el.option("Inactive", value="Inactive"),
                rx.el.option("Under Maintenance", value="Under Maintenance"),
                on_change=WeighingState.set_vehicle_filter_status,
                class_name="p-2 border rounded-lg bg-white",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 p-4 bg-gray-50 rounded-lg border",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Plate"),
                        rx.el.th("Type"),
                        rx.el.th("Make/Model"),
                        rx.el.th("Status"),
                        rx.el.th("Actions"),
                        class_name="text-left text-sm font-semibold text-gray-600",
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        WeighingState.paginated_vehicles,
                        lambda vehicle: rx.el.tr(
                            rx.el.td(
                                rx.el.image(
                                    src="/placeholder.svg",
                                    class_name="h-8 w-8 rounded-full object-cover inline-block mr-2",
                                ),
                                vehicle["license_plate"],
                                class_name="p-3 font-medium text-gray-800 flex items-center",
                            ),
                            rx.el.td(vehicle["vehicle_type"], class_name="p-3"),
                            rx.el.td(
                                f"{vehicle['make']} {vehicle['model']}",
                                class_name="p-3",
                            ),
                            rx.el.td(
                                vehicle_status_badge(vehicle["status"]),
                                class_name="p-3",
                            ),
                            rx.el.td(
                                rx.el.button(
                                    "View Details",
                                    on_click=WeighingState.view_vehicle_details(
                                        vehicle["id"]
                                    ),
                                    class_name="text-purple-600 hover:underline font-medium",
                                ),
                                class_name="p-3",
                            ),
                            class_name="border-b text-sm",
                        ),
                    )
                ),
                class_name="w-full",
            ),
            class_name="overflow-x-auto rounded-lg border bg-white mt-6 shadow-sm",
        ),
        rx.el.div(
            rx.el.p(
                f"Page {WeighingState.vehicles_current_page} of {WeighingState.total_vehicle_pages}",
                class_name="text-sm text-gray-600",
            ),
            rx.el.div(
                rx.el.button(
                    "Previous",
                    on_click=WeighingState.prev_vehicle_page,
                    disabled=WeighingState.vehicles_current_page <= 1,
                    class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                ),
                rx.el.button(
                    "Next",
                    on_click=WeighingState.next_vehicle_page,
                    disabled=WeighingState.vehicles_current_page
                    >= WeighingState.total_vehicle_pages,
                    class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                ),
                class_name="flex gap-2",
            ),
            class_name="flex justify-between items-center mt-4",
        ),
    )


def vehicles_page() -> rx.Component:
    return rx.el.div(
        rx.cond(
            WeighingState.selected_vehicle_detail,
            vehicle_detail_view(),
            vehicle_list_view(),
        ),
        class_name="p-6",
    )