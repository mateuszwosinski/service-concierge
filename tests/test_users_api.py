"""Tests for the Users API."""

import pytest

from concierge.external_systems.users import UsersAPI


class TestUsersAPI:
    """Test the Users API functionality."""

    @pytest.fixture
    def users_api(self):
        """Create a fresh UsersAPI instance for testing."""
        return UsersAPI()

    def test_get_user_by_email(self, users_api):
        """Test getting user by email."""
        # Test exact match (case-insensitive)
        user = users_api.get_user_by_email("john.doe@example.com")
        assert user is not None
        assert user.user_id == "user_123"
        assert user.name == "John Doe"
        assert user.email == "john.doe@example.com"
        assert user.phone == "+1-555-0101"

        # Test case insensitive
        user = users_api.get_user_by_email("JOHN.DOE@EXAMPLE.COM")
        assert user is not None
        assert user.user_id == "user_123"

        # Test non-existent email
        user = users_api.get_user_by_email("nonexistent@example.com")
        assert user is None

    def test_get_user_by_phone(self, users_api):
        """Test getting user by phone."""
        # Test exact match
        user = users_api.get_user_by_phone("+1-555-0102")
        assert user is not None
        assert user.user_id == "user_456"
        assert user.name == "Jane Smith"
        assert user.email == "jane.smith@example.com"
        assert user.phone == "+1-555-0102"

        # Test non-existent phone
        user = users_api.get_user_by_phone("+1-555-9999")
        assert user is None

    def test_get_user_by_id(self, users_api):
        """Test getting user by user_id."""
        # Test valid user_id
        user = users_api.get_user_by_id("user_789")
        assert user is not None
        assert user.user_id == "user_789"
        assert user.name == "Bob Wilson"
        assert user.email == "bob.wilson@example.com"
        assert user.phone == "+1-555-0103"

        # Test non-existent user_id
        user = users_api.get_user_by_id("user_999")
        assert user is None

    def test_get_all_users(self, users_api):
        """Test getting all users."""
        users = users_api.get_all_users()
        assert len(users) == 5
        assert all(user.user_id for user in users)
        assert all(user.name for user in users)
        assert all(user.email for user in users)
        assert all(user.phone for user in users)

    def test_email_index_integrity(self, users_api):
        """Test that email index is properly built."""
        # All users should be findable by their email
        all_users = users_api.get_all_users()
        for user in all_users:
            found_user = users_api.get_user_by_email(user.email)
            assert found_user is not None
            assert found_user.user_id == user.user_id

    def test_phone_index_integrity(self, users_api):
        """Test that phone index is properly built."""
        # All users should be findable by their phone
        all_users = users_api.get_all_users()
        for user in all_users:
            found_user = users_api.get_user_by_phone(user.phone)
            assert found_user is not None
            assert found_user.user_id == user.user_id

    def test_multiple_users(self, users_api):
        """Test that we can retrieve multiple different users."""
        user1 = users_api.get_user_by_email("alice.brown@example.com")
        user2 = users_api.get_user_by_email("michael.chen@example.com")

        assert user1 is not None
        assert user2 is not None
        assert user1.user_id != user2.user_id
        assert user1.user_id == "user_001"
        assert user2.user_id == "user_002"
