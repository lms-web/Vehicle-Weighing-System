import reflex as rx
import asyncio
import random
from typing import TypedDict, Optional


class DetectedVehicle(TypedDict):
    plate: str
    image_url: str
    is_known: bool
    vehicle_id: Optional[int]
    confidence: float


class Notification(TypedDict):
    id: int
    message: str
    timestamp: str
    type: str
    read: bool


class CameraState(rx.State):
    """Manages ANPR camera integration and vehicle detection alerts."""

    is_camera_active: bool = False
    show_alert_modal: bool = False
    show_registration_form: bool = False
    detected_vehicle: Optional[DetectedVehicle] = None
    pending_registration_plate: str = ""
    notifications: list[Notification] = []
    notification_count: int = 0
    show_notifications: bool = False

    @rx.event(background=True)
    async def toggle_camera_feed(self):
        async with self:
            self.is_camera_active = not self.is_camera_active
        if self.is_camera_active:
            yield CameraState.simulate_vehicle_detection

    @rx.event(background=True)
    async def simulate_vehicle_detection(self):
        from app.states.weighing_state import WeighingState

        while True:
            async with self:
                if not self.is_camera_active:
                    break
            await asyncio.sleep(random.randint(10, 20))
            async with self:
                weighing_state = await self.get_state(WeighingState)
                known_vehicles = weighing_state.vehicles
                if random.choice([True, False]) and known_vehicles:
                    vehicle = random.choice(known_vehicles)
                    self.detected_vehicle = {
                        "plate": vehicle["license_plate"],
                        "image_url": "/placeholder.svg",
                        "is_known": True,
                        "vehicle_id": vehicle["id"],
                        "confidence": round(random.uniform(0.9, 0.99), 2),
                    }
                else:
                    plate = f"K{random.choice('ABCDEF')}{random.choice('ABCDEF')}{random.randint(100, 999)}{random.choice('ABCDEF')}"
                    self.detected_vehicle = {
                        "plate": plate,
                        "image_url": "/placeholder.svg",
                        "is_known": False,
                        "vehicle_id": None,
                        "confidence": round(random.uniform(0.75, 0.95), 2),
                    }
                self.show_alert_modal = True

    @rx.event
    async def accept_vehicle(self):
        from app.states.vehicle_registration_state import VehicleRegistrationState

        if self.detected_vehicle and self.detected_vehicle["is_known"]:
            print(f"Accepted known vehicle: {self.detected_vehicle['plate']}")
        else:
            print(
                f"Accepted unknown vehicle: {self.detected_vehicle['plate']}. Triggering registration."
            )
            self.show_registration_form = True
            registration_state = await self.get_state(VehicleRegistrationState)
            registration_state.new_vehicle_plate = self.detected_vehicle["plate"]
        self.show_alert_modal = False
        self.detected_vehicle = None

    @rx.event
    def reject_vehicle(self):
        print(f"Rejected vehicle: {self.detected_vehicle['plate']}")
        self.show_alert_modal = False
        self.detected_vehicle = None

    @rx.event
    def toggle_notifications(self):
        self.show_notifications = not self.show_notifications

    @rx.event
    def mark_notification_as_read(self, notification_id: int):
        for i, n in enumerate(self.notifications):
            if n["id"] == notification_id:
                self.notifications[i]["read"] = True
                break
        self.notification_count = len([n for n in self.notifications if not n["read"]])