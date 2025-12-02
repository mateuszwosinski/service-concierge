"""Mock Appointments API for managing meeting scheduling and queries."""

from datetime import datetime
from typing import Optional

from concierge.datatypes.general_types import AppointmentInfo


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
        """Create mock appointment data."""
        return {
            "APT-001": AppointmentInfo(
                appointment_id="APT-001",
                user_email="john.doe@example.com",
                user_phone="+1-555-0101",
                date="2025-12-05",
                time="10:00",
                service_type="Consultation",
                status="scheduled",
                created_at="2025-11-25T09:00:00",
            ),
            "APT-002": AppointmentInfo(
                appointment_id="APT-002",
                user_email="jane.smith@example.com",
                user_phone="+1-555-0102",
                date="2025-12-06",
                time="14:30",
                service_type="Technical Support",
                status="confirmed",
                created_at="2025-11-26T11:30:00",
            ),
            "APT-003": AppointmentInfo(
                appointment_id="APT-003",
                user_email="john.doe@example.com",
                user_phone="+1-555-0101",
                date="2025-12-10",
                time="09:00",
                service_type="Follow-up",
                status="scheduled",
                created_at="2025-11-28T15:20:00",
            ),
            "APT-004": AppointmentInfo(
                appointment_id="APT-004",
                user_email="bob.wilson@example.com",
                user_phone="+1-555-0103",
                date="2025-12-03",
                time="16:00",
                service_type="Consultation",
                status="completed",
                created_at="2025-11-20T10:00:00",
            ),
            "APT-005": AppointmentInfo(
                appointment_id="APT-005",
                user_email="alice.brown@example.com",
                user_phone="+1-555-0104",
                date="2025-12-08",
                time="11:00",
                service_type="Product Demo",
                status="scheduled",
                created_at="2025-11-29T13:45:00",
            ),
        }

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
        Retrieve all appointments for a user by email.

        Args:
            email: User's email address

        Returns:
            List of AppointmentInfo objects
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

    def schedule_appointment(self, email: str, phone: str, date: str, time: str, service_type: str) -> dict[str, str]:
        """
        Schedule a new appointment.

        Business Logic:
        - Date must be in the future
        - No duplicate appointments at the same date/time for the same user

        Args:
            email: User's email address
            phone: User's phone number
            date: Appointment date in YYYY-MM-DD format
            time: Appointment time in HH:MM format
            service_type: Type of service

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
