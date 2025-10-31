import reflex as rx
from app.states.transactions_state import TransactionsState
from app.states.weighing_state import WeighingState


def transaction_detail_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.overlay(class_name="fixed inset-0 bg-black/50 z-40"),
        rx.radix.primitives.dialog.content(
            rx.cond(
                TransactionsState.selected_transaction_detail,
                rx.el.div(
                    rx.el.h2(
                        f"Ticket #{TransactionsState.selected_transaction_detail['transaction']['ticket_number']}",
                        class_name="text-2xl font-bold mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Vehicle Plate: ",
                                rx.el.span(
                                    TransactionsState.selected_transaction_detail[
                                        "vehicle_plate"
                                    ],
                                    class_name="font-mono",
                                ),
                            ),
                            rx.el.p(
                                "Customer: ",
                                rx.el.span(
                                    TransactionsState.selected_transaction_detail[
                                        "customer_name"
                                    ],
                                    class_name="font-medium",
                                ),
                            ),
                            rx.el.p(
                                "Material: ",
                                rx.el.span(
                                    TransactionsState.selected_transaction_detail[
                                        "material_name"
                                    ],
                                    class_name="font-medium",
                                ),
                            ),
                            rx.el.p(
                                "Timestamp: ",
                                rx.el.span(
                                    TransactionsState.selected_transaction_detail[
                                        "transaction"
                                    ]["timestamp"].to_string(),
                                    class_name="font-mono",
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-2 text-sm p-4 bg-gray-50 rounded-lg",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Weight Information",
                                class_name="text-lg font-semibold mt-4 mb-2",
                            ),
                            rx.el.div(
                                rx.el.p("Tare Weight:", class_name="font-semibold"),
                                rx.el.p(
                                    f"{TransactionsState.selected_transaction_detail['weight_record']['tare_weight']} kg"
                                ),
                                class_name="flex justify-between p-2 bg-gray-100 rounded-md",
                            ),
                            rx.el.div(
                                rx.el.p("Gross Weight:", class_name="font-semibold"),
                                rx.el.p(
                                    f"{TransactionsState.selected_transaction_detail['weight_record']['gross_weight']} kg"
                                ),
                                class_name="flex justify-between p-2 bg-white rounded-md",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Net Weight:", class_name="font-bold text-blue-600"
                                ),
                                rx.el.p(
                                    f"{TransactionsState.selected_transaction_detail['weight_record']['net_weight']} kg",
                                    class_name="font-bold text-blue-600",
                                ),
                                class_name="flex justify-between p-2 bg-blue-50 rounded-md mt-1",
                            ),
                            class_name="text-sm mt-4",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Payment Information",
                                class_name="text-lg font-semibold mt-4 mb-2",
                            ),
                            rx.el.div(
                                rx.el.p("Amount Due:", class_name="font-semibold"),
                                rx.el.p("Ksh 16,411.88", class_name="font-mono"),
                                class_name="flex justify-between p-2",
                            ),
                            rx.el.div(
                                rx.el.p("Payment Status:", class_name="font-semibold"),
                                rx.el.span(
                                    "Completed",
                                    class_name="px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full",
                                ),
                                class_name="flex justify-between items-center p-2",
                            ),
                            class_name="text-sm mt-4",
                        ),
                        class_name="space-y-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Close",
                            on_click=TransactionsState.close_detail_modal,
                            class_name="w-full mt-6 bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition",
                        ),
                        class_name="mt-6",
                    ),
                    class_name="p-6",
                ),
            ),
            class_name="bg-white rounded-xl shadow-lg max-w-lg mx-auto z-50",
        ),
        open=TransactionsState.show_detail_modal,
    )


def transactions_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            "Transactions Log", class_name="text-3xl font-bold text-gray-800 mb-6"
        ),
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    placeholder="Search by ticket...",
                    on_change=TransactionsState.set_search_query.debounce(500),
                    class_name="p-2 border rounded-lg",
                ),
                rx.el.input(
                    type="date",
                    on_change=TransactionsState.set_filter_date_start,
                    default_value=TransactionsState.filter_date_start,
                    class_name="p-2 border rounded-lg",
                ),
                rx.el.input(
                    type="date",
                    on_change=TransactionsState.set_filter_date_end,
                    default_value=TransactionsState.filter_date_end,
                    class_name="p-2 border rounded-lg",
                ),
                rx.el.select(
                    rx.el.option("All Types", value="ALL"),
                    rx.el.option("IN", value="IN"),
                    rx.el.option("OUT", value="OUT"),
                    on_change=TransactionsState.set_filter_transaction_type,
                    class_name="p-2 border rounded-lg bg-white",
                ),
                rx.el.select(
                    rx.el.option("All Statuses", value="ALL"),
                    rx.el.option("Paid", value="Paid"),
                    rx.el.option("Pending", value="Pending"),
                    rx.el.option("Overdue", value="Overdue"),
                    on_change=TransactionsState.set_filter_payment_status,
                    class_name="p-2 border rounded-lg bg-white",
                ),
                class_name="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6 p-4 bg-gray-50 rounded-lg border",
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
                            rx.el.th(
                                "Status",
                                class_name="p-3 text-center text-sm font-semibold text-gray-600",
                            ),
                            rx.el.th(
                                "Actions",
                                class_name="p-3 text-left text-sm font-semibold text-gray-600",
                            ),
                        ),
                        class_name="bg-gray-50",
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            TransactionsState.paginated_transactions,
                            lambda transaction: rx.el.tr(
                                rx.el.td(
                                    transaction["ticket_number"],
                                    class_name="p-3 text-sm font-mono",
                                ),
                                rx.el.td(
                                    WeighingState.vehicle_plates[
                                        transaction["vehicle_id"].to_string()
                                    ],
                                    class_name="p-3 text-sm font-medium",
                                ),
                                rx.el.td(
                                    transaction["transaction_type"],
                                    class_name="p-3 text-sm",
                                ),
                                rx.el.td(
                                    transaction["timestamp"].to_string(),
                                    class_name="p-3 text-sm",
                                ),
                                rx.el.td(
                                    rx.el.span(
                                        "Paid",
                                        class_name="px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full",
                                    ),
                                    class_name="p-3 text-center",
                                ),
                                rx.el.td(
                                    rx.el.button(
                                        "View",
                                        on_click=TransactionsState.view_transaction_details(
                                            transaction["id"]
                                        ),
                                        class_name="text-purple-600 hover:underline text-sm font-medium",
                                    ),
                                    class_name="p-3",
                                ),
                                class_name="border-b hover:bg-gray-50",
                            ),
                        )
                    ),
                    class_name="w-full",
                ),
                class_name="overflow-x-auto rounded-lg border bg-white shadow-sm",
            ),
            rx.el.div(
                rx.el.p(
                    f"Page {TransactionsState.current_page} of {TransactionsState.total_pages}",
                    class_name="text-sm text-gray-600",
                ),
                rx.el.div(
                    rx.el.button(
                        "Previous",
                        on_click=TransactionsState.prev_page,
                        disabled=TransactionsState.current_page <= 1,
                        class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                    ),
                    rx.el.button(
                        "Next",
                        on_click=TransactionsState.next_page,
                        disabled=TransactionsState.current_page
                        >= TransactionsState.total_pages,
                        class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                    ),
                    class_name="flex gap-2",
                ),
                class_name="flex justify-between items-center mt-4",
            ),
        ),
        transaction_detail_modal(),
        class_name="p-6",
        on_mount=TransactionsState.load_transactions,
    )