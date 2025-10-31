import reflex as rx
from app.states.vehicle_registration_state import VehicleRegistrationState
from app.states.weighing_state import WeighingState
from app.states.camera_state import CameraState


def vehicle_registration_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.overlay(class_name="fixed inset-0 bg-black/50 z-40"),
        rx.radix.primitives.dialog.content(
            rx.el.div(
                rx.el.h2("Register New Vehicle", class_name="text-2xl font-bold mb-4"),
                rx.el.form(
                    rx.el.div(
                        rx.el.label("License Plate", class_name="font-semibold"),
                        rx.el.input(
                            default_value=VehicleRegistrationState.new_vehicle_plate,
                            is_disabled=True,
                            class_name="w-full p-2 border rounded-lg bg-gray-100",
                            name="license_plate",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Vehicle Type", class_name="font-semibold"),
                        rx.el.input(
                            placeholder="e.g., Truck, Van",
                            default_value=VehicleRegistrationState.new_vehicle_type,
                            class_name="w-full p-2 border rounded-lg",
                            name="vehicle_type",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Make", class_name="font-semibold"),
                        rx.el.input(
                            placeholder="e.g., Volvo, Ford",
                            default_value=VehicleRegistrationState.new_vehicle_make,
                            class_name="w-full p-2 border rounded-lg",
                            name="make",
                        ),
                        rx.el.label("Model", class_name="font-semibold"),
                        rx.el.input(
                            placeholder="e.g., VNL, Transit",
                            default_value=VehicleRegistrationState.new_vehicle_model,
                            class_name="w-full p-2 border rounded-lg",
                            name="model",
                        ),
                        class_name="grid grid-cols-2 gap-4 mb-3",
                    ),
                    rx.el.div(
                        rx.el.label("Color", class_name="font-semibold"),
                        rx.el.input(
                            placeholder="e.g., Blue, White",
                            default_value=VehicleRegistrationState.new_vehicle_color,
                            class_name="w-full p-2 border rounded-lg",
                            name="color",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Assign Driver (Optional)", class_name="font-semibold"
                        ),
                        rx.el.select(
                            rx.el.option("Select a driver", value=""),
                            rx.foreach(
                                WeighingState.drivers,
                                lambda driver: rx.el.option(
                                    driver["name"], value=driver["id"]
                                ),
                            ),
                            on_change=VehicleRegistrationState.set_selected_driver_id,
                            class_name="w-full p-2 border rounded-lg bg-white",
                            name="driver_id",
                        ),
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=VehicleRegistrationState.cancel_registration,
                            class_name="w-full bg-gray-200 text-gray-800 font-semibold py-2 px-4 rounded-lg hover:bg-gray-300 transition",
                            type="button",
                        ),
                        rx.el.button(
                            "Register Vehicle",
                            class_name="w-full bg-purple-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-purple-700 transition",
                            type="submit",
                        ),
                        class_name="flex gap-4 mt-6",
                    ),
                    on_submit=VehicleRegistrationState.register_vehicle,
                ),
                class_name="p-6",
            ),
            class_name="bg-white rounded-xl shadow-lg max-w-lg mx-auto z-50",
        ),
        open=CameraState.show_registration_form,
    )