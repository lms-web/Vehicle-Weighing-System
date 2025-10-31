import reflex as rx
from app.states.camera_state import CameraState
from app.components.camera_alert_modal import camera_toggle_button


def camera_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Camera Feed", class_name="text-3xl font-bold text-gray-800"),
            camera_toggle_button(),
            class_name="relative flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.cond(
                CameraState.is_camera_active,
                rx.el.div(
                    rx.el.img(
                        src="/placeholder.svg", class_name="w-full rounded-lg shadow-md"
                    ),
                    rx.el.div(
                        rx.icon("video", class_name="h-5 w-5 text-red-500"),
                        rx.el.p("LIVE", class_name="font-bold text-red-500"),
                        class_name="absolute top-4 left-4 bg-white/80 px-3 py-1 rounded-full flex items-center gap-2 text-sm",
                    ),
                ),
                rx.el.div(
                    rx.icon("video_off", class_name="h-16 w-16 text-gray-400"),
                    rx.el.p(
                        "Camera is Inactive", class_name="text-gray-500 mt-4 text-lg"
                    ),
                    class_name="flex flex-col items-center justify-center h-96 border-2 border-dashed rounded-lg bg-gray-50",
                ),
            ),
            class_name="relative",
        ),
        class_name="p-6",
    )