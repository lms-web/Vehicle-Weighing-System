import reflex as rx
from app.states.weighing_state import WeighingState
from app.states.mpesa_state import MpesaState


def payment_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.overlay(class_name="fixed inset-0 bg-black/50 z-40"),
        rx.radix.primitives.dialog.content(
            rx.el.div(
                rx.el.h2("Complete Payment", class_name="text-2xl font-bold mb-4"),
                rx.el.div(
                    rx.el.p("Amount Due:", class_name="font-semibold text-lg"),
                    rx.el.p(
                        f"Ksh {WeighingState.amount_due.to_string()}",
                        class_name="font-bold text-2xl text-green-600",
                    ),
                    class_name="flex justify-between items-center p-4 bg-green-50 rounded-lg mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Phone Number (for M-Pesa)",
                        class_name="block text-sm font-medium text-gray-600 mb-1",
                    ),
                    rx.el.input(
                        placeholder="254712345678",
                        on_change=MpesaState.set_phone_number,
                        class_name="w-full p-2 border rounded-lg",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=WeighingState.close_payment_modal,
                        class_name="w-full bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition",
                    ),
                    rx.el.button(
                        "Confirm Payment",
                        on_click=WeighingState.process_payment_and_complete,
                        class_name="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition",
                    ),
                    class_name="flex gap-4 mt-6",
                ),
                class_name="p-6",
            ),
            class_name="bg-white rounded-xl shadow-lg max-w-lg mx-auto z-50",
        ),
        open=WeighingState.show_payment_modal,
    )