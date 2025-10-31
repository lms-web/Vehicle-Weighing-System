import reflex as rx
from app.states.settings_state import SettingsState


def settings_tab(tab_name: str) -> rx.Component:
    is_active = SettingsState.active_tab == tab_name
    return rx.el.button(
        tab_name,
        on_click=SettingsState.set_active_tab(tab_name),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 font-semibold text-purple-600 border-b-2 border-purple-600",
            "px-4 py-2 font-medium text-gray-500 hover:text-gray-700",
        ),
    )


def pricing_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Pricing Rules Management", class_name="text-xl font-semibold mb-4"),
        rx.el.p(
            "Configure pricing for different material types and vehicles.",
            class_name="text-gray-500",
        ),
        class_name="p-6 bg-white rounded-lg border shadow-sm mt-6",
    )


def users_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h3("User Management", class_name="text-xl font-semibold mb-4"),
        rx.el.p(
            "Manage user accounts, roles, and permissions.", class_name="text-gray-500"
        ),
        class_name="p-6 bg-white rounded-lg border shadow-sm mt-6",
    )


def system_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h3("System Configuration", class_name="text-xl font-semibold mb-4"),
        rx.el.p("General system settings and preferences.", class_name="text-gray-500"),
        class_name="p-6 bg-white rounded-lg border shadow-sm mt-6",
    )


def camera_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Camera & ANPR Settings", class_name="text-xl font-semibold mb-4"),
        rx.el.p(
            "Configure camera feeds and ANPR integration.", class_name="text-gray-500"
        ),
        class_name="p-6 bg-white rounded-lg border shadow-sm mt-6",
    )


def notifications_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Notification Settings", class_name="text-xl font-semibold mb-4"),
        rx.el.p("Set up alerts and notifications.", class_name="text-gray-500"),
        class_name="p-6 bg-white rounded-lg border shadow-sm mt-6",
    )


def settings_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Settings", class_name="text-3xl font-bold text-gray-800"),
        rx.el.div(
            settings_tab("Pricing"),
            settings_tab("Users"),
            settings_tab("System"),
            settings_tab("Camera"),
            settings_tab("Notifications"),
            class_name="flex border-b mt-6",
        ),
        rx.el.div(
            rx.match(
                SettingsState.active_tab,
                ("Pricing", pricing_settings()),
                ("Users", users_settings()),
                ("System", system_settings()),
                ("Camera", camera_settings()),
                ("Notifications", notifications_settings()),
            )
        ),
        class_name="p-6",
    )