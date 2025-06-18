from sightcall_transcript_to_tutorial.application.commands.login_command import LoginCommand
from sightcall_transcript_to_tutorial.infrastructure.for_tests.gateways.fake_authentication_gateway import (
    FakeAuthenticationGateway,
)
from sightcall_transcript_to_tutorial.infrastructure.for_tests.repositories.fake_user_repository import (
    FakeUserRepository,
)


class TestLoginCommand:
    """Test LoginCommand for GitHub OAuth login URL generation"""

    def test_should_return_github_oauth_login_url_when_executed(self):
        """Test successful generation of GitHub OAuth login URL"""
        # Given
        command = self._given_login_command_with_fake_gateway()

        # When
        login_url = self._when_executing_login_command(command)

        # Then
        self._then_should_return_expected_github_login_url(login_url)

    def _given_login_command_with_fake_gateway(self) -> LoginCommand:
        """Setup login command with fake authentication gateway"""
        user_repo = FakeUserRepository()
        gateway = FakeAuthenticationGateway(user_repo)
        return LoginCommand(gateway)

    def _when_executing_login_command(self, command: LoginCommand) -> str:
        """Execute the login command"""
        return command.execute()

    def _then_should_return_expected_github_login_url(self, login_url: str) -> None:
        """Verify that the returned URL matches expected GitHub OAuth URL"""
        expected_url = "https://fake-oauth/login"
        assert login_url == expected_url
