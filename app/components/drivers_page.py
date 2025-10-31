import reflex as rx
from app.states.driver_management_state import DriverManagementState
from app.states.weighing_state import WeighingState


def driver_registration_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                "Add New Driver",
                on_click=DriverManagementState.toggle_registration_modal,
                class_name="flex items-center bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition",
            )
        ),
        rx.radix.primitives.dialog.overlay(class_name="fixed inset-0 bg-black/50 z-40"),
        rx.radix.primitives.dialog.content(
            rx.el.div(
                rx.el.h2("Register New Driver", class_name="text-2xl font-bold mb-4"),
                rx.el.form(
                    rx.el.div(
                        rx.el.label("Full Name", class_name="font-semibold"),
                        rx.el.input(
                            name="name", class_name="w-full p-2 border rounded-lg"
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("License Number", class_name="font-semibold"),
                        rx.el.input(
                            name="license_number",
                            class_name="w-full p-2 border rounded-lg",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Phone Number", class_name="font-semibold"),
                        rx.el.input(
                            name="phone", class_name="w-full p-2 border rounded-lg"
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("ID Number", class_name="font-semibold"),
                        rx.el.input(
                            name="id_number", class_name="w-full p-2 border rounded-lg"
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Assign Vehicles (Optional)", class_name="font-semibold"
                        ),
                        rx.el.div(
                            rx.foreach(
                                WeighingState.vehicles,
                                lambda vehicle: rx.el.label(
                                    rx.el.input(
                                        type="checkbox",
                                        name="vehicle_ids",
                                        key=vehicle["id"],
                                        default_value=vehicle["id"],
                                    ),
                                    rx.el.span(
                                        vehicle["license_plate"], class_name="ml-2"
                                    ),
                                    class_name="flex items-center text-sm",
                                ),
                            ),
                            class_name="grid grid-cols-2 gap-2 p-2 border rounded-lg h-32 overflow-y-auto",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=DriverManagementState.toggle_registration_modal,
                            class_name="w-full bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition",
                            type="button",
                        ),
                        rx.el.button(
                            "Register Driver",
                            class_name="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition",
                            type="submit",
                        ),
                        class_name="flex gap-4 mt-6",
                    ),
                    on_submit=DriverManagementState.register_driver,
                ),
                class_name="p-6",
            ),
            class_name="bg-white rounded-xl shadow-lg max-w-lg mx-auto z-50",
        ),
        open=DriverManagementState.show_registration_modal,
    )


def drivers_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Driver Management", class_name="text-3xl font-bold text-gray-800"
            ),
            driver_registration_modal(),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Search by name, license, phone...",
                on_change=DriverManagementState.set_driver_search_query,
                class_name="w-full md:w-1/3 p-2 border rounded-lg",
            ),
            class_name="flex gap-4 mb-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Name",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "License No.",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Phone",
                            class_name="p-3 text-left text-sm font-semibold text-gray-600",
                        ),
                        rx.el.th(
                            "Assigned Vehicles",
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
                        DriverManagementState.paginated_drivers,
                        lambda driver: rx.el.tr(
                            rx.el.td(
                                driver["name"],
                                class_name="p-3 text-sm font-medium text-gray-800",
                            ),
                            rx.el.td(
                                driver["license_number"], class_name="p-3 text-sm"
                            ),
                            rx.el.td(driver["phone"], class_name="p-3 text-sm"),
                            rx.el.td(
                                driver["associated_vehicle_ids"].length().to_string(),
                                class_name="p-3 text-sm text-center",
                            ),
                            rx.el.td(
                                rx.el.button(
                                    "View Details",
                                    on_click=DriverManagementState.view_driver_details(
                                        driver["id"]
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
                f"Page {DriverManagementState.drivers_page_current} of {DriverManagementState.total_driver_pages}",
                class_name="text-sm text-gray-600",
            ),
            rx.el.div(
                rx.el.button(
                    "Previous",
                    on_click=DriverManagementState.prev_driver_page,
                    disabled=DriverManagementState.drivers_page_current <= 1,
                    class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                ),
                rx.el.button(
                    "Next",
                    on_click=DriverManagementState.next_driver_page,
                    disabled=DriverManagementState.drivers_page_current
                    >= DriverManagementState.total_driver_pages,
                    class_name="px-4 py-2 text-sm font-medium border rounded-lg disabled:opacity-50",
                ),
                class_name="flex gap-2",
            ),
            class_name="flex justify-between items-center mt-4",
        ),
        class_name="p-6",
    )