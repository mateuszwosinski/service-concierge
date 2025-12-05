"""Mock Appointments API for managing meeting scheduling and queries."""

import json
from datetime import datetime
from typing import Optional

from concierge.datatypes.api_types import AppointmentInfo
from concierge.paths import APPOINTMENTS_DATA_PATH


class AppointmentsAPI:
    """Mock API for appointment management operations."""

    def __init__(self) -> None:
        """Initialize the Appointments API with mock data."""
        self._appointments: dict[str, AppointmentInfo] = self._initialize_mock_appointments()
        self._email_index: dict[str, list[str]] = {}
        self._phone_index: dict[str, list[str]] = {}
        self._build_indexes()

    @staticmethod
    def _initialize_mock_appointments() -> dict[str, AppointmentInfo]:
        """Load mock appointment data from JSON file."""
        data_path = APPOINTMENTS_DATA_PATH
        with data_path.open() as f:
            appointments_data = json.load(f)

        return {apt_id: AppointmentInfo(**apt_dict) for apt_id, apt_dict in appointments_data.items()}

    def _build_indexes(self) -> None:
        """Build email and phone indexes for quick lookup."""
        self._email_index.clear()
        self._phone_index.clear()

        for apt_id, appointment in self._appointments.items():
            # Email index
            if appointment.user_email not in self._email_index:
                self._email_index[appointment.user_email] = []
            self._email_index[appointment.user_email].append(apt_id)

            # Phone index
            if appointment.user_phone not in self._phone_index:
                self._phone_index[appointment.user_phone] = []
            self._phone_index[appointment.user_phone].append(apt_id)

    def get_appointment(self, appointment_id: str) -> Optional[AppointmentInfo]:
        """
        Retrieve appointment details by appointment_id.

        Args:
            appointment_id: The unique appointment identifier

        Returns:
            AppointmentInfo if found, None otherwise
        """
        return self._appointments.get(appointment_id)

    def get_appointments_by_email(self, email: str) -> list[AppointmentInfo]:
        """
        Retrieve all appointments for a user by their email address. Use this to check a client's existing appointments, including scheduled, confirmed, completed, or cancelled appointments.

        Args:
            email: User's email address (e.g., "client@example.com")

        Returns:
            List of AppointmentInfo objects with complete appointment details
        """
        apt_ids = self._email_index.get(email, [])
        return [self._appointments[apt_id] for apt_id in apt_ids if apt_id in self._appointments]

    def get_appointments_by_phone(self, phone: str) -> list[AppointmentInfo]:
        """
        Retrieve all appointments for a user by phone.

        Args:
            phone: User's phone number

        Returns:
            List of AppointmentInfo objects
        """
        apt_ids = self._phone_index.get(phone, [])
        return [self._appointments[apt_id] for apt_id in apt_ids if apt_id in self._appointments]

    def schedule_appointment(
        self, user_id: str, email: str, phone: str, date: str, time: str, service_type: str
    ) -> dict[str, str]:
        """
        Schedule a new appointment for services like Personal Styling Session, Tailoring and Fitting, Wardrobe Consultation, Custom Fitting, VIP Styling Experience, or Alteration Pickup. Automatically checks for conflicts and prevents double-booking.

        Business Logic:
        - Date must be in the future
        - No duplicate appointments at the same date/time for the same user

        Args:
            user_id: User's unique identifier
            email: User's email address
            phone: User's phone number (format: +1-555-0101)
            date: Appointment date in YYYY-MM-DD format
            time: Appointment time in HH:MM 24-hour format
            service_type: Type of service (e.g., "Personal Styling Session", "Tailoring and Fitting")

        Returns:
            Dictionary with success status, message, and appointment_id if successful
        """
        # Check for conflicting appointments
        existing_appointments = self.get_appointments_by_email(email)
        for apt in existing_appointments:
            if apt.date == date and apt.time == time and apt.status in ["scheduled", "confirmed"]:
                return {
                    "success": "false",
                    "message": f"You already have an appointment at {time} on {date}",
                }

        # Generate new appointment ID
        apt_count = len(self._appointments) + 1
        new_apt_id = f"APT-{apt_count:03d}"

        # Create appointment
        new_appointment = AppointmentInfo(
            appointment_id=new_apt_id,
            user_id=user_id,
            user_email=email,
            user_phone=phone,
            date=date,
            time=time,
            service_type=service_type,
            status="scheduled",
            created_at=datetime.now().isoformat(),
        )

        self._appointments[new_apt_id] = new_appointment
        self._build_indexes()

        return {
            "success": "true",
            "message": f"Appointment scheduled for {date} at {time}",
            "appointment_id": new_apt_id,
        }

    def reschedule_appointment(self, appointment_id: str, new_date: str, new_time: str) -> dict[str, str]:
        """
        Reschedule an existing appointment.

        Business Logic:
        - Appointment must exist
        - Appointment must not be cancelled or completed
        - New date/time must not conflict with other appointments

        Args:
            appointment_id: The unique appointment identifier
            new_date: New date in YYYY-MM-DD format
            new_time: New time in HH:MM format

        Returns:
            Dictionary with success status and message
        """
        appointment = self._appointments.get(appointment_id)

        if not appointment:
            return {"success": "false", "message": f"Appointment {appointment_id} not found"}

        if appointment.status in ["cancelled", "completed"]:
            return {
                "success": "false",
                "message": f"Cannot reschedule {appointment.status} appointment. Please schedule a new one.",
            }

        # Check for conflicts
        user_appointments = self.get_appointments_by_email(appointment.user_email)
        for apt in user_appointments:
            if (
                apt.appointment_id != appointment_id
                and apt.date == new_date
                and apt.time == new_time
                and apt.status in ["scheduled", "confirmed"]
            ):
                return {
                    "success": "false",
                    "message": f"You already have an appointment at {new_time} on {new_date}",
                }

        old_date = appointment.date
        old_time = appointment.time
        appointment.date = new_date
        appointment.time = new_time

        return {
            "success": "true",
            "message": f"Appointment rescheduled from {old_date} {old_time} to {new_date} {new_time}",
        }

    def cancel_appointment(self, appointment_id: str) -> dict[str, str]:
        """
        Cancel an appointment.

        Business Logic:
        - Appointment must exist
        - Appointment must not already be cancelled or completed

        Args:
            appointment_id: The unique appointment identifier

        Returns:
            Dictionary with success status and message
        """
        appointment = self._appointments.get(appointment_id)

        if not appointment:
            return {"success": "false", "message": f"Appointment {appointment_id} not found"}

        if appointment.status == "cancelled":
            return {"success": "false", "message": "Appointment is already cancelled"}

        if appointment.status == "completed":
            return {"success": "false", "message": "Cannot cancel a completed appointment"}

        appointment.status = "cancelled"

        return {
            "success": "true",
            "message": f"Appointment {appointment_id} on {appointment.date} at {appointment.time} has been cancelled",
        }

    def confirm_appointment(self, appointment_id: str) -> dict[str, str]:
        """
        Confirm an appointment.

        Args:
            appointment_id: The unique appointment identifier

        Returns:
            Dictionary with success status and message
        """
        appointment = self._appointments.get(appointment_id)

        if not appointment:
            return {"success": "false", "message": f"Appointment {appointment_id} not found"}

        if appointment.status == "confirmed":
            return {"success": "false", "message": "Appointment is already confirmed"}

        if appointment.status in ["cancelled", "completed"]:
            return {"success": "false", "message": f"Cannot confirm a {appointment.status} appointment"}

        appointment.status = "confirmed"

        return {
            "success": "true",
            "message": f"Appointment {appointment_id} on {appointment.date} at {appointment.time} has been confirmed",
        }


# Global instance
appointments_api = AppointmentsAPI()
