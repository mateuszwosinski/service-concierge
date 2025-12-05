"""Mock Users API for managing user lookups."""

import json
from typing import Optional

from concierge.datatypes.api_types import UserProfile
from concierge.paths import USERS_DATA_PATH


class UsersAPI:
    """Mock API for user lookup operations."""

    def __init__(self) -> None:
        """Initialize the Users API with mock data."""
        self._users: dict[str, UserProfile] = self._initialize_mock_users()
        self._email_index: dict[str, str] = {}
        self._phone_index: dict[str, str] = {}
        self._build_indexes()

    @staticmethod
    def _initialize_mock_users() -> dict[str, UserProfile]:
        """Load mock user data from JSON file."""
        data_path = USERS_DATA_PATH
        with data_path.open() as f:
            users_data = json.load(f)

        return {user_id: UserProfile(**user_dict) for user_id, user_dict in users_data.items()}

    def _build_indexes(self) -> None:
        """Build email and phone indexes for quick lookup."""
        self._email_index.clear()
        self._phone_index.clear()

        for user_id, user in self._users.items():
            # Email index (case-insensitive)
            self._email_index[user.email.lower()] = user_id

            # Phone index
            self._phone_index[user.phone] = user_id

    def get_user_by_email(self, email: str) -> Optional[UserProfile]:
        """
        Get user profile by email address. Use this to find a user's user_id and details when you have their email. Returns complete user profile including user_id, name, email, and phone.

        Args:
            email: User's email address (case-insensitive)

        Returns:
            UserProfile object if found, None otherwise
        """
        user_id = self._email_index.get(email.lower())
        if user_id:
            return self._users.get(user_id)
        return None

    def get_user_by_phone(self, phone: str) -> Optional[UserProfile]:
        """
        Get user profile by phone number. Use this to find a user's user_id and details when you have their phone number. Returns complete user profile including user_id, name, email, and phone.

        Args:
            phone: User's phone number (format: +1-555-0101)

        Returns:
            UserProfile object if found, None otherwise
        """
        user_id = self._phone_index.get(phone)
        if user_id:
            return self._users.get(user_id)
        return None

    def get_user_by_id(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile by user_id.

        Args:
            user_id: The unique user identifier

        Returns:
            UserProfile object if found, None otherwise
        """
        return self._users.get(user_id)

    def get_all_users(self) -> list[UserProfile]:
        """
        Get all users in the system.

        Returns:
            List of all UserProfile objects
        """
        return list(self._users.values())


# Global instance
users_api = UsersAPI()
