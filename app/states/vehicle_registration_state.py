import reflex as rx
from typing import Optional


class VehicleRegistrationState(rx.State):
    """State for handling new vehicle registration."""

    new_vehicle_plate: str = ""
    new_vehicle_type: str = "Truck"
    new_vehicle_make: str = ""
    new_vehicle_model: str = ""
    new_vehicle_color: str = ""
    selected_driver_id: str | None = None
    show_new_driver_form: bool = False
    new_driver_name: str = ""
    new_driver_license: str = ""
    new_driver_phone: str = ""
    new_driver_id_number: str = ""

    @rx.event
    async def register_vehicle(self, form_data: dict):
        from app.states.weighing_state import WeighingState
        from app.states.camera_state import CameraState

        weighing_state = await self.get_state(WeighingState)
        new_vehicle_id = len(weighing_state.vehicles) + 1
        new_vehicle = {
            "id": new_vehicle_id,
            "license_plate": form_data["license_plate"],
            "vehicle_type": form_data["vehicle_type"],
            "make": form_data["make"],
            "model": form_data["model"],
            "color": form_data["color"],
        }
        self.selected_driver_id = form_data.get("driver_id")
        weighing_state.vehicles.append(new_vehicle)
        if self.show_new_driver_form:
            new_driver_id_val = len(weighing_state.drivers) + 1
            new_driver = {
                "id": new_driver_id_val,
                "name": self.new_driver_name,
                "license_number": self.new_driver_license,
                "phone": self.new_driver_phone,
                "id_number": self.new_driver_id_number,
                "photo": "/placeholder.svg",
                "associated_vehicle_ids": [new_vehicle_id],
            }
            weighing_state.drivers.append(new_driver)
        elif self.selected_driver_id:
            driver_id_int = int(self.selected_driver_id)
            for driver in weighing_state.drivers:
                if driver["id"] == driver_id_int:
                    driver["associated_vehicle_ids"].append(new_vehicle_id)
                    break
        print(f"Registered new vehicle: {new_vehicle['license_plate']}")
        camera_state = await self.get_state(CameraState)
        camera_state.show_registration_form = False
        self._reset_form()

    def _reset_form(self):
        self.new_vehicle_plate = ""
        self.new_vehicle_type = "Truck"
        self.new_vehicle_make = ""
        self.new_vehicle_model = ""
        self.new_vehicle_color = ""
        self.selected_driver_id = None
        self.show_new_driver_form = False
        self.new_driver_name = ""
        self.new_driver_license = ""
        self.new_driver_phone = ""
        self.new_driver_id_number = ""

    @rx.event
    async def cancel_registration(self):
        from app.states.camera_state import CameraState

        camera_state = await self.get_state(CameraState)
        camera_state.show_registration_form = False
        self._reset_form()