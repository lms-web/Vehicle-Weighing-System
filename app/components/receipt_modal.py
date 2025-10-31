import reflex as rx
from app.states.receipt_state import ReceiptState
from app.states.weighing_state import WeighingState


def receipt_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.overlay(class_name="fixed inset-0 bg-black/50"),
        rx.radix.primitives.dialog.content(
            rx.el.div(
                rx.el.div(
                    rx.el.h2("Receipt", class_name="text-2xl font-bold"),
                    rx.el.p(
                        f"Receipt #: {ReceiptState.current_receipt['receipt_number']}",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="text-center",
                ),
                rx.el.div(
                    rx.el.p("Company Logo", class_name="text-center font-bold my-4"),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("Transaction ID:", class_name="font-semibold"),
                            rx.el.p(
                                ReceiptState.current_receipt[
                                    "transaction_id"
                                ].to_string()
                            ),
                            class_name="flex justify-between",
                        ),
                        rx.el.div(
                            rx.el.p("Amount Paid:", class_name="font-semibold"),
                            rx.el.p(
                                f"Ksh {ReceiptState.current_receipt['amount_paid'].to_string()}"
                            ),
                            class_name="flex justify-between",
                        ),
                        rx.el.div(
                            rx.el.p("Payment Method:", class_name="font-semibold"),
                            rx.el.p(ReceiptState.current_receipt["payment_method"]),
                            class_name="flex justify-between",
                        ),
                        rx.cond(
                            ReceiptState.current_receipt["mpesa_code"],
                            rx.el.div(
                                rx.el.p("M-Pesa Code:", class_name="font-semibold"),
                                rx.el.p(ReceiptState.current_receipt["mpesa_code"]),
                                class_name="flex justify-between",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p("Date Issued:", class_name="font-semibold"),
                            rx.el.p(ReceiptState.current_receipt["issued_date"]),
                            class_name="flex justify-between",
                        ),
                        class_name="space-y-2 mt-4",
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        "Print",
                        class_name="w-full bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition",
                    ),
                    rx.el.button(
                        "Close",
                        on_click=ReceiptState.close_receipt_modal,
                        class_name="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition",
                    ),
                    class_name="mt-6 flex gap-4",
                ),
                class_name="p-6",
            ),
            class_name="bg-white rounded-xl shadow-lg max-w-md mx-auto",
        ),
        open=ReceiptState.show_receipt_modal,
    )