import asyncio
from typing import Any
from urllib.parse import urlencode

import httpx
from jose import JWTError, jwt

from sightcall_transcript_to_tutorial.domain.config.settings import settings
from sightcall_transcript_to_tutorial.domain.entities.authenticated_user import AuthenticatedUser
from sightcall_transcript_to_tutorial.domain.entities.user import User
from sightcall_transcript_to_tutorial.domain.gateways.authentication_gateway_interface import (
    AuthenticationGatewayInterface,
)
from sightcall_transcript_to_tutorial.domain.repositories.user_repository_interface import UserRepositoryInterface
from sightcall_transcript_to_tutorial.domain.value_objects.user_id import UserId

# GitHub API URLs
GITHUB_AUTHORIZATION_URL: str = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL: str = "https://github.com/login/oauth/access_token"
GITHUB_USER_API_URL: str = "https://api.github.com/user"
GITHUB_USER_EMAILS_API_URL: str = "https://api.github.com/user/emails"
GITHUB_SCOPE: str = "read:user user:email"

# HTTP Headers
AUTHORIZATION_HEADER_TEMPLATE = "token {}"
JSON_ACCEPT_HEADER = "application/json"


class GitHubOAuthError(Exception):
    """Custom error for GitHub OAuth failures."""

    pass


class GitHubAuthenticationGateway(AuthenticationGatewayInterface):
    """
    Production gateway for GitHub OAuth 2.0 and JWT handling.
    Implements AuthenticationGatewayInterface.
    """

    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository
        self._initialize_configuration()

    def get_login_url(self) -> str:
        """Build the GitHub OAuth login URL for user redirection."""
        query_parameters = self._build_oauth_query_parameters()
        return f"{GITHUB_AUTHORIZATION_URL}?{urlencode(query_parameters)}"

    def authenticate_callback(self, code: str) -> AuthenticatedUser:
        """
        Exchange the OAuth code for an access token and fetch the GitHub user profile.
        Raise GitHubOAuthError on failure.
        """
        access_token = self._exchange_code_for_access_token(code)
        user_data = self._fetch_github_user_profile(access_token)
        validated_email = self._ensure_valid_email(user_data, access_token)
        user_data["email"] = validated_email
        return self._build_authenticated_user_from_github_data(user_data)

    def create_jwt(self, user: User) -> str:
        """Create a JWT for the user, including both user_id and github_id."""
        payload = self._build_jwt_payload(user)
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_jwt(self, token: str) -> AuthenticatedUser:
        """
        Decode and verify a JWT, returning the AuthenticatedUser.
        Raise ValueError if the token is invalid.
        """
        try:
            payload = self._decode_jwt_payload(token)
            return self._extract_authenticated_user_from_payload(payload)
        except (JWTError, KeyError, ValueError) as error:
            raise ValueError("Invalid JWT token") from error

    def get_current_user_from_jwt(self, token: str) -> User:
        """Extract and validate current user from JWT token."""
        try:
            payload = self._decode_jwt_payload(token)
            user_id, github_id = self._extract_user_identifiers_from_payload(payload)
            user = self._find_and_validate_user(user_id, github_id)
            return user
        except Exception as e:
            raise ValueError(f"Invalid JWT token for user extraction: {e}")

    def _initialize_configuration(self) -> None:
        """Initialize gateway configuration from settings."""
        self.client_id: str = settings.github_client_id
        self.client_secret: str = settings.github_client_secret
        self.callback_url: str = settings.github_callback_url
        self.jwt_secret: str = settings.jwt_secret
        self.jwt_algorithm: str = settings.jwt_algorithm

    def _build_oauth_query_parameters(self) -> dict[str, str]:
        """Build OAuth query parameters for GitHub authorization URL."""
        return {
            "client_id": self.client_id,
            "redirect_uri": self.callback_url,
            "scope": GITHUB_SCOPE,
        }

    def _build_jwt_payload(self, user: User) -> dict[str, Any]:
        """Build JWT payload from user data."""
        return {
            "user_id": user.user_id.value,
            "github_id": user.github_id,
            "username": user.name,
        }

    def _decode_jwt_payload(self, token: str) -> dict[str, Any]:
        """Decode JWT token and return payload."""
        return jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])

    def _extract_authenticated_user_from_payload(self, payload: dict[str, Any]) -> AuthenticatedUser:
        """Extract AuthenticatedUser from JWT payload."""
        github_id = int(payload["sub"])
        username = payload["username"]
        email = payload["email"]
        return AuthenticatedUser(github_id, username, email)

    def _extract_user_identifiers_from_payload(self, payload: dict[str, Any]) -> tuple[str, int]:
        """Extract user identifiers from JWT payload."""
        user_id = payload.get("user_id")
        github_id = payload.get("github_id")

        if not user_id:
            raise ValueError("JWT missing user_id")
        if github_id is None:
            raise ValueError("JWT missing github_id")

        return str(user_id), github_id

    def _find_and_validate_user(self, user_id: str, expected_github_id: int) -> User:
        """Find user by ID and validate GitHub ID matches."""
        user = self._user_repository.find_by_id(UserId(user_id))
        if not user:
            raise ValueError("User not found")
        if user.github_id != expected_github_id:
            raise ValueError("github_id mismatch")
        return user

    def _ensure_valid_email(self, user_data: dict[str, Any], access_token: str) -> str:
        """Ensure user data contains a valid email, fetching from API if needed."""
        email = user_data.get("email")
        email_str = email if isinstance(email, str) else ""

        if not AuthenticatedUser._is_valid_email(email_str):
            email_str = self._fetch_primary_email(access_token)

        if not AuthenticatedUser._is_valid_email(email_str):
            raise GitHubOAuthError("Invalid email returned from GitHub profile and /user/emails endpoint.")

        return email_str

    def _exchange_code_for_access_token(self, code: str) -> str:
        """Exchange the OAuth code for an access token using GitHub's API."""
        try:
            token_data = asyncio.run(self._perform_token_exchange(code))
        except Exception as error:
            raise GitHubOAuthError(f"Failed to exchange code for access token: {error}") from error

        access_token = token_data.get("access_token")
        if not access_token:
            raise GitHubOAuthError("No access token returned from GitHub.")
        return access_token

    def _fetch_github_user_profile(self, access_token: str) -> dict[str, Any]:
        """Fetch the GitHub user profile using the access token."""
        try:
            return asyncio.run(self._perform_user_profile_fetch(access_token))
        except Exception as error:
            raise GitHubOAuthError(f"Failed to fetch GitHub user profile: {error}") from error

    def _fetch_primary_email(self, access_token: str) -> str:
        """Fetch the user's primary email from the /user/emails endpoint."""
        try:
            emails = asyncio.run(self._perform_emails_fetch(access_token))
            return self._extract_primary_verified_email(emails)
        except Exception:
            return ""

    def _extract_primary_verified_email(self, emails: list[dict[str, Any]]) -> str:
        """Extract primary verified email from emails list."""
        # Find primary, verified email
        for email_obj in emails:
            if email_obj.get("primary") and email_obj.get("verified"):
                email = email_obj.get("email")
                return email if isinstance(email, str) else ""

        # Fallback: return first verified email
        for email_obj in emails:
            if email_obj.get("verified"):
                email = email_obj.get("email")
                return email if isinstance(email, str) else ""

        return ""

    def _build_authenticated_user_from_github_data(self, user_data: dict[str, Any]) -> AuthenticatedUser:
        """Build an AuthenticatedUser from GitHub API user data."""
        try:
            github_id = user_data["id"]
            username = user_data["login"]
            email = user_data.get("email") or ""
            return AuthenticatedUser(github_id, username, email)
        except (KeyError, ValueError) as error:
            raise GitHubOAuthError(f"Malformed GitHub user data: {error}") from error

    async def _perform_token_exchange(self, code: str) -> dict[str, Any]:
        """Perform async token exchange with GitHub."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                GITHUB_TOKEN_URL,
                data=self._build_token_exchange_data(code),
                headers={"Accept": JSON_ACCEPT_HEADER},
            )
            response.raise_for_status()
            return response.json()

    async def _perform_user_profile_fetch(self, access_token: str) -> dict[str, Any]:
        """Perform async user profile fetch from GitHub."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GITHUB_USER_API_URL,
                headers={"Authorization": AUTHORIZATION_HEADER_TEMPLATE.format(access_token)},
            )
            response.raise_for_status()
            return response.json()

    async def _perform_emails_fetch(self, access_token: str) -> list[dict[str, Any]]:
        """Perform async emails fetch from GitHub."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GITHUB_USER_EMAILS_API_URL,
                headers={"Authorization": AUTHORIZATION_HEADER_TEMPLATE.format(access_token)},
            )
            response.raise_for_status()
            return response.json()

    def _build_token_exchange_data(self, code: str) -> dict[str, str]:
        """Build data payload for token exchange request."""
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.callback_url,
        }
