from sightcall_transcript_to_tutorial.domain.gateways.authentication_gateway_interface import (
    AuthenticationGatewayInterface,
)


class LoginCommand:
    def __init__(self, gateway: AuthenticationGatewayInterface):
        self.gateway = gateway

    def execute(self) -> str:
        return self.gateway.get_login_url()
