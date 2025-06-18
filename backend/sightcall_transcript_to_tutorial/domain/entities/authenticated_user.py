# AuthenticatedUser entity for TDD (initial stub, not implemented)


class AuthenticatedUser:
    def __init__(self, github_id: int, username: str, email: str):
        if github_id is None:
            raise ValueError("github_id is required")
        if not AuthenticatedUser._is_valid_email(email):
            raise ValueError(f"Invalid email: {email}")
        self.github_id = github_id
        self.username = username
        self.email = email

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        # Simple validation: must contain '@' and '.' after '@'
        if not isinstance(email, str) or "@" not in email:
            return False
        local, _, domain = email.partition("@")
        return bool(local) and "." in domain
