"""Tests for the Appointments API."""

from concierge.external_systems import appointments_api


class TestAppointmentsAPI:
    """Test suite for Appointments API functionality."""

    def test_get_appointment_success(self) -> None:
        """Test retrieving an existing appointment."""
        appointment = appointments_api.get_appointment("APT-001")

        assert appointment is not None
        assert appointment.appointment_id == "APT-001"
        assert appointment.user_email == "john.doe@example.com"
        assert appointment.service_type == "Personal Styling Session"
        assert appointment.status == "scheduled"

    def test_get_appointment_not_found(self) -> None:
        """Test retrieving a non-existent appointment."""
        appointment = appointments_api.get_appointment("APT-999")
        assert appointment is None

    def test_get_appointments_by_email(self) -> None:
        """Test retrieving appointments by email."""
        appointments = appointments_api.get_appointments_by_email("john.doe@example.com")

        assert len(appointments) == 2
        assert all(apt.user_email == "john.doe@example.com" for apt in appointments)

    def test_get_appointments_by_email_no_results(self) -> None:
        """Test retrieving appointments for email with no appointments."""
        appointments = appointments_api.get_appointments_by_email("nobody@example.com")
        assert len(appointments) == 0

    def test_get_appointments_by_phone(self) -> None:
        """Test retrieving appointments by phone number."""
        appointments = appointments_api.get_appointments_by_phone("+1-555-0102")

        assert len(appointments) == 1
        assert appointments[0].user_phone == "+1-555-0102"
        assert appointments[0].service_type == "Tailoring and Fitting"

    def test_get_appointments_by_phone_no_results(self) -> None:
        """Test retrieving appointments for phone with no appointments."""
        appointments = appointments_api.get_appointments_by_phone("+1-555-0000")
        assert len(appointments) == 0

    def test_schedule_appointment_success(self) -> None:
        """Test scheduling a new appointment."""
        result = appointments_api.schedule_appointment(
            user_id="user-123",
            email="new.client@example.com",
            phone="+1-555-9999",
            date="2025-12-20",
            time="15:00",
            service_type="Personal Styling Session",
        )

        assert result["success"] == "true"
        assert "scheduled" in result["message"].lower()
        assert "appointment_id" in result

        # Verify appointment was created
        new_apt_id = result["appointment_id"]
        appointment = appointments_api.get_appointment(new_apt_id)
        assert appointment is not None
        assert appointment.user_email == "new.client@example.com"

    def test_schedule_appointment_conflict(self) -> None:
        """Test scheduling appointment at conflicting time."""
        # Try to schedule at same time as existing appointment
        result = appointments_api.schedule_appointment(
            user_id="user-123",
            email="john.doe@example.com",
            phone="+1-555-0101",
            date="2025-12-05",
            time="10:00",
            service_type="Wardrobe Consultation",
        )

        assert result["success"] == "false"
        assert "already have" in result["message"].lower()

    def test_reschedule_appointment_success(self) -> None:
        """Test rescheduling an existing appointment."""
        result = appointments_api.reschedule_appointment("APT-001", "2025-12-07", "13:00")

        assert result["success"] == "true"
        assert "rescheduled" in result["message"].lower()

        # Verify appointment was updated
        appointment = appointments_api.get_appointment("APT-001")
        assert appointment is not None
        assert appointment.date == "2025-12-07"
        assert appointment.time == "13:00"

    def test_reschedule_appointment_not_found(self) -> None:
        """Test rescheduling non-existent appointment."""
        result = appointments_api.reschedule_appointment("APT-999", "2025-12-20", "10:00")

        assert result["success"] == "false"
        assert "not found" in result["message"].lower()

    def test_reschedule_appointment_completed_fails(self) -> None:
        """Test that rescheduling a completed appointment fails."""
        result = appointments_api.reschedule_appointment("APT-004", "2025-12-20", "10:00")

        assert result["success"] == "false"
        assert "cannot reschedule" in result["message"].lower()

    def test_cancel_appointment_success(self) -> None:
        """Test canceling an appointment."""
        result = appointments_api.cancel_appointment("APT-005")

        assert result["success"] == "true"
        assert "cancelled" in result["message"].lower()

        # Verify status changed
        appointment = appointments_api.get_appointment("APT-005")
        assert appointment is not None
        assert appointment.status == "cancelled"

    def test_cancel_appointment_not_found(self) -> None:
        """Test canceling non-existent appointment."""
        result = appointments_api.cancel_appointment("APT-999")

        assert result["success"] == "false"
        assert "not found" in result["message"].lower()

    def test_cancel_appointment_already_cancelled(self) -> None:
        """Test canceling already cancelled appointment."""
        # Cancel twice
        appointments_api.cancel_appointment("APT-006")
        result = appointments_api.cancel_appointment("APT-006")

        assert result["success"] == "false"
        assert "already cancelled" in result["message"].lower()

    def test_cancel_appointment_completed_fails(self) -> None:
        """Test that canceling a completed appointment fails."""
        result = appointments_api.cancel_appointment("APT-004")

        assert result["success"] == "false"
        assert "cannot cancel" in result["message"].lower()

    def test_confirm_appointment_success(self) -> None:
        """Test confirming an appointment."""
        result = appointments_api.confirm_appointment("APT-003")

        assert result["success"] == "true"
        assert "confirmed" in result["message"].lower()

        # Verify status changed
        appointment = appointments_api.get_appointment("APT-003")
        assert appointment is not None
        assert appointment.status == "confirmed"

    def test_confirm_appointment_not_found(self) -> None:
        """Test confirming non-existent appointment."""
        result = appointments_api.confirm_appointment("APT-999")

        assert result["success"] == "false"
        assert "not found" in result["message"].lower()

    def test_confirm_appointment_already_confirmed(self) -> None:
        """Test confirming already confirmed appointment."""
        result = appointments_api.confirm_appointment("APT-002")

        assert result["success"] == "false"
        assert "already confirmed" in result["message"].lower()
