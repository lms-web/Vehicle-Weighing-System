import reflex as rx
from app.states.customer_management_state import CustomerManagementState


def customer_registration_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                "Add New Customer",
                on_click=CustomerManagementState.toggle_registration_modal,
                class_name="flex items-center bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition",
            )
        ),
        rx.radix.primitives.dialog.overlay(class_name="fixed inset-0 bg-black/50 z-40"),
        rx.radix.primitives.dialog.content(
            rx.el.div(
                rx.el.h2("Register New Customer", class_name="text-2xl font-bold mb-4"),
                rx.el.form(
                    rx.el.div(
                        rx.el.label("Customer Name", class_name="font-semibold"),
                        rx.el.input(
                            placeholder="e.g., John Doe",
                            name="customer_name",
                            class_name="w-full p-2 border rounded-lg",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Company", class_name="font-semibold"),
                        rx.el.input(
                            placeholder="e.g., BuildCo Inc.",
                            name="company",
                            class_name="w-full p-2 border rounded-lg",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Contact Info", class_name="font-semibold"),
                        rx.el.input(
                            placeholder="e.g., 555-1234",
                            name="contact_info",
                            class_name="w-full p-2 border rounded-lg",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Billing Address", class_name="font-semibold"),
                        rx.el.input(
                            placeholder="e.g., 123 Main St, Nairobi",
                            name="billing_address",
                            class_name="w-full p-2 border rounded-lg",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Credit Limit (Ksh)", class_name="font-semibold"),
                        rx.el.input(
                            placeholder="e.g., 50000",
                            name="credit_limit",
                            type="number",
                            class_name="w-full p-2 border rounded-lg",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=CustomerManagementState.toggle_registration_modal,
                            class_name="w-full bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition",
                            type="button",
                        ),
                        rx.el.button(
                            "Register Customer",
                            class_name="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition",
                            type="submit",
                        ),
                        class_name="flex gap-4 mt-6",
                    ),
                    on_submit=CustomerManagementState.register_customer,
                ),
                class_name="p-6",
            ),
            class_name="bg-white rounded-xl shadow-lg max-w-lg mx-auto z-50",
        ),
        open=CustomerManagementState.show_registration_modal,
    )


def customers_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Customer Management", class_name="text-3xl font-bold text-gray-800"
            ),
            customer_registration_modal(),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Search by name, company...",
                on_change=CustomerManagementState.set_customer_search_query,
                class_name="w-full md:w-1/3 p-2 border rounded-lg",
            ),
            class_name="flex gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Customer Name",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Company",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Contact",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Transactions",
                            class_name="p-3 text-center text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Outstanding",
                            class_name="p-3 text-right text-sm font-semibold text-gray-600",
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
                        CustomerManagementState.paginated_customers,
                        lambda customer: rx.el.tr(
                            rx.el.td(
                                customer["customer_name"],
                                class_name="p-3 text-sm font-medium text-gray-800",
                            ),
                            rx.el.td(customer["company"], class_name="p-3 text-sm"),
                            rx.el.td(
                                customer["contact_info"], class_name="p-3 text-sm"
                            ),
                            rx.el.td("0", class_name="p-3 text-sm text-center"),
                            rx.el.td(
                                f"Ksh {customer['credit_limit']}",
                                class_name="p-3 text-sm text-right font-mono",
                            ),
                            rx.el.td(
                                rx.el.button(
                                    "View Details",
                                    on_click=CustomerManagementState.view_customer_details(
                                        customer["id"]
                                    ),
                                    class_name="text-purple-600 hover:underline text-sm font-medium",
                                ),
                                class_name="p-3 text-sm",
                            ),
                            class_name="border-b hover:bg-gray-50",
                        ),
                    )
                ),
                class_name="w-full",
            ),
            class_name="overflow-x-auto rounded-lg border bg-white mt-6 shadow-sm",
        ),
        rx.el.div(
            rx.el.p(
                f"Page {CustomerManagementState.customers_page_current} of {CustomerManagementState.total_customer_pages}",
                class_name="text-sm text-gray-600",
            ),
            rx.el.div(
                rx.el.button(
                    "Previous",
                    on_click=CustomerManagementState.prev_customer_page,
                    disabled=CustomerManagementState.customers_page_current <= 1,
                    class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                ),
                rx.el.button(
                    "Next",
                    on_click=CustomerManagementState.next_customer_page,
                    disabled=CustomerManagementState.customers_page_current
                    >= CustomerManagementState.total_customer_pages,
                    class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                ),
                class_name="flex gap-2",
            ),
            class_name="flex justify-between items-center mt-4",
        ),
        class_name="p-6",
    )