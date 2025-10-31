import reflex as rx
from app.states.camera_state import CameraState


def camera_alert_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(rx.el.div()),
        rx.radix.primitives.dialog.overlay(class_name="fixed inset-0 bg-black/50 z-40"),
        rx.radix.primitives.dialog.content(
            rx.cond(
                CameraState.detected_vehicle,
                rx.el.div(
                    rx.el.div(
                        rx.el.h2("Vehicle Detected", class_name="text-2xl font-bold"),
                        rx.el.p(
                            "A vehicle has been detected at the entry gate.",
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="text-center",
                    ),
                    rx.el.div(
                        rx.el.img(
                            src=CameraState.detected_vehicle["image_url"],
                            class_name="rounded-lg w-full h-auto",
                        ),
                        class_name="my-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("License Plate:", class_name="font-semibold"),
                            rx.el.p(
                                CameraState.detected_vehicle["plate"],
                                class_name="font-mono text-lg bg-gray-100 p-2 rounded-md",
                            ),
                            class_name="flex justify-between items-center",
                        ),
                        rx.el.div(
                            rx.el.p("Confidence:", class_name="font-semibold"),
                            rx.el.p(
                                f"{(CameraState.detected_vehicle['confidence'] * 100).to_string()}%",
                                class_name="font-mono text-lg",
                            ),
                            class_name="flex justify-between items-center",
                        ),
                        class_name="mb-4 space-y-1",
                    ),
                    rx.cond(
                        CameraState.detected_vehicle["is_known"],
                        rx.el.div(
                            rx.icon("check_check", class_name="h-5 w-5 text-green-500"),
                            rx.el.p(
                                "Vehicle is registered.",
                                class_name="text-green-600 font-medium",
                            ),
                            class_name="flex items-center gap-2 p-3 bg-green-50 rounded-lg",
                        ),
                        rx.el.div(
                            rx.icon(
                                "flag_triangle_right",
                                class_name="h-5 w-5 text-yellow-500",
                            ),
                            rx.el.p(
                                "Vehicle not found in registry.",
                                class_name="text-yellow-600 font-medium",
                            ),
                            class_name="flex items-center gap-2 p-3 bg-yellow-50 rounded-lg",
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Reject",
                            on_click=CameraState.reject_vehicle,
                            class_name="w-full bg-red-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-red-600 transition",
                        ),
                        rx.el.button(
                            "Accept",
                            on_click=CameraState.accept_vehicle,
                            class_name="w-full bg-green-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-green-700 transition",
                        ),
                        class_name="mt-6 flex gap-4",
                    ),
                    class_name="p-6",
                ),
            ),
            class_name="bg-white rounded-xl shadow-lg max-w-md mx-auto z-50",
        ),
        open=CameraState.show_alert_modal,
    )


def camera_toggle_button() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon("camera", class_name="h-5 w-5"),
            rx.cond(
                CameraState.is_camera_active, "Deactivate Camera", "Activate Camera"
            ),
            on_click=CameraState.toggle_camera_feed,
            class_name=rx.cond(
                CameraState.is_camera_active,
                "flex items-center gap-2 px-3 py-2 rounded-lg bg-red-100 text-red-600 hover:bg-red-200 transition-all",
                "flex items-center gap-2 px-3 py-2 rounded-lg bg-green-100 text-green-600 hover:bg-green-200 transition-all",
            ),
        ),
        class_name="absolute top-4 right-4 z-10",
    )