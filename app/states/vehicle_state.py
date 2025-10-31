import reflex as rx
from typing import TypedDict, Optional
from app.models import Vehicle, WeighingTransaction, MaintenanceLog
import datetime


class VehicleAnalytics(TypedDict):
    total_transactions: int
    total_weight_moved: float
    total_revenue: float
    average_net_weight: float


class VehicleState(rx.State):
    """Manages the vehicle details page, including analytics, history, and maintenance."""

    selected_vehicle: Optional[Vehicle] = None
    vehicle_history: list[WeighingTransaction] = []
    vehicle_analytics: Optional[VehicleAnalytics] = None
    maintenance_logs: list[MaintenanceLog] = []
    filter_vehicle_type: str = "ALL"
    filter_status: str = "ALL"
    search_query: str = ""

    @rx.event
    async def load_vehicle_details(self, vehicle_id: int):
        from app.states.weighing_state import WeighingState

        weighing_state = await self.get_state(WeighingState)
        vehicle = next(
            (v for v in weighing_state.vehicles if v["id"] == vehicle_id), None
        )
        if vehicle:
            self.selected_vehicle = vehicle
            self.vehicle_history = [
                t
                for t in weighing_state.transactions
                if t.get("vehicle_id") == vehicle_id
            ]
            self._calculate_analytics()
            self._load_maintenance_logs(vehicle_id)

    def _calculate_analytics(self):
        total_transactions = len(self.vehicle_history)
        if total_transactions == 0:
            self.vehicle_analytics = {
                "total_transactions": 0,
                "total_weight_moved": 0,
                "total_revenue": 0,
                "average_net_weight": 0,
            }
            return
        total_weight_moved = 125000.5
        total_revenue = 87500.0
        average_net_weight = (
            total_weight_moved / total_transactions if total_transactions > 0 else 0
        )
        self.vehicle_analytics = {
            "total_transactions": total_transactions,
            "total_weight_moved": round(total_weight_moved, 2),
            "total_revenue": round(total_revenue, 2),
            "average_net_weight": round(average_net_weight, 2),
        }

    def _load_maintenance_logs(self, vehicle_id: int):
        self.maintenance_logs = [
            {
                "id": 1,
                "vehicle_id": vehicle_id,
                "service_date": (
                    datetime.date.today() - datetime.timedelta(days=30)
                ).isoformat(),
                "service_type": "Oil Change",
                "notes": "Completed routine oil change and filter replacement.",
                "next_service_due": (
                    datetime.date.today() + datetime.timedelta(days=150)
                ).isoformat(),
            },
            {
                "id": 2,
                "vehicle_id": vehicle_id,
                "service_date": (
                    datetime.date.today() - datetime.timedelta(days=90)
                ).isoformat(),
                "service_type": "Tire Rotation",
                "notes": "Rotated all tires and checked pressure.",
                "next_service_due": None,
            },
        ]

    @rx.event
    def go_back_to_list(self):
        self.selected_vehicle = None
        self.vehicle_history = []
        self.vehicle_analytics = None
        self.maintenance_logs = []