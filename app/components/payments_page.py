import reflex as rx
from app.states.mpesa_state import MpesaState


def payments_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("M-Pesa Payments", class_name="text-3xl font-bold mb-6 text-gray-800"),
        rx.el.div(
            rx.el.h2(
                "Initiate STK Push",
                class_name="text-xl font-semibold text-gray-700 mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Phone Number (254...)",
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
                rx.el.label(
                    "Amount (Ksh)",
                    class_name="block text-sm font-medium text-gray-600 mb-1",
                ),
                rx.el.input(
                    type="number",
                    placeholder="100",
                    on_change=MpesaState.set_amount,
                    class_name="w-full p-2 border rounded-lg",
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Pay Now",
                on_click=MpesaState.initiate_stk_push(
                    MpesaState.phone_number, MpesaState.amount
                ),
                is_loading=MpesaState.is_processing,
                class_name="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition disabled:opacity-50",
                disabled=MpesaState.is_processing,
            ),
            rx.cond(
                MpesaState.payment_status,
                rx.el.div(
                    MpesaState.payment_status,
                    class_name="mt-4 p-3 rounded-lg bg-green-100 text-green-700",
                ),
            ),
            rx.cond(
                MpesaState.error_message,
                rx.el.div(
                    MpesaState.error_message,
                    class_name="mt-4 p-3 rounded-lg bg-red-100 text-red-700",
                ),
            ),
            class_name="bg-white p-6 rounded-xl border shadow-sm",
        ),
        class_name="p-6",
    )